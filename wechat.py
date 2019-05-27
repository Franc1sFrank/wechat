
import itchat
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib as mpl
from wordcloud import WordCloud
from snownlp import SnowNLP
import re
import jieba
from jieba import analyse
import numpy as np
from PIL import Image
import csv
from pyecharts import Map, Geo


def analyseSex(friends):
    sexs = list(map(lambda x: x['Sex'], friends[1:]))
    counts = Counter(sexs).items()
    counts = sorted(counts, key=lambda x: x[0], reverse=False)
    counts = list(map(lambda x: x[1], counts))
    # 0unknown 1male 2female
    labels = ['unknown', 'male', 'female']
    colors = ['yellowgreen', 'darkslateblue', 'orangered']
    plt.figure(figsize=(8, 5), dpi=80)
    plt.axes(aspect=1)
    plt.pie(counts,
            labels=labels,
            colors=colors,
            labeldistance=1.1,
            autopct='%3.1f%%',
            shadow=False,
            startangle=90,
            pctdistance=0.6
            )
    plt.legend(loc='upper right', )
    plt.title(u'%s_friends_sex_ratio ' % friends[0]['NickName'])
    plt.show()


def analyseSignature(friends):
    signatures = ''
    emotions = []
    for friend in friends:
        # get friend's signature
        signature = friend['Signature']
        if signature != None:
            # filter tags and emoji
            signature = signature.strip().replace('span', '').replace('class', '').replace('emoji', '')
            signature = re.sub(r'1f(\d.+)', '', signature)

            if len(signature) > 0:
                # analyze tags
                nlp = SnowNLP(signature)
                # get moods
                emotions.append(nlp.sentiments)
                # jieba
                signatures += ' '.join(jieba.analyse.extract_tags(signature, 5))

    # Sinature WordCloud
    back_coloring = np.array(Image.open('basketball.jpg'))
    wordcloud = WordCloud(
        font_path='arial.ttf',
        background_color="white",
        max_words=1200,
        mask=back_coloring,
        max_font_size=75,
        random_state=45,
        width=960,
        height=720,
        margin=15
    )

    # generate wordcloud
    wordcloud.generate(signatures)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
    wordcloud.to_file('signatures.jpg')

    # Signature Emotional Judgment
    count_good = len(list(filter(lambda x: x > 0.66, emotions)))
    count_normal = len(list(filter(lambda x: 0.33 <= x <= 0.66, emotions)))
    count_bad = len(list(filter(lambda x: x < 0.33, emotions)))
    labels = [u'negative', u'neutral', u'positive']
    values = (count_bad, count_normal, count_good)
    plt.rcParams['font.sans-serif'] = ['simHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.xlabel(u'mood')
    plt.ylabel(u'frequency')
    plt.xticks(range(3), labels)
    plt.legend(loc='upper right', )
    plt.bar(range(3), values, color='rgb')
    plt.title(u'%s_signature_mood' % friends[0]['NickName'])
    plt.show()


def analyseLocation(friends):
    keys = []
    values = []
    province = list(map(lambda x: x['Province'], friends[1:]))

    for i in set(province):
        keys.append(i)
        values.append(province.count(i))

    maps = Map("map_of_china", 'map_of_china', width=1200, height=600)
    maps.add("", keys, values, visual_range=[0, 50], maptype='china', is_visualmap=True,
             visual_text_color='#000')
    maps.show_config()
    maps.render(path="location.html")


if __name__ == '__main__':
    # solve PIL error codes
    mpl.rcParams['font.sans-serif'] = ['arial']
    mpl.rcParams['axes.unicode_minus'] = False
    # login wechat
    itchat.auto_login(hotReload=True)
    friends = itchat.get_friends(update=True)
    print(friends)
    # analyse sex
    analyseSex(friends)
    # analyse signature
    analyseSignature(friends)
    # analyse geo
    analyseLocation(friends)


try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract


import itchat
itchat.login()
itchat.send(u'你好，文件传输助手', 'filehelper')
print(itchat.search_friends(name='Francis_Frank'))