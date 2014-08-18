"""
Tweet Sense -- Twitter interactive intelligence api

Building a training corpus:
1) Form a representative "demographic".
2) Download and index their tweets

>>> female_gamers = Specs(gender=['female'], age=range(13,30), keywords=['nintendo', 'game', 'xbox', 'play'])
>>> demographic = Demographic('gamer chicks', specs=female_gamers)
>>> demographic.sync()

Alternatively, you can directly specify a group of users as the target demographic,

>>> big_guys_with_tiny_dogs = map(User, ('arnoldS_69', 'DanielTosh', 'christina_aguilera'))
>>> demographic = Demographic('men with ridiculous dogs', users=big_guys_with_tiny_dogs)
>>> demographic.sync()

Creating a question:
3) Label the question
4) Supply a training set of real or hypothetical tweets that answers the
   question (1 means yes, 0 means no)

>>> label = "Is xbox more popular than nintendo?"
>>> training_tweets = (('xbox rocks', 1), ('nintendo is better than xbox', 0),
                       ('xbox is way cooler', 1), ('I love mario cart more than halo.', 0))
>>> question = Question(label, training_tweets)

Poll a focus group:
5) Ask the question, using any modifiers

>>> poll = demographic.poll(question)

Modifiers may be used to do trend analysis,

>>> trend = Trend(t_start='3/12/2014', near=('atlanta', 'north carolina', '123 Maple Lane, North Pole'))
>>> poll = demographic.poll(question, qualifiers=trend)

NOTE: Demographics are fundametally sets, and accordingly, somewhere there just has to be a venn
      diagram. While simplistic in conception, the implementation of demographics as sets allows
      fine tuning of a sample population using set operations, so this functionality should be
      represented somewhere in the front end.

NOTE: Since we are a data science company, lets do some freaking data science! Suggestions will be
      one of the most powerful features because it gives us access to who is trying to learn what
      about whom. My mental image is of how google suggests search completions as you type.

NOTE: I need input from you guys about what you think a "trend" should be. Think in terms of feature
      recognition, because I want to be able to predict trend emergence by appling time series pattern
      matching on well defined, quantifiable features of trends.

NOTE: Spotlight and Discovery functionality are the two "killer features" and accordingly will take
      the longest to complete. One of the problems in machine learning is having one giant data set
      and two or more fundamental operations that are incompatibly amenable to different data structures.
      The idea is to provide a user experience so intuitive it will offset the surpise factor of
      deep insights.

TODO: In no particular order,

      Exception handling - backend exceptions should provide detailed json responses that ease client
      side debugging and introspection.

      Trend creation and manipulation.

      Suggestion creation and manipulation.

      Boosting functionality (crowd sources ML logic to a bunch of specialized weak learners to
      increase accuracy without overfitting).

      Backend data store handling needs improvement.

      Docker integration.

      Spotlight and Discovery.

      Visualization aids, data cleaning, pipelining.
"""

from collections import namedtuple
import random
from pymongo import MongoClient
import asyncio
from TextBlob import TextBlob
from TextBlob.classifiers import NaiveBayesClassifier

# temporary wrappers
Tweet = namedtuple('content t_created retweets geo')
Specs = namedtuple('age gender location keywords n_followers n_friends')

# Twitter API V-1.1 URLs
GET_TWEET_URL = '...'

# event loop for pulling in tweets and persisting them server side
DL_LOOP = asyncio.BaseEventLoop()  # download tweets
DB_LOOP = asyncio.BaseEventLoop()  # persist in data store

# handles mongo connection
MONGO = MongoClient()


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
# all sorts of information about light trucks. The problem with this approach is that


class Spotlight:
    pass


class Discovery:
    pass


class TwitterUser(int):
    db_prefix = 'twitter_user'
    db = MONGO[db_prefix]

    def __init__(self, handle):
        self.handle = handle

    def to_json(self):
        pass

    def dump(self):
        json = self.to_json()
        self.db.insert()

    def _save(self):
        asyncio.Task(self.dump, self.db, loop=DB_LOOP)

    @asyncio.coroutine
    def tweets(self, **filters):
        response, content = request.get(GET_TWEET_URL % self.handle, parameters=filters)
        yield from iter((content,))

    @asyncio.coroutine
    def dump(self, db):
        pass

    def load_tweets(self):
        pass

    def __setstate__(self, state):
        pass

    def __getstate__(self):
        self.db.insert({'label': label, 'exemplars': exemplars})



class Demographic(frozenset):
    """
    spec = Specs(gender='female', age=range(13,30), keywords=('nintendo', 'game', 'xbox', 'play'))
    demo = Demographic('gamer_chicks', specs=spec)
    """
    db_prefix = 'demographic'
    db = MONGO[db_prefix]

    def __new__(cls, name, specs=None, users=None):
        instance = super().__new__(cls.build_from_specification(specs) if specs else users)
        instance.name = name
        return instance

    def poll(self, question, qualifiers=None, weighted=False):
        """
        Uses the demographic as a focus group to answer a yes or no question.
        The return value sits inside the interval between 0 and 1, where 0 is
        a definite "no" and 1 is a definite "yes".
        """
        # get the sample size
        N = float(len(self))
        # `ask` does the polling
        if not weighted:
            ask = lambda user: question(user, qualifiers)
        else:
            # if weighted flaq is set, then weight the vote by the number of followers,
            # making the assumption that the more followers, the more influential a user.
            normalizing_constant = float(sum(len(user.followers) for user in self))
            ask = lambda user: question(user, qualifiers) * len(user.followers) / normalizing_constant
        # calculate the average
        return sum(ask(user) for user in self) / N

    def sync(self):
        """
        Updates the backend asynchronously
        """
        for user in self:
            get_tweets = asyncio.Task(user.tweets, loop=DL_LOOP)
            save_to_db = asyncio.Task(user.dump, self.db, loop=DB_LOOP)
            DL_LOOP.run_until_complete(get_tweets)
            DB_LOOP.run_until_complete(save_to_db)

    def build_from_specification(self, specs):
        """
        Search twitter for users matching the specifications.

        Under construction.
        """
        pass

    def sample(self, N=100):
        """
        Return a sample of the demographic with respect to a gaussian distribution.
        """
        return random.sample(self, N)

    def broaden(self):
        """
        Mutates the demographic in place.
        """
        expanded = self.broaden_demographic(self)
        self.update(expanded)

    @classmethod
    def broaden_demographic(cls, demo):
        """
        Grows the membership of a demographic by including the friends and followers.
        """
        new = cls(demo.name,
                  users=(set(user.friends) | set(user.followers) for user in demo))
        new.update(demo)
        return new

    def to_json(self):
        pass

    def dump(self):
        pass

    def _save(self):
        asyncio.Task(self.dump, self.db, loop=DB_LOOP)

    def __setstate__(self, state):
        pass

    def __getstate__(self):
        state = {'_id': self}
        self.db.insert(state)
        return state



class Classifier(int):
    """
    Wrapper class for integer labeled classifiers, for use in TextBlob or scikit-learn
    """
    db_prefix = 'classifier'
    db = MONGO[db_prefix]

    def __new__(cls, label, exemplars, cls=None):
        instance = super().__new__(hash(label))
        instance.label = label
        instance.logic = (cls or NaiveBayesClassifier)(exemplars)
        return instance

    @staticmethod
    def not_implemented(*args, **kwargs):
        raise NotImplementedError

    __call__ = __add__ = __sub__ = __mul__ = __div__ = not_implemented

    def analyze(self, *args, **kwargs):
        return self.logic(*args, **kwargs)

    def to_json(self):
        pass

    def dump(self):
        pass

    def _save(self):
        asyncio.Task(self.dump, self.db, loop=DB_LOOP)

    def __setstate__(self, state):
        pass

    def __getstate__(self):
        state = {'_id': self, 'label': label, 'exemplars': exemplars}
        self.db.insert(state)
        return state


class Question(Classifier):
    db_prefix = 'question'
    db = MONGO[db_prefix]

    def __call__(self, user, qualifiers=None):
        return self.analyze(user.load_tweets())

    def to_json(self):
        pass

    def dump(self):
        pass

    def _save(self):
        asyncio.Task(self.dump, self.db, loop=DB_LOOP)

    def __setstate__(self, state):
        pass

    def __getstate__(self):
        self.db.insert({'label': label, 'exemplars': exemplars})



class Trend:
    pass


class Suggestion:
    pass