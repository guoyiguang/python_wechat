import itchat
import os
import PIL.Image as Image
from os import listdir
import math
itchat.login()
friends = itchat.get_friends(update=True)[0:]
user = friends[0]["UserName"]
os.mkdir(user)
num = 0
# 通过循环获取好友的头像
for i in friends:
	img = itchat.get_head_img(userName=i["UserName"])
	fileImage = open(user + "/" + str(num) + ".jpg",'wb')
	fileImage.write(img)
	fileImage.close()
	num += 1
pics = listdir(user)
numPic = len(pics)
print(numPic)
# 通过好友数量来计算每行和每列要展示的图片数量
eachsize = int(math.sqrt(float(640 * 640) / numPic))
print(eachsize)
numline = int(640 / eachsize)
# 创建一个新的图像
toImage = Image.new('RGB', (618, 657))
print(numline)
x = 0
y = 0
for i in pics:
	try:
		#打开图片
		img = Image.open(user + "/" + i)
	except IOError:
		print("Error: 没有找到文件或读取文件失败")
	else:
		#缩小图片
		img = img.resize((eachsize, eachsize), Image.ANTIALIAS)
		#拼接图片
		toImage.paste(img, (x * eachsize, y * eachsize))
		x += 1
		if x == numline:
			x = 0
			y += 1
toImage.save(user + ".jpg")



