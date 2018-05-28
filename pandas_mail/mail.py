import smtplib
import os
from email.mime.text import MIMEText
from email.header import Header
import pymysql
from pandas import Series,DataFrame
import time
import pandas as pd
import plotly.plotly as pl
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import datetime

# 数据库ip地址
host="192.168.115.105"
# 数据库名称
db = "news_manage_test"
# 登陆用户名
user="root"
# 登陆密码
password="Hik12345+"
# 获取上一天日期
today = datetime.date.today()
oneday = datetime.timedelta(days=1)
yesterday = today-oneday
print (yesterday)
# 链接数据库
db = pymysql.connect(host,user,password,db,port=3306)
# 使用cursor()的方法获取游标
cur=db.cursor()
# 编写sql查询数据
#sql="SELECT channel,idx_value,stat_date FROM `news_app_analysis` WHERE  DATE_FORMAT(stat_date,'%Y-%m-%d')='2018-05-22' and idx_group='channel'"
sql="SELECT channel,idx_value,stat_date FROM `news_app_analysis` WHERE  DATE_FORMAT(stat_date,'%%Y-%%m-%%d')='%s' and idx_group='channel'"%yesterday
cur.execute(sql) # 执行sql语句
results = cur.fetchall() # 获取所有输出结果

print(results)
df = pd.DataFrame([ij for ij in i] for i in results)
df.rename(columns={0:'Channel_name',1:'Channel_num',2:'date'},inplace=True)
# 取值的 ‘Channel_num’ 列
channel_num = df['Channel_num']
channel_name = df['Channel_name']

# 构造一个空的列表
dt = []
# 将df2的值转换成列表，但是值的类型是字符串。
channel_num_2 = channel_num.values.tolist()
# 将字符串类型值转换为int类型
for i in channel_num_2:
    j = int(i)
    dt.append(j)
lenth = len(dt)

s = pd.Series(dt, index=channel_name)
s.plot(kind='bar')

# 存储为图片
plt.savefig("examples.jpg")
plt.show()
sub = "test"
# d为表格内容
d = ''
for i in range(len(df)):
    d=d+"""
    <tr>
        <td>"""+str(df.index[i])+"""</td>
        <td>""" + str(df.iloc[i][0]) + """</td>
        <td width="60" align="center">""" + str(df.iloc[i][1]) + """</td>
        <td width="75">""" + str(df.iloc[i][2]) + """</td>
    </tr>"""

# web页面内容
html="""\
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<body>
<div id="container" style=center>
<p><h2>展现每日新增用户各个渠道下载数目</h2></p>
<div id="content">
 <table width="60%" border="2" bordercolor="black" cellspacing="0" cellpadding="1">
<tr>
  <td width="40"><strong>排序</strong></td>
  <td width="50"><strong>渠道名称</strong></td>
  <td width="60" align="center"><strong>下载数目</strong></td>
  <td width="50"><strong>日期</strong></td>
</tr>""""""
</table>
</div>
</div>
</div>
<img src="cid:image1"/>
</body>
</html>
    """


# # 第三方 SMTP 服务
mail_host = "smtp.edspay.com"  # 设置服务器
mail_user = "guoyiguang@edspay.com"  # 用户名
mail_pass = "aladin#2018"  # 口令
sender = 'guoyiguang@edspay.com'
receivers = ['827267162@qq.com','17530152552@163.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
# 定义邮件内容
msgRoot = MIMEMultipart('related')
# 指定图片为当前目录
msgRoot['From'] ='guoyiguang@edspay.com'
msgRoot['To'] = '827267162@qq.com'
subject = 'Python SMTP 邮件测试'
msgRoot['Subject'] = Header(subject, 'utf-8')
msgAlternative = MIMEMultipart('alternative')
msgRoot.attach(msgAlternative)
msgAlternative.attach(MIMEText(html, 'html', 'utf-8'))
fp = open('examples.jpg', 'rb')
msgImage = MIMEImage(fp.read())
fp.close()
# 定义图片 ID，在 HTML 文本中引用
msgImage.add_header('Content-ID', '<image1>')
msgRoot.attach(msgImage)
smtpObj = smtplib.SMTP()
smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
smtpObj.login(mail_user, mail_pass)
smtpObj.sendmail(sender, receivers, msgRoot.as_string())
print("邮件发送成功")
