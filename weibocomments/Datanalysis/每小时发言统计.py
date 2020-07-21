import pymysql
import matplotlib.pyplot as plt
import jieba
from wordcloud import WordCloud
from snownlp import SnowNLP



def data_fetch():
    db = pymysql.connect(host='localhost', user='root', password='your ped', port=3306, db='your db')
    cur = db.cursor()
    sql = 'select * from LWLweiboComments'
    cur.execute(sql)
    data = cur.fetchall()
    return data

def comments_per_hour():
    data = data_fetch()
    
    a = lambda h,m:h+m/60
    time_list = [a(h=int(item[1][11:13]),m=int(item[1][14:16])) for item in data]
    # print(time_list[:10])
    # print(len(time_list))
    # plt.xlim(datetime(2008,1,1), datetime(2010,12,31))　　
    # plt.ylim(0,300)
    # s1 = Series(time_list)
    # s1.plot(kind='kde')
    ax = plt.gca()
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']        # 解决中文乱码问题
    #去掉边框
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    #移位置 设为原点相交
    ax.xaxis.set_ticks_position('bottom')
    ax.spines['bottom'].set_position(('data',0))
    ax.yaxis.set_ticks_position('left')
    ax.spines['left'].set_position(('data',0))
    plt.hist(time_list, bins=24,range=(0,24), density=True,facecolor="blue", edgecolor="black", alpha=0.7)
    
    plt.title('评论时间分布')
    plt.xlabel('时间')
    plt.ylabel('频率')
    plt.savefig('./评论时间分布.jpg')
    plt.show()


if __name__ == '__main__':
    comments_per_hour()
    