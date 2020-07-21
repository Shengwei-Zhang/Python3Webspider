import matplotlib.pyplot as plt
import jieba
from snownlp import SnowNLP
import requests
import seaborn as sns
import numpy as np
from random import choice



def emotion_data():
    posi = 0
    nega = 0
    count = 0
    with open('comments.text') as f:
            comments_text = f.read().split("\n")
    # print(type(comments_text))
    # print(comments_text[:100])
    data = data_process(comments_text)
    data_li = list()
    print(comments_text.count(" "))
    for item in data:
        count +=1
        if item == '' or item == None:
            continue
        else:
            data_li.append(SnowNLP(item).sentiments)
            if SnowNLP(item).sentiments>=0.6:
                posi+=1
            else:
                nega+=1
            # print(type(SnowNLP(item).sentiments))
        print('\r'+"-"*int(count*100/len(data))+">"+'已完成分析%.2f %%'%(count*100/len(data)), end=' ')
    print("")
    return data_li, posi, nega

def data_process(data):
    random_data = list()
    for i in range(20000):
        random_data.append(choice(data))
    return random_data


def data_show():
    # plt.figure(figsize=(6,6))
    data, posi, nega = emotion_data()
    ax = plt.gca()
   
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']        # 解决中文乱码问题
    plt.title("评论情感分布饼状图")
    labels = ["positive","negative"]
    plt.pie([posi,nega],autopct = '%3.2f%%', pctdistance = 0.6, labels=labels)
    plt.savefig("./评论情感分布饼状图.jpg")
    plt.show()

if __name__ == '__main__':
    # emotion_data()
    data_show()

    