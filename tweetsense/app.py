# Flask specific app runner
from flask import Flask, request
app = Flask(__name__)

# the kitchen sink...
import time
import json
from collections import Sequence
import functools
from tweetsense import Persistable, TwitterUser, Demographic, Question, Poll, Trend


def serialize(handler):
    """
    Auto serialization decorator
    """
    # fake monad
    maybe = lambda x: x.dehydrate() if isinstance(x, Persistable) else x

    @functools.wraps(handler)
    def _wrap(*args, **kwargs):
        data = handler(*args, **kwargs)
        if isinstance(data, Sequence):
            return json.dumps([maybe(x) for x in data if x])
        elif not data:
            return ''
        else:
            return json.dumps(maybe(data))

    return _wrap


@serialize
@app.route('/demographic', methods=['GET', 'POST'])
def demographic():
    if request.method is 'GET':
        # get all demos
        return Demographic.load_object()
    elif request.method is 'POST':
        # create demo
        return Demographic.hydrate(request.data, from_string=True).save()
    else:
        raise NotImplementedError


@serialize
@app.route('/demographic/(?P<name>.*)', methods=['GET', 'PUT', 'DELETE'])
def demographic_by_id(name):
    if request.method is 'GET':
        # get specific demo
        return Demographic.load_object(_id=name)
    elif request.method is 'PUT':
        # update specific demo
        return Demographic.update(name, json.loads(request.data))
    elif request.method is 'DELETE':
        # delete specific demo
        return Demographic.delete_object(_id=name)
    else:
        raise NotImplementedError


@serialize
@app.route('/demographic/(?P<name>.*)/sync', methods=['GET'])
def sync_demographic(name):
    # fire off backend sync
    try:
        Demographic.load_object(_id=name).sync()
        return {'synced': True, 'timestamp': time.asctime()}
    except:
        return {'synced': False, 'timestamp': time.asctime()}


@serialize
@app.route('/demographic/(?P<name>.*)/clone', methods=['POST'])
def clone_demographic(name):
    # clone and rename demo
    clone = Demographic.load_object(_id=name)
    clone.name = json.loads(request.data)['name']
    return clone.save()


@serialize
@app.route('/demographic/(?P<name>.*)/broaden', methods=['GET'])
def broaden_demographic(name):
    # enlarge demo
    demo = Demographic.load_object(_id=name)
    demo.broaden()
    return demo.save()


@serialize
@app.route('/demographic/(?P<name>.*)/sample/(?P<sample_size>.*)', methods=['GET'])
def sample_demographic(name, sample_size):
    # return random sample
    return Demographic.load_object(_id=name).sample(N=sample_size)


@serialize
@app.route('/demographic/(?P<name>.*)/poll', methods=['GET', 'POST'])
def poll(name):
    if request.method is 'GET':
        # get all polls for a demo
        return Poll.load_object(_id=name)
    elif request.method is 'POST':
        # create a poll
        raw_json = json.loads(request.data)
        question = Question.hydrate(raw_json['question'])
        # trend handling is currently absent
        focus_group = Demographic.load_object(_id=name).poll(
                        question=question, weight=request.args.get('weight', False))
        return focus_group.save()
    else:
        raise NotImplementedError


@serialize
@app.route('/demographic/(?P<name>.*)/poll/(?P<id>.*)', methods=['GET'])
def poll_by_id(name, id):
    # load a specific poll
    return Poll.load_object(_id=id)


@serialize
@app.route('/question', methods=['POST'])
def question():
    # create a question
    return Question.hydrate(request.data, from_string=True).save()


@serialize
@app.route('/question/(?P<label>.*', methods=['GET', 'DELETE'])
def question_by_id(label):
    if request.method is 'GET':
        # get a specific question
        return Question.load_object(_id=label)
    elif request.method is 'DELETE':
        # delete a specific question
        return Question.delete_object(_id=label)
    else:
        raise NotImplementedError


@serialize
@app.route('/trend', methods=['GET', 'POST'])
def trend():
    if request.method is 'GET':
        # get all trends
        return Trend.load_object()
    elif request.method is 'POST':
        # create trend
        return Trend.hydrate(request.data, from_string=True).save()
    else:
        raise NotImplementedError