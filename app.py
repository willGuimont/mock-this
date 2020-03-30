import json
import os
import random

import pymongo
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

mongo_user = os.environ['MONGO_USER']
mongo_pwd = os.environ['MONGO_PWD']

client = pymongo.MongoClient(
    f'mongodb+srv://{mongo_user}:{mongo_pwd}@cluster0-svqla.mongodb.net/test?retryWrites=true&w=majority')
db = client.Cluster0
count = db.count


def random_case(x: str, p: float):
    return x.upper() if random.uniform(0, 1) <= p else x.lower()


def mockify(s: str, p: float):
    return ''.join(map(lambda x: random_case(x, p), s))


@app.route('/', methods=['POST'])
def index():
    return mock()


@app.route('/mock', methods=['POST'])
def mock():
    content = request.get_data()
    try:
        json_content = json.loads(content)
    except json.decoder.JSONDecodeError:
        return '400'

    message = json_content.get('message')
    if message is None:
        return '400'

    p = json_content.get('probability_upper', 0.5)
    output = {'mock': mockify(message, p=p)}

    count.update({}, {"$inc": {"count": 1}})

    return jsonify(output)


@app.route('/count', methods=['GET'])
def get_count():
    if count.find_one() is None:
        count.insert_one({'count': 0})
        return jsonify({'count': 0})

    current_count = count.find_one()['count']
    return jsonify({'count': current_count})


if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run(threaded=True, port=port)
