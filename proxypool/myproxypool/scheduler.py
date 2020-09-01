'''
多进程启动
爬取代理、测试代理、获得可用代理、
'''
from myproxypool.crawler import Crawler

from myproxypool.setting import *
import multiprocessing

from myproxypool.tester import Tester
from myproxypool.api import app




class Scheduler():


    def __init__(self):
        self.crawler = Crawler()
        self.test = Tester()
        self.url = TRAGET_URL
        self.headers = HEADERS
        self.flask_run = app.run




    def run(self):

        p1 = multiprocessing.Process(target=self.crawler.add_proxy)
        p2 = multiprocessing.Process(target=self.test.start)
        p3 = multiprocessing.Process(target=self.flask_run)

        if GETTER_ENABLED:
            p1.start()

        if TESTER_ENABLED:
            p2.start()

        if API_ENABLED:
            p3.start()

