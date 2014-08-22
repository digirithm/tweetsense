"""
Tweet Sense -- Twitter interactive intelligence api

TODO: In no particular order,

      Trend creation and manipulation.

      Suggestion creation and manipulation.

      Boosting functionality (crowd sources ML logic to a bunch of specialized weak learners to
      increase accuracy without overfitting).

      Spotlight and Discovery.

      Visualization aids, data cleaning, pipelining.
"""
# sanity check
import sys
assert not sys.version.startswith('2'), 'Compatible with only python >= 3.*'

# main imports
import types
import random
import asyncio
from collections import namedtuple
from pymongo import MongoClient, ObjectId
from TextBlob import TextBlob
from TextBlob.classifiers import NaiveBayesClassifier

# temporary wrapper
Specs = namedtuple('age gender location keywords n_followers n_friends')

# Twitter API V-1.1 URLs, count set to max
GET_USER_TWEETS_URL = 'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=%s&count=3200'

# event loop for pulling in tweets and persisting them server side
DL_LOOP = asyncio.BaseEventLoop()  # download tweets
DB_LOOP = asyncio.BaseEventLoop()  # persist in data store

# handles mongo connections
MONGO_CLIENT = MongoClient()
DATA_STORAGE = MONGO_CLIENT['data']
USER_STORAGE = MONGO_CLIENT['user']


class InheritanceException(Exception):
    pass


class StorageException(Exception):
    pass


class EnforceHashableMeta(type):
    """
    Ensures the base class is hashable.
    """
    def __new__(meta, name, bases, attrs):
        if len(bases) and not all(isinstance(b, types.Hashable) for b in bases):
            raise InheritanceException('Can only use Persitable with hashable types')
        # intentionally not using `super`
        return type.__new__(meta, name, bases, attrs)


class Persistable(metaclass=EnforceHashableMeta):
    """
    Is a mixin that allows hashing, classification, and mongo persistance to be performed
    using the same subtype across multiple APIs (in other words, gets rid of about 10K lines
    of code) and is more lightweight than a traditional ORM solution.

    It is imperative to only use this mixin with hashable types!
    """
    storage = None

    @property
    def _id(self):
        return ObjectId(hash(self))

    def dehydrate(self):
        """
        Creates a serializable dictionary from the object. Override in a subclass.
        """
        raise NotImplementedError(self.__doc__)

    @classmethod
    def hydrate(cls, data, from_string=False):
        """
        Takes a dictionary and recreates the object from the class. If `from_string`
        is set to True, you may pass in raw json as the data. Override in a subclass.
        """
        raise NotImplementedError(self.__doc__)

    @asyncio.coroutine
    def _async_save(self):
        """
        py 3.* only, in 2.* series this would have to be done with gevent
        """
        if not hasattr(self.storage) or self.storage is None:
            raise StorageException('Data store has not been set on this class')

        future = asyncio.Future()

        def dump():
            data = self.dehydrate()
            # force upserts for simplicity
            saved = self.storage.update({'_id': self._id}, data, upsert=True)
            future.set_result(saved)
            # up-delegate flow control
            yield from asyncio.sleep(0)

        DB_LOOP.run_until_complete(dump)
        return future.result

    @classmethod
    def load_object(cls, _id=None):
        """
        A blank _id retrieves all documents in a particular collection
        """
        if _id:
            hsh = _id if isinstance(_id, ObjectId) else ObjectId(_id)
            return cls.hydrate(cls.storage.find_one({'_id': hsh}))
        else:
            # rehydrate an entire collection of documents
            return [cls.hydrate(x) for x in cls.storage.find()]

    def save(self):
        return self._async_save()

    @classmethod
    def save_objects(cls, obj):
        return obj.save() if not \
               isinstance(obj, types.SequenceType) else [x.save() for x in obj]

    # For asynchronously accessing the multiprocessing API via `pickle`

    def __setstate__(self, state):
        return self.hydrate(state)

    def __getstate__(self):
        return self._async_save()

    # End multiprocessing


def set_storage(db=db, name=name):
    def _wrap_cls(cls):
        cls.storage = db[collection_name]
        def _object_factory(*args, **kwargs):
            return cls(*args, **kwargs)
        return _object_factory
    return _wrap_cls


def rate_limit(calls_per_window=3200, window=TWITTER_API_LIMIT):
    def _wrap(F):
        @functools.lru_cache
        def _call(*args, **kwargs):
            return F(*args, **kwargs)
        return _call
    return _wrap
    

# Spotlight and Discovery functionality are under construction. The idea is to address
# the search/retrieval dilemma through a common framework, while maximizing insight
# and minimizing suprise.
#
# Insight vs Suprise: A primer
#
# Take, for instance, the old days of Google when you could browse the internet by topic.
# This was great when you wanted to discover something but didn't know what to search for,
# especially before boolean filters were permitted or query prompting. To learn about light
# trucks, you would navigate categories>automotive>trucks>light-trucks and you would find
# all sorts of information about light trucks. The problem with this approach is that...etc
# ...TODO FINISH EXPLANATION


class Spotlight(Persistable):
    pass


class Discovery(Persistable):
    pass


# Core functionality ...


def _attach_ObjectId(X):
    """
    Prepares a tweet for persistance
    """
    X['_id'] = ObjectId(hash(X['screen_name']))
    return X


@set_storage(db=DATA_STORAGE, name='twitter_user')
class TwitterUser(int, Persistable):
    """
    Rough approximation of a twitter user whose tweets can be persisted or
    used as a classifier.
    """

    def __new__(cls, handle):
        instance = int.__new__(cls, hash(handle))
        instance.handle = handle
        instance._tweet_cache = None
        return instance

    @rate_limit(calls_per_window=10, window=TWITTER_API_LIMIT)
    def download_tweets(self, **filters):
        future = asyncio.Future()

        @asyncio.coroutine
        def do_get():
            response, content = request.get(GET_USER_TWEETS_URL % self.handle)
            future.set_result((response, content))
            # up-delegate flow control
            yield from asyncio.sleep(0)

        DL_LOOP.run_until_complete(do_get)
        r, c = future.result
        if r.status_code == 200:
            self._tweet_cache = tweets = c.json
            # force upsert
            self.storage.update((_attach_ObjectId(t) for t in tweets), upsert=True)

    @property
    def tweets(self):
        if not self._tweet_cache:
            self.download_tweets()
            return self.tweets
        else:
            return self._tweet_cache

    def update_cache(self):
        self._tweet_cache = self.storage.find({'_id': ObjectId(hash(self.handle))})

    def clear_cache(self):
        self._tweet_cache = None


@set_storage(db=USER_STORAGE, name='demographic')
class Demographic(frozenset, Persistable):
    """
    Demographics are fundamentally sets,

    >>> gamer_ girls = Specs(gender='female',
    ...                      age=range(13,30), keywords=('nintendo', 'game', 'xbox', 'play'))
    >>> nerds = Specs(gender=['male', 'female'],
    ...               age=range(13,30), keywords=('star trek', 'larping', 'comic books'))
    >>> gamer_girls_and_nerds = Demographic(specs=women) & Demographic(specs=nerds)

    Any poll on gamer_girls_and_nerds will use the intersection of the gamer girls and nerds.
    Trend handling is very powerful, for instance, to poll this hybrid demographic for changes
    in opinion regarding potentially engaging subject matter,

    >>> question = Question(label='Do you like Big Bang Theory?',
                            exemplars=[...scored training tweets...])
    >>> is_popular = gamer_girls_and_nerds.poll(question=question,
                                                trend=Trend.common.emerging_meme, weighted=True)
    >>> print(is_popular)
    (agree=0.7918, trending=0.28)

    The above result indicates that the majority of the demographic's members answer the question
    in the affirmative, however, as the show has been around for many seasons, the model disagrees
    with the assumption that the popularity of The Big Bang Theory is behaving with the characteristics
    of an emerging meme.
    """

    def __new__(cls, name, specs=None, users=None):
        instance = frozenset.__new__(cls,
                        cls.build_from_specification(specs) if specs else users)
        instance.name = name
        return instance

    def poll(self, question, trend=None, weighted=False):
        """
        Uses the demographic as a focus group to answer a yes or no question.
        The return value sits inside the interval between 0 and 1, where 0 is
        a definite "no" and 1 is a definite "yes".
        """
        # get the sample size
        N = float(len(self))
        # `ask` does the polling
        if not weighted:
            ask = lambda user: question(user, trend)
        else:
            # if weighted flaq is set, then weight the vote by the number of followers,
            # making the assumption that the more followers, the more influential a user.
            normalizing_constant = float(sum(len(user.followers) for user in self))
            ask = lambda user: question(user, trend) * len(user.followers) / normalizing_constant
        # calculate the average
        result = sum(ask(user) for user in self) / N)
        return Poll(question=question, trend=trend, result=result)

    def sync(self):
        """
        Updates the backend asynchronously
        """
        for user in self:
            user.download_tweets()

    def build_from_specification(self, specs):
        """
        Search twitter for users matching the specifications.
        """
        pass

    def sample(self, N=100):
        """
        Return a sample of the demographic with respect to a gaussian (i.e. normal) distribution.
        """
        return self.__class__(users=random.sample(self, N))

    @classmethod
    def sample_demographic(cls, demo, N=100):
        return demo.sample(N)

    def broaden(self):
        cls = self.__class__
        new = self | cls.broaden_demographic(self)
        return cls(self.name, new)

    @classmethod
    def broaden_demographic(cls, demo):
        """
        Grows the membership of a demographic by collecting the friends and followers.
        Prefixes name with a temporary `_` to indicate that we are simulating the
        "update" of an overriden immutable type.
        """
        return cls('_' + demo.name,
                   users=(frozenset(user.friends) | frozenset(user.followers) for user in demo))


# Under Construction, Trends/Suggestions


class Trend(int, Persistable):
    pass


class Suggestion(int, Persistable):
    pass


# Machine Learning facade


def not_implemented(*args, **kwargs):
    raise NotImplementedError


class EnforceCallableHashedTypeMeta(EnforceHashableMeta):
    """
    Ensures all hasbable subtypes are callable.
    """
    def __new__(meta, name, bases, attrs):
        if len(bases) and not any('__call__' in b.__dict__ for b in bases):
            raise InheritanceException('Subtypes must declare themselves callable')
        # intentionally not using `super`
        return EnforceHashableMeta.__new__(meta, name, bases, attrs)


class Classifier(int, Persistable, metaclass=EnforceCallableHashedTypeMeta):
    """
    Wrapper class for integer labeled classifiers, for use in TextBlob or scikit-learn.
    Use NaiveBayes as the default because it gives the best results for our current setup.
    """

    def __new__(cls, label, exemplars, classifier_type=None):
        instance = int.__new__(cls, hash(label))
        instance.label = label
        instance.logic = (classifier_type or NaiveBayesClassifier)(exemplars)
        return instance

    # don't do anything mathy with the classifiers to be on the safe side
    __add__ = __sub__ = __mul__ = __div__ = not_implemented

    def analyze(self, *args, **kwargs):
        # downward delegation
        return self.logic(*args, **kwargs)


@set_storage(db=USER_STORAGE, name='question')
class Question(Classifier):
    def __call__(self, user, trend=None):
        return self.analyze(user.tweets)
