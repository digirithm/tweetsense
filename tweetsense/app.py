from flask import Flask, request
app = Flask(__name__)


@app.route('/demographic', methods=['GET', 'POST'])
def demographic():
    pass


@app.route('/demographic/(?P<name>.*)', methods=['GET', 'PUT', 'DELETE'])
def demographic_by_id(name):
    pass


@app.route('/demographic/(?P<name>.*)/sync', methods=['GET'])
def sync_demographic(name):
    pass


@app.route('/demographic/(?P<name>.*)/clone', methods=['POST'])
def clone_demographic(name):
    pass


@app.route('/demographic/(?P<name>.*)/broaden', methods=['GET'])
def broaden_demographic(name):
    pass


@app.route('/demographic/(?P<name>.*)/sample/(?P<sample_size>.*)', methods=['GET'])
def sample_demographic(name, sample_size):
    pass


@app.route('/demographic/(?P<name>.*)/poll', methods=['GET', 'POST'])
def poll(name):
    pass


@app.route('/demographic/(?P<name>.*)/poll/(?P<id>.*)', methods=['GET'])
def poll_by_id(name, id):
    pass


@app.route('/question', methods=['POST'])
def question():
    pass


@app.route('/question/(?P<label>.*', methods=['GET', 'DELETE'])
def question_by_id(label):
    pass


@app.route('/trend', methods=['GET', 'POST'])
def trend():
    pass