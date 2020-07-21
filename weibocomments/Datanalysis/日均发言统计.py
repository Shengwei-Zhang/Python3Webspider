import pymysql
import matplotlib.pyplot as plt
import jieba
from wordcloud import WordCloud
from snownlp import SnowNLP


def data_fetch():
    db = pymysql.connect(host='localhost', user='root', password='your pwd', port=3306, db='your db')
    cur = db.cursor()
    sql = 'select * from LWLweiboComments'
    cur.execute(sql)
    data = cur.fetchall()
    return data

def comments_per_day():
    data = data_fetch()

    day_list = [item[1][4:10] for item in data]
    # print(day_list[-1])
    single_data = day_dataprocess(day_list)
    # print(single_data[1])

    # print(single_data[-1])
    data_list = list()
    for item in single_data:
        data_list.append((item, day_list.count(item)))
    data_list.reverse()
    print(data_list[:10])
    x_list = list()
    y_list = list()
    for x, y in data_list:
        # print(x)
        # print(y)
        x_list.append(x)
        y_list.append(y)
    print(len(x_list))
    print(len(y_list))
    
    plt.figure(figsize=(20,6))
    ax = plt.gca()

    #去掉边框
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    #移位置 设为原点相交
    ax.xaxis.set_ticks_position('bottom')
    ax.spines['bottom'].set_position(('data',0))
    ax.yaxis.set_ticks_position('left')
    ax.spines['left'].set_position(('data',0))
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']        # 解决中文乱码问题
    plt.plot(x_list,y_list)
    plt.xticks(x_list[::8])
    plt.title('每天的评论数')
    plt.xlabel('日期')
    plt.ylabel('评论数')
    plt.savefig('./每天的评论数.jpg')    
    plt.show()

def day_dataprocess(data):
    result = list()
    for item in data:
        if item not in result:
            result.append(item)
    return result

if __name__ == '__main__':
    comments_per_day()
    
