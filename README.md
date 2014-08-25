Tweet Sense -- Twitter interactive intelligence api
===================================================

TweetSense is fundamentally, the ultimate twitter intelligence experience. Browse twitter, create virtual focus groups, manipulate and experience the data, as trends and memes evolve. Welcome to TweetSense!

NOTE: Demographics are fundametally sets, and accordingly, somewhere there just has to be a venn
      diagram. While simplistic in conception, the implementation of demographics as sets allows
      fine tuning of a sample population using set operations, so this functionality should be
      represented somewhere in the front end.

<pre>
      >>> gamer_ girls = Specs(gender='female',
      ...                      age=range(13,30), keywords=('nintendo', 'game', 'xbox', 'play'))
      >>> nerds = Specs(gender=['male', 'female'],
      ...               age=range(13,30), keywords=('star trek', 'larping', 'comic books'))
      >>> gamer_girls_and_nerds = Demographic(specs=women) & Demographic(specs=nerds)

      Any poll on gamer_girls_and_nerds will use the intersection of the gamer girls and the nerds.
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
      with the assertion that the popularity of The Big Bang Theory is behaving with the characteristics
      of an emerging meme.
</pre>

NOTE: Spotlight and Discovery functionality are the two "killer features" and accordingly will take
      the longest to complete. One of the problems in machine learning is having one giant data set
      and two or more fundamental operations that are incompatibly amenable to different data structures.
      The idea is to provide a user experience so intuitive it will offset the surpise factor of
      deep insights.

Workflow:

First build a training corpus,
-- Form a representative "demographic".
-- Download and index their tweets

<pre>
>>> female_gamers = Specs(gender=['female'], age=range(13,30), keywords=['nintendo', 'game', 'xbox', 'play'])
>>> demographic = Demographic('gamer chicks', specs=female_gamers)
>>> demographic.sync()
</pre>

Alternatively, you can directly specify a group of users as the target demographic,

<pre>
>>> big_guys_with_tiny_dogs = map(User, ('arnoldS_69', 'DanielTosh', 'christina_aguilera'))
>>> demographic = Demographic('men with ridiculous dogs', users=big_guys_with_tiny_dogs)
>>> demographic.sync()
</pre>

Now create a question, any question with a yes or no answer,
-- Give the question a label
-- Supply a training set of real or hypothetical tweets that answers the question (1 means yes, 0 means no)

<pre>
>>> label = "Is xbox more popular than nintendo?"
>>> training_tweets = (('xbox rocks', 1), ('nintendo is better than xbox', 0),
                       ('xbox is way cooler', 1), ('I love mario cart more than halo.', 0))
>>> question = Question(label, training_tweets)
</pre>

Poll a focus group,
5) Ask the question, using any modifiers

<pre>
>>> poll = demographic.poll(question)
</pre>

Modifiers may be used to do trend analysis,

<pre>
>>> trend = Trend(t_start='3/12/2014', near=('atlanta', 'north carolina', '123 Maple Lane, North Pole'))
>>> poll = demographic.poll(question, qualifiers=trend)
</pre>

REST API
--------
This is a JSON/REST api that adheres to the following url hierarchy and json schemas:

<pre>
GET /demographic
- Gets all demographics
- Returns a json structure with the following format,
{
    demographics: [...]  # list of demographic json objects (see GET /demographic/<demographic name>)
}
</pre>

<pre>
GET /demographic/(?P<name>.*)
- Gets the specified demographic
- Returns a json structure with the following format,
{
    name: ...,
    specs: {
           age: [...],        # list of integers
           gender: [...],     # list of strings (ie 'male', 'female')
           location: [...],   # list of strings (colon separated lat:long, addresses, or regions)
           keywords: [...],   # list of strings (keyword phrases and hashtags)
           n_followers: ...,  # string (integer prefixed with `<`, `>`, or `=`)
           n_friends: ...     # string (integer prefixed with `<`, `>`, or `=`)
           },
    users: [...]              # list of strings (twitter handles)
}
</pre>

<pre>
POST /demographic
- Creates a demographic
- Takes a json structure with the following format,
{
    name: ...,
    specs: {
           age: [...],        # list of integers
           gender: [...],     # list of strings (ie 'male', 'female')
           location: [...],   # list of strings (colon separated lat:long, addresses, or regions)
           keywords: [...],   # list of strings (keyword phrases and hashtags)
           n_followers: ...,  # string (integer prefixed with `<`, `>`, or `=`)
           n_friends: ...     # string (integer prefixed with `<`, `>`, or `=`)
           },
    users: [...]              # list of strings (twitter handles)
}
</pre>

<pre>
PUT /demographic/(?P<name>.*)
- Updates a demographic but does not re-sync
- Takes a json structure with the following format,
{
    name: ...,
    specs: {
           age: [...],        # list of integers
           gender: [...],     # list of strings (ie 'male', 'female')
           location: [...],   # list of strings (colon separated lat:long, addresses, or regions)
           keywords: [...],   # list of strings (keyword phrases and hashtags)
           n_followers: ...,  # string (integer prefixed with `<`, `>`, or `=`)
           n_friends: ...     # string (integer prefixed with `<`, `>`, or `=`)
           },
    users: [...]              # list of strings (twitter handles)
}
</pre>

<pre>
DELETE /demographic/(?P<name>.*)
- Removes the demographic from the database
- Returns empty json structure
</pre>

<pre>
GET /demographic/(?P<name>.*)/sync
- Syncs the demographic on the backend (ie dumps the tweets to the database)
- Returns an empty json structure
</pre>

<pre>
POST /demographic/(?P<name>.*)/clone
- Creates a copy of the demographic and saves to the database
- Returns an empty json structure
- Takes json structure of the format,
{
    name: ...  # name of the cloned demographic
}
</pre>

</pre>
GET /demographic/(?P<name>.*)/broaden
- Expands the demographic to include friends and followers
- Returns empty json structure
</pre>

<pre>
GET /demographic/(?P<name>.*)/sample/(?P<sample_size>.*)
- Returns a random sample from the demographic
- Returns a json structure with the following format,
{
    users: [...]  # list of strings (user handles)
}
</pre>

<pre>
GET /demographic/(?P<name>.*)/poll
- Gets all the polls for the demographic
- Returns a json structure of the following format,
{
    polls: [...]  # list of poll json objects
}
</pre>

<pre>
POST /demographic/(?P<name>.*)/poll
- Polls the demographic
- Returns json, {id: ..., result: ...}, where `id` is the poll id and `result` is a float
- Takes a json structure of the following format,
{
    question: ...,  # string (label of the question)
    trend: ...      # string (id of a trend you'd like to qualify the search with)
}
</pre>

<pre>
GET /demographic/(?P<name>.*)/poll/(?P<id>.*)
- Gets the results of the corresponding poll
- Returns a json structure of the following format,
{
    id: ...,        # string
    question: ...,  # string (label of the question)
    trend: ...      # string (id of the trend, if any)
}
</pre>

<pre>
DELETE /demographic/(?P<name>.*)/poll/(?P<id>.*)
- Removes a poll from the database
- Returns empty json structure
</pre>

Questions can be of any type so long as they have a two valued answer space (most often
yes or no). To create a question, the classifier has to be trained on some examples
which can either be existing -- actual -- tweets, or can be hypothetical tweets.

<pre>
GET /question/(?P<label>.*)
- Gets a question
- Returns a json structure with the following format,
{
    label: ...,              # string
    exemplars: [...]         # list of tuples (each tuple is a tweet and a "score")
}
</pre>

<pre>
POST /question
- Creates a question
- Returns json, {label: ...}
- Takes a json structure with the following format,
{
    label: ...,              # string
    exemplars: [...]         # list of tuples (each tuple is a tweet and a "score")
}
</pre>

<pre>
DELETE /question/(?P<label>.*)
- Removes the question from the database
- Returns empty json structure
</pre>

NOTE: Questions are immutable once created, for simplicity, so there is no PUT method for
      updating an existing question. Rather, delete and create anew (might change in future)

Trends are under construction,

<pre>
GET /trend/(?P<id>.*)
- TBD
</pre>

<pre>
POST /trend
- TBD
</pre>

<pre>
PUT /trend/(?P<id>.*)
- TBD
</pre>

<pre>
DELETE /trend/(?P<id>.*)
- TBD
</pre>

Suggestions are under construction. Suggestions allow a user to ask the backend for advice and
recommendations on demographics, questions, and trends

<pre>
GET /suggestion
- TBD
</pre>

<pre>
POST /suggestion
- TBD
</pre>

<pre>
GET /suggestion/(?P<id>.*)
- TBD
</pre>

<pre>
DELETE /suggestion/(?P<id>.*)
- TBD
</pre>

<pre>
GET/POST/PUT/DELETE /account
- TBD
</pre>

<pre>
GET/POST/PUT/DELETE /user
- TBD
</pre>

<pre>
GET/POST/PUT/DELETE /admin
</pre>