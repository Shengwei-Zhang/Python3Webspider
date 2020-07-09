import requests
import time 
import json
import pymysql
import re
import random
from setting import headers, start_url, next_url


class WeiboCommentSpider():

    def __init__(self):
        self.headers = headers
        self.start_url = start_url
        self.next_url = next_url
        self.db = pymysql.connect(host='localhost', user='root', password='you psw', port=3306, db='your db')
        self.continue_url = start_url
        self.count = 0

    def get_data(self,url):
        for trytime in range(3):
            try:
                response = requests.get(url=url, headers=self.headers,timeout=5)
                data = json.loads(response.text)
                # print(data)
                if response.status_code == 200:
                    break
            except:
                print('超时')

        if trytime == 2:
            print('连续3次超时')
            return 
        
        if data['ok'] == 0:
            print("获取到的数据data['ok']=", 0)
            return

        elif data['ok'] == 1:
            max_id = data.get("data").get("max_id")
            comments = data.get('data').get('data')
            for item in comments:
                ''' 获取内容creattime；floor——number；text；userid；screen——name；'''
                self.count+=1
                create_time = item['created_at']
                floor_number = item['floor_number']
                text = ''.join(re.findall('[\u4e00-\u9fa5]',item['text']))    #item['text']
                userid = item.get('user')['id']
                screen_name = item.get('user')['screen_name']
                cur = self.db.cursor()
                sql = '''insert into LWLweiboComments (序号, 评论时间, 用户ID, 用户昵称, 楼层, 评论内容) values (%s, %s, %s, %s, %s, %s)'''
                try:
                    self.db.ping(reconnect=True)
                    cur.execute(sql, (self.count, create_time, userid, screen_name, floor_number, text))
                    self.db.commit()
                    print('第{}条插入成功'.format(self.count))
                except:
                    self.db.rollback()
                    print('插入失败')
            self.continue_url = self.next_url.format(str(max_id))
            print(self.continue_url)
            time.sleep(random.random())
            self.get_data(self.continue_url)
        return
        
    def create_table(self):
        cur = self.db.cursor()
        sql = '''create table if not exists LWLweiboComments (序号 BIGINT, 评论时间 VARCHAR(255), 用户ID BIGINT, 用户昵称 VARCHAR(255), 楼层 INT, 评论内容 TEXT)'''
        cur.execute(sql)

    def run(self):
        self.create_table()
        while True:
            self.get_data(self.continue_url)
            self.count = self.count
            print(self.count)
            print('休息一下啊')
            time.sleep(random.random()*300)
                       
if __name__ == "__main__":
    weibospider = WeiboCommentSpider()
    weibospider.run()
