'''
数据来源：http://data.eastmoney.com/zlsj/2020-03-31-1-2.html
'''

import requests
import json
import re
import pymysql
import time
import random


# #设置一个浏览器标识的列表
user_agent_list=['Mozilla/5.0(Windows;U;WindowsNT6.1;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50',
                 'Mozilla/5.0(Macintosh;IntelMacOSX10.6;rv:2.0.1)Gecko/20100101Firefox/4.0.1',
                 'Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTML,likeGecko)Chrome/17.0.963.56Safari/535.11']
#设置一个请求头
headers={
    'User-Agent':random.choice(user_agent_list)
}
class Q1_StocksPositon():

    def __init__(self):
        self.headers = \
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
            }
        self.db = pymysql.connect(host='localhost', user='root', password='zsw123456', port=3306, db='2020_Q1')
        self.start_url = 'http://data.eastmoney.com/zlsj/zlsj_list.aspx?type=ajax&st=2&sr=-1&p={}&ps=50&jsObj=cZlgqOju&stat=1&cmd=1&date=2020-03-31'

    def create_table(self):
        cur = self.db.cursor()
        # sql = "create table if not exists (序号 INT, 股票代码 VARCHAR(255), 股票简称 VARCHAR(255), 持有基金家数 INT," \
        #       "持股总数 FLOAT, 持股市值 FLOAT, 持股变化 VARCHAR(255), 持股变动数值 FLOAT, 持股变动比例 FLOAT)"

        sql = '''create table if not exists Q1_stock_position (序号 INT, 股票代码 VARCHAR(255), 股票简称 VARCHAR(255), 
        持有基金家数（家） INT, 持股总数（万股） FLOAT, 持股市值（亿元） FLOAT, 持股变化 VARCHAR(255), 持股变动数值（万股） FLOAT, 持股变动比例 FLOAT)'''
        cur.execute(sql)
        print('创建表成功')

    def data_processing(self):
        i_list = [i for i in range(1, 35)]
        pattern = '(\[\{.*\])'
        while len(i_list) > 0:
            i = i_list.pop()
            url = self.start_url.format(i)
            print(url)
            response = requests.get(url=url, headers=headers)
            time.sleep(2)
            str = re.search(pattern, response.text)
            if str != None:
                data = json.loads(str.group(1))
                # print(data)
                for items in data:
                    yield items
            else:
                i_list.insert(0, i)


    def insert_data(self):
        cur = self.db.cursor()
        count = 0
        items = self.data_processing()
        sql = 'insert into Q1_stock_position(序号, 股票代码, 股票简称, 持有基金家数（家）, 持股总数（万股）, 持股市值（亿元）, 持股变化, 持股变动数值（万股）, 持股变动比例) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
        for item in items:
            stock_num = item['SCode']                # 股票代码
            stock_name = item['SName']               # 股票民称
            fund_num = item['Count']                 # 持有基金家数
            ShareHDNum = item['ShareHDNum']/10000   # 持股总数（万股）
            VPosition = item['VPosition']/1000000000  # 持股市值
            CGChange = item['CGChange']               # 持股变化
            ShareHDNumChange = item['ShareHDNumChange']/10000   # 持股变动数值
            RateChange = item['RateChange']            # 持股变动比例
            count+=1                                   # 序号
            try:
                self.db.ping(reconnect=True)
                cur.execute(sql, (count, stock_num, stock_name, fund_num, ShareHDNum, VPosition, CGChange, ShareHDNumChange, RateChange))
                self.db.commit()
                print('第{}条插入成功'.format(count))
            except:
                self.db.rollback()
                print('插入失败')

    def run(self):
        self.create_table()
        # self.data_processing()
        self.insert_data()

if __name__ == '__main__':
    Q1 = Q1_StocksPositon()
    Q1.run()
