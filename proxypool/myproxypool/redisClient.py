'''
封装 redis的方法
'''
import redis
from myproxypool.setting import *
from random import choice


class PoolEmptyError(ValueError):
    pass

class RedisClient():

    def __init__(self):
        self.db = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)

    def add(self, proxy, score=INIT_SCORE):
        # Add proxy in redis and set it MAX_SCORE

        if not self.db.zscore(REDIS_KEY, proxy):
            return self.db.zadd(REDIS_KEY, {proxy: score})

    def random(self):
        # Get the proxy randomly
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY, 0, 100)
            if len(result):
                return choice(result)
            else:
                raise PoolEmptyError('No Proxy')

    def decrease(self, proxy):

        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            print('代理', proxy, '当前分数', score, '减1')
            return self.db.zincrby(REDIS_KEY, -1, proxy)
        else:
            print('代理', proxy, '当前分数', score, '移除')
            return self.db.zrem(REDIS_KEY, proxy)

    def exists(self, proxy):
        return not self.db.zscore(REDIS_KEY, proxy) == None

    def max(self, proxy):

        print('代理', proxy, '可用，设置为', MAX_SCORE)
        return self.db.zadd(REDIS_KEY, {proxy: MAX_SCORE})

    def count(self):

        return self.db.zcard(REDIS_KEY)

    def all(self):

        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)



