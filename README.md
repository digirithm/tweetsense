tweetsense
==========

Twitter interactive intelligence api



Client side is really a glorified twitter browser with one hell of a UX. When a client logs in, the browser makes a connection to the server and populates the account, preloading any "favorite" demographics, questions, or saved trend data. The REST api exposes hooks to each of the five numbered steps listed below.

Building a training corpus:
1) Form a representative "demographic".
2) Download and index their tweets

>>> female_gamers = Specs(gender=['female'], age=range(13, 30), keywords=('nintendo', 'game', 'xbox', 'play'))
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

This is a JSON/REST api that adheres to the following url hierarchy and json schemas:

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

GET /demographic/(?P<name>.*)/sync
- Syncs the demographic on the backend (ie dumps the tweets to the database)
- Returns an empty json structure

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

DELETE /demographic/(?P<name>.*)
- Removes the demographic from the database
- Returns empty json structure

GET /question/(?P<label>.*)
- Gets a question
- Returns a json structure with the following format,
{
    label: ...,              # string
    exemplars: [...]         # list of strings (contents of real or hypothetical tweets)
}

POST /question/(?P<label>.*)
- Creates a question
- Returns json, {label: ...}
- Takes a json structure with the following format,
{
    label: ...,              # string
    exemplars: [...]         # list of strings (contents of real or hypothetical tweets)
}

DELETE /question/(?P<label>.*)
- Removes the question from the database
- Returns empty json structure

NOTE: Questions are immutable once created, for simplicity, so there is no PUT method for
      updating an existing question. Rather, delete and create anew (might change in future)

GET /demographic/(?P<name>.*)/poll/(?P<id>.*)
- Gets the results of the corresponding poll
- Returns a json structure of the following format,
{
    id: ...,        # string
    question: ...,  # string (label of the question)
    trend: ...      # string (id of the trend, if any)
}

POST /demographic/(?P<name>.*)/poll
- Polls the demographic
- Returns json, {id: ..., result: ...}, where `id` is the poll id and `result` is a float
- Takes a json structure of the following format,
{
    question: ...,  # string (label of the question)
    trend: ...      # string (id of a trend you'd like to qualify the search with)
}

DELETE /demographic/(?P<name>.*)/poll
- Removes a poll from the database
- Returns empty json structure

Trends are under construction,

GET /trend/(?P<id>.*)
- TBD

POST /trend
- TBD

PUT /trend/(?P<id>.*)
- TBD

DELETE /trend/(?P<id>.*)
- TBD
