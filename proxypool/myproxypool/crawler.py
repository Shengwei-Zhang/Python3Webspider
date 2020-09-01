'''
爬取代理并储存入redis中
'''
import time
import requests
from myproxypool.setting import HEADERS
import re
from lxml import etree
from myproxypool.redisClient import RedisClient

class Crawler():

    def __init__(self):
        self.headers = HEADERS

    def get_html(self, url, headers):

        try:
            data = requests.get(url=url, headers=headers, timeout=10).text
            # print(data)
            return data

        except:

            print("超时！")



    def proxy_89ip(self):
        print("proxy_89ip---正在爬取")
        url = "https://www.89ip.cn/index_{}.html"
        pattern = r"\\t\\t\\t(.*?)\\n?"
        for i in range(1, 6):
            # print("第{}页开始爬取".format(i))
            url = url.format(i)
            response = self.get_html(url, self.headers)
            time.sleep(2)

            if response != None:
                data = etree.HTML(response).xpath("//div[@class='layui-form']//table//tr")

                for item in data[1:]:
                    ip = re.findall(pattern, str(etree.tostring(item, encoding='utf8')))[0]
                    port = re.findall(pattern, str(etree.tostring(item, encoding='utf8')))[1]
                    proxy = ip+":"+port
                    # print(proxy)
                    yield proxy

            else:
                print("89ip获取失败")
                break


    def proxy_66ip(self):
        print("proxy_66ip---正在爬取")
        url = 'http://www.66ip.cn/{}.html'
        pattern = r"d>(.*?)</td>?<td>(.*?)</td>"
        for i in range(1, 20):
            url = url.format(i)
            response = self.get_html(url, self.headers)
            time.sleep(2)
            if response != None:
                data = etree.HTML(response).xpath("//div[@class='container']//table//tr")
                for item in data[1:]:
                    # print(etree.tostring(item))
                    ip = re.search(pattern, str(etree.tostring(item))).group(1)
                    port = re.search(pattern, str(etree.tostring(item))).group(2)
                    # print(type(etree.tostring(item, encoding="utf8")))
                    proxy = ip+":"+port
                    yield proxy
            else:
                print("66ip 获取失败")
                break

    def kuaidaili(self):
        print("快代理正在爬取")
        url = "https://www.kuaidaili.com/free/inha/{}/"
        pattern = r'IP">(.*?)</td>?.*PORT">(.*?)</td>'
        for i in range(2, 6):
            url = url.format(i)
            response = self.get_html(url, self.headers)
            time.sleep(1)
            if response != None:
                data = etree.HTML(response).xpath("//div[@id='list']//table//tr")
                for item in data[1:]:
                    ip = re.search(pattern, str(etree.tostring(item))).group(1)
                    port = re.search(pattern, str(etree.tostring(item))).group(2)
                    proxy = ip + ":" + port
                    # print(proxy)
                    yield proxy
            else:
                print("kuaidaili获取失败")
                break

    def add_proxy(self, **kwargs):
        proxy_66 = self.proxy_66ip()
        proxy_89 = self.proxy_89ip()
        proxy_kuaidaili = self.kuaidaili()

        while True:
            try:
             ip_66 = proxy_66.__next__()
             RedisClient().add(proxy=ip_66)
             print(ip_66,"添加成功")

             ip_89 = proxy_89.__next__()
             RedisClient().add(proxy=ip_89)
             print(ip_89, "添加成功")

             ip_kuaidl = proxy_kuaidaili.__next__()
             RedisClient().add(proxy=ip_kuaidl)
             print(ip_kuaidl, "添加成功")


            except StopIteration:
                break






