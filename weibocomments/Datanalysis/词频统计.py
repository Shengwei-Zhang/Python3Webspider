import pymysql
import matplotlib.pyplot as plt
import jieba
from wordcloud import WordCloud
from snownlp import SnowNLP
import matplotlib

data = [ ('那边', 11782), ('大家', 11886), ('炸鸡腿', 12414), ('谢谢', 12449), ('他们', 12460),  ('致敬', 12563),('难过', 12648), ('还是', 12958), ('出来', 13480), ('什么', 13941), ('现在', 14358), ('一切', 14382), ('可以', 14584), ('好好', 14683),('疫情', 14963),('伤心', 15093), ('恭喜', 15463), ('微博', 15516), ('回来', 15597), ('自己', 15781), ('世界', 15881), ('起来', 16347),('这个', 17568), ('看看', 18043), ('鲜花', 18694), ('平安', 18983), ('武汉', 19090), ('看到', 19158), ('知道', 20512),('真的', 22111),  ('医生', 23345), ('天堂', 23884), ('一个', 27901), ('走好', 28566),('没有', 31356), ('悲伤', 33555), ('晚安', 36554), ('一定', 41136), ('英雄', 42010), ('今天', 43198), ('希望', 51659), ('我们', 51676), ('早日康复', 56769), ('加油', 72503),('一路走好', 84772), ('李医生', 155835), ('蜡烛', 343040)]


def worlds_cal():
    jieba.load_userdict("/Users/zhangsw/pyproject/dict.txt.big.txt")
    with open('/Users/zhangsw/pyproject/comments.text') as f:
            comments_text = f.read()
    comments_text = " ".join(jieba.cut(comments_text))
    print('*******',type(comments_text))
    # print(comments_text[:100])
    frequency = {}
    for word in comments_text.split(' '):
        if word not in frequency:
            frequency[word] = 1
        else:
            frequency[word] += 1
    data = sorted(frequency.items(), key = lambda kv:kv[1])

    x_list = list()
    y_list = list()
    for y, x in data:
        x_list.append(x)
        y_list.append(y)
    # print(x_list)
    plt.figure(figsize=(10,8))
    ax = plt.gca()
    #去掉边框
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    #移位置 设为原点相交
    # ax.xaxis.set_ticks_position('bottom')
    # ax.spines['bottom'].set_position(('data',0))
    # ax.yaxis.set_ticks_position('left')
    # ax.spines['left'].set_position(('data',0))


    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']        # 解决中文乱码问题
    plt.barh(range(len(x_list)),x_list, height=0.5, color='steelblue', alpha=1)      # 从下往上画
    plt.yticks(range(len(x_list)), y_list, size = "small")  #range(1, len(labels)+1),
    plt.xlim(10000,400000)
    plt.xlabel("词出现次数")
    plt.title("词频统计")
    for x,y in enumerate(x_list):
        plt.text(y, x-0.3, '%s' % y)
    plt.savefig('./词频统计.jpg')
    plt.show()













if __name__ == '__main__':
    worlds_cal()
    

