#import WordCloud as WordCloud
import itchat
import re
import io
from os import path
from wordcloud import WordCloud, ImageColorGenerator
import jieba
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import colors
import random
import os
from matplotlib import pyplot as plt
from wxpy import *
from pyecharts import Map
# 好友性别分析，使用饼状图来显示
def draw(datas):
    l =[]
    for key in datas.keys():
        l.append(datas[key])
    # 定义饼图的标签
    names = ['male','female','unkonw']
    # 模拟饼图数值
    num = [134, 93, 6]
    # 第二块离开圆心0.06
    exp =[0,0.06,0]
    fig = plt.figure()
    plt.pie(l,explode=exp,labels=names,autopct='%1.2f%%')
    # 设置标签格式
    plt.title('Gedeon\'s sex analyze', bbox={'facecolor': '0.8', 'pad': 5})
    plt.show()

# 爬取好友性别信息，并输出比列
def parse_friedns():
    itchat.login()
    text = dict()
    # 获取所有的好友信息
    friedns = itchat.get_friends(update=True)[0:]
    print(friedns)
    male = "male"
    female = "female"
    other = "other"
    # 其中 标志位为1表示为男，标志位为2表示女。还有未知的。。。
    for i in friedns[1:]:
        sex = i['Sex']
        if sex == 1:
            text[male] = text.get(male, 0) + 1
        elif sex == 2:
            text[female] = text.get(female, 0) + 1
        else:
            text[other] = text.get(other, 0) + 1
    total = len(friedns[1:])
    print("男性好友： %.2f%%" % (float(text[male]) / total * 100) + "\n" +
          "女性好友： %.2f%%" % (float(text[female]) / total * 100) + "\n" +

          "不明性别好友： %.2f%%" % (float(text[other]) / total * 100))
    print(text,"=========================")
    draw(text)
# 爬取好友个性签名
def parse_signature():
    itchat.login()
    siglist = []
    friedns = itchat.get_friends(update=True)[1:]
    for i in friedns:
        signature = i["Signature"].strip().replace("span", "").replace("class", "").replace("emoji", "")
        rep = re.compile("1f\d+\w*|[<>/=]")
        signature = rep.sub("", signature)
        siglist.append(signature)
    text = "".join(siglist)
    with io.open('text.txt', 'a', encoding='utf-8') as f:
        wordlist = jieba.cut(text, cut_all=True)
        word_space_split = " ".join(wordlist)
        f.write(word_space_split)
        f.close()

#根据爬取的好友个性签名绘制词云
def draw_signature():
    text = open(u'text.txt', encoding='utf-8').read()
    coloring = np.array(Image.open('shade.jpg'))
    coloring2 = np.array(Image.open('7.png'))
    my_wordcloud = WordCloud(background_color="black",
                         mask=coloring, max_font_size=60, random_state=42, scale=2,
                         font_path="simhei.ttf").generate(text)
    image_colors = ImageColorGenerator(coloring)
    # plt.imshow(my_wordcloud.recolor(color_func=image_colors))
    plt.imshow(my_wordcloud)
    plt.axis("off")
    plt.savefig("demo.jpg",dpi=200)
    plt.show()
def map():
    #爬取好友地域分析，并使用地图格式来显示

    # 使用一个字典统计各省好友数量
    province_dict = {'北京': 0, '上海': 0, '天津': 0, '重庆': 0,
        '河北': 0, '山西': 0, '吉林': 0, '辽宁': 0, '黑龙江': 0,
        '陕西': 0, '甘肃': 0, '青海': 0, '山东': 0, '福建': 0,
        '浙江': 0, '台湾': 0, '河南': 0, '湖北': 0, '湖南': 0,
        '江西': 0, '江苏': 0, '安徽': 0, '广东': 0, '海南': 0,
        '四川': 0, '贵州': 0, '云南': 0,
        '内蒙古': 0, '新疆': 0, '宁夏': 0, '广西': 0, '西藏': 0,
        '香港': 0, '澳门': 0}

    # 统计省份
    bot = Bot()
    my_friends = bot.friends()
    for friend in my_friends:
        if friend.province in province_dict.keys():
            province_dict[friend.province] += 1

    # 为了方便数据的呈现，生成JSON Array格式数据
    data = []
    for key, value in province_dict.items():
        data.append({'name': key, 'value': value})

    print(data)



if __name__ == '__main__':
    map()
    # 分析好友性别 并且调用draw方法，绘制饼图
    #parse_friedns()

    # 获取好有个性签名
    #parse_signatuwxImage.pyre()

    # 绘制云图
    # draw_signature()