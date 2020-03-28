import os
import random

from flask import Flask, request


def random_case(x: str, p: float):
    return x.upper() if random.uniform(0, 1) <= p else x.lower()


def mockify(s: str, p: float):
    return ''.join(map(lambda x: random_case(x, p), s))


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    content = request.json
    print(content)
    return mockify(content['message'], p=0.5)


if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run(threaded=True, port=port)
