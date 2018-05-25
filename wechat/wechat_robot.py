import itchat
import requests

#向图灵机器人申请，然后会获得一个 API KEY
key ="f4f4cafaac86464082acebd30b153b94"

def get_response(msg):
    # 构造了要发送给服务器的接口
    #使用图灵机器人提供的接口
    apiUrl = 'http://www.tuling123.com/openapi/api'
    # 一个发动的api的数据
    data={
        'key' :key,
        'info':msg,
        'userid':'wechat-robot'
    }
    try:
        # 使用post方法去请求
        r=requests.post(apiUrl,data=data).json()
        # 字典的get方法在字典没有'text'值的时候会返回None而不会抛出异常
        return r.get('text')
        # 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常
        # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
    except:
        return
# 使用装饰器
@itchat.msg_register(itchat.content.TEXT)
#获取图灵机器人返回的数据
#处理图灵机器人出现异常的时候
def tuling_reply(msg):
    # 为了保证在图灵Key出现问题的时候仍旧可以回复，这里设置一个默认回复
    defaultReply = 'I received: ' + msg['Text']
    # 如果图灵Key出现问题，那么reply将会是None
    reply = get_response(msg['Text'])
    # a or b的意思是，如果a有内容，那么返回a，否则返回b
    # 有内容一般就是指非空或者非None，你可以用`if a: print('True')`来测试
    return reply or defaultReply

# 为了让实验过程更加方便（修改程序不用多次扫码），我们使用热启动
itchat.auto_login(hotReload=True)
itchat.run()
