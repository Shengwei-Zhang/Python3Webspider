import matplotlib.pyplot as plt
import jieba
from wordcloud import WordCloud




def comments_cloud():
    jieba.load_userdict("dict.txt.big.txt")
    with open('comments.text') as f:
        comments_text = " ".join(jieba.cut(f.read()))
        print(comments_text[:100])
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS'] 
    plt.axis("off")
    wordcloud = WordCloud(font_path="/System/Library/fonts/PingFang.ttc",mask = None,).generate(comments_text)
    # wordcloud = WordCloud(mask = None,).generate(comments_text)
    plt.savefig('./词云1.jpg')
    plt.imshow(wordcloud, interpolation='bilinear',)
    
    plt.show()



if __name__ == '__main__':
    comments_cloud()
    