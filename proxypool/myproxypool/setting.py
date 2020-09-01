

HEADERS ={
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",

}

# 关于代理检测设置
TRAGET_URL = "https://www.bilibili.com/"
BATCH_TEST_SIZE=100


# 参数设置
TESTER_ENABLED=True
GETTER_ENABLED=True
API_ENABLED=True



# 关于redis的设置
MAX_SCORE=100
MIN_SCORE=0
INIT_SCORE= 10
REDIS_HOST='localhost'
REDIS_PORT=6379
REDIS_PASSWORD=''
REDIS_KEY='proxies'