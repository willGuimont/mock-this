import os
import random

from flask import Flask, request, jsonify
import json
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)


def random_case(x: str, p: float):
    return x.upper() if random.uniform(0, 1) <= p else x.lower()


def mockify(s: str, p: float):
    return ''.join(map(lambda x: random_case(x, p), s))


@app.route('/', methods=['POST'])
def index():
    content = request.get_data()
    try:
        json_content = json.loads(content)
    except json.decoder.JSONDecodeError:
        return '400'
    output = {'mock': mockify(json_content['message'], p=0.5)}
    return jsonify(output)


if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run(threaded=True, port=port)
