'''
实现flask 获取ip

'''

import flask
from myproxypool.redisClient import RedisClient


def redis_con():
    return RedisClient().random()



app = flask.Flask(__name__)


@app.route('/')
def random():
    return redis_con()
