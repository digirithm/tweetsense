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



[![MEAN.JS Logo](http://meanjs.org/img/logo-small.png)](http://meanjs.org/)

[![Build Status](https://travis-ci.org/meanjs/mean.svg?branch=master)](https://travis-ci.org/meanjs/mean)
[![Dependencies Status](https://david-dm.org/meanjs/mean.svg)](https://david-dm.org/meanjs/mean)

MEAN.JS is a full-stack JavaScript open-source solution, which provides a solid starting point for [MongoDB](http://www.mongodb.org/), [Node.js](http://www.nodejs.org/), [Express](http://expressjs.com/), and [AngularJS](http://angularjs.org/) based applications. The idea is to solve the common issues with connecting those frameworks, build a robust framework to support daily development needs, and help developers use better practices while working with popular JavaScript components. 

## Before You Begin 
Before you begin we recommend you read about the basic building blocks that assemble a MEAN.JS application: 
* MongoDB - Go through [MongoDB Official Website](http://mongodb.org/) and proceed to their [Official Manual](http://docs.mongodb.org/manual/), which should help you understand NoSQL and MongoDB better.
* Express - The best way to understand express is through its [Official Website](http://expressjs.com/), particularly [The Express Guide](http://expressjs.com/guide.html); you can also go through this [StackOverflow Thread](http://stackoverflow.com/questions/8144214/learning-express-for-node-js) for more resources.
* AngularJS - Angular's [Official Website](http://angularjs.org/) is a great starting point. You can also use [Thinkster Popular Guide](http://www.thinkster.io/), and the [Egghead Videos](https://egghead.io/).
* Node.js - Start by going through [Node.js Official Website](http://nodejs.org/) and this [StackOverflow Thread](http://stackoverflow.com/questions/2353818/how-do-i-get-started-with-node-js), which should get you going with the Node.js platform in no time.


## Prerequisites
Make sure you have installed all these prerequisites on your development machine.
* Node.js - [Download & Install Node.js](http://www.nodejs.org/download/) and the npm package manager, if you encounter any problems, you can also use this [Github Gist](https://gist.github.com/isaacs/579814) to install Node.js.
* MongoDB - [Download & Install MongoDB](http://www.mongodb.org/downloads), and make sure it's running on the default port (27017).
* Bower - You're going to use the [Bower Package Manager](http://bower.io/) to manage your front-end packages, in order to install it make sure you've installed Node.js and npm, then install bower globally using npm:

```
$ npm install -g bower
```

* Grunt - You're going to use the [Grunt Task Runner](http://gruntjs.com/) to automate your development process, in order to install it make sure you've installed Node.js and npm, then install grunt globally using npm:

```
$ sudo npm install -g grunt-cli
```

## Downloading MEAN.JS
There are several ways you can get the MEAN.JS boilerplate: 

### Yo Generator 
The recommended way would be to use the [Official Yo Generator](http://meanjs.org/generator.html) which will generate the latest stable copy of the MEAN.JS boilerplate and supplies multiple sub-generators to ease your daily development cycles.

### Cloning The GitHub Repository
You can also use Git to directly clone the MEAN.JS repository:
```
$ git clone https://github.com/meanjs/mean.git meanjs
```
This will clone the latest version of the MEAN.JS repository to a **meanjs** folder.

### Downloading The Repository Zip File
Another way to use the MEAN.JS boilerplate is to download a zip copy from the [master branch on github](https://github.com/meanjs/mean/archive/master.zip). You can also do this using `wget` command:
```
$ wget https://github.com/meanjs/mean/archive/master.zip -O meanjs.zip; unzip meanjs.zip; rm meanjs.zip
```
Don't forget to rename **mean-master** after your project name.

## Quick Install
Once you've downloaded the boilerplate and installed all the prerequisites, you're just a few steps away from starting to develop you MEAN application.

The first thing you should do is install the Node.js dependencies. The boilerplate comes pre-bundled with a package.json file that contains the list of modules you need to start your application, to learn more about the modules installed visit the NPM & Package.json section.

To install Node.js dependencies you're going to use npm again, in the application folder run this in the command-line:

```
$ npm install
```

This command does a few things:
* First it will install the dependencies needed for the application to run.
* If you're running in a development environment, it will then also install development dependencies needed for testing and running your application.
* Finally, when the install process is over, npm will initiate a bower installcommand to install all the front-end modules needed for the application

## Running Your Application
After the install process is over, you'll be able to run your application using Grunt, just run grunt default task:

```
$ grunt
```

Your application should run on the 3000 port so in your browser just go to [http://localhost:3000](http://localhost:3000)
                            
That's it! your application should be running by now, to proceed with your development check the other sections in this documentation. 
If you encounter any problem try the Troubleshooting section.

## Development and deployment With Docker

* Install [Docker](http://www.docker.com/)
* Install [Fig](https://github.com/orchardup/fig)

* Local development and testing with fig: 
```bash
$ fig up
```

* Local development and testing with just Docker:
```bash
$ docker build -t mean .
$ docker run -p 27017:27017 -d --name db mongo
$ docker run -p 3000:3000 --link db:db_1 mean
$
```

* To enable live reload forward 35729 port and mount /app and /public as volumes:
```bash
$ docker run -p 3000:3000 -p 35729:35729 -v /Users/mdl/workspace/mean-stack/mean/public:/home/mean/public -v /Users/mdl/workspa/mean-stack/mean/app:/home/mean/app --link db:db_1 mean
```

## Getting Started With MEAN.JS
You have your application running but there are a lot of stuff to understand, we recommend you'll go over the [Offical Documentation](http://meanjs.org/docs.html). 
In the docs we'll try to explain both general concepts of MEAN components and give you some guidelines to help you improve your development procees. We tried covering as many aspects as possible, and will keep update it by your request, you can also help us develop the documentation better by checking out the *gh-pages* branch of this repository.

## Community
* Use to [Offical Website](http://meanjs.org) to learn about changes and the roadmap.
* Join #meanjs on freenode.
* Discuss it in the new [Google Group](https://groups.google.com/d/forum/meanjs)
* Ping us on [Twitter](http://twitter.com/meanjsorg) and [Facebook](http://facebook.com/meanjs)

## Live Example
Browse the live MEAN.JS example on [http://meanjs.herokuapp.com](http://meanjs.herokuapp.com).

## Credits
Inspired by the great work of [Madhusudhan Srinivasa](https://github.com/madhums/)
The MEAN name was coined by [Valeri Karpov](http://blog.mongodb.org/post/49262866911/the-mean-stack-mongodb-expressjs-angularjs-and)

## License
(The MIT License)

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
'Software'), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
