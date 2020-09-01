
import asyncio
import aiohttp
from myproxypool.redisClient import RedisClient
from myproxypool.setting import *
import time

class Tester():

    def __init__(self):
        self.url = TRAGET_URL
        self.redis = RedisClient()
        self.headers = HEADERS




    async def test(self, proxy):
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn, headers=self.headers) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                print('正在测试', proxy)
                async with session.get(self.url, proxy=real_proxy, timeout=15) as response:
                    if response.status == 200:
                        self.redis.max(proxy)
                        print('代理可用', proxy)
                    else:
                        self.redis.decrease(proxy)
                        print('请求码响应不合法', proxy)
            except:  # ClientError,ClientConnectorError,
                self.redis.decrease(proxy)
                print('代理请求失败', proxy)

    def start(self):
        # 测试主函数

        print('测试器开始运行')
        try:
            proxies = self.redis.all()
            loop = asyncio.get_event_loop()
            # 批量测试
            for i in range(0, len(proxies), BATCH_TEST_SIZE):
                test_proxies = proxies[i:i + BATCH_TEST_SIZE]
                tasks = [self.test(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(5)
        except Exception as e:
            print('测试器发生错误', e.args)
