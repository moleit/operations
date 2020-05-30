# -*- conding=utf-8 -*-

#导入包
import telnetlib
import time
import datetime

#获取当前时间
now = datetime.datetime.now()

#获取host地址
host = input("请输入需要备份配置的主机IP地址（仅支持Telnet方式）：")

#循环获取运行配置文件内容是否继续循环的标志
flag = True
#保存配置文件字符串
output = ""
pp = ""

#日志文件名称
filename = "{0}_{1}-{2}-{3}_{4}-{5}-{6}.log".format(host, now.year, now.month, now.day, now.hour,
                                                        now.minute, now.second)
#创建telnet连接对象
tel = telnetlib.Telnet(host)
#开启调试模式
tel.set_debuglevel(2)


#判断程序是否正确连连接
if tel:
    data = tel.read_until(b"Username:")
    #获取telnet密码
    username = input("连接目标主机成功,请输入登陆用户名:")
    tel.write(username.encode() + b'\n')
    data = tel.read_until(b"Password:")


#判断用户名是否正确
if ("Password:" in data.decode()):
    telpassword = input("请输入telnet密码:")
    tel.write(telpassword.encode() + b'\n')
    data = tel.read_very_eager()
else:
    print("您输入的用户名错误，请重新运行程序！")
    exit()

#判断telnet是否成功
if ("Password:" in data.decode()):
    print("您输入的用户名或者密码错误，请重新运行程序！")
    exit()
else:
    # 获取enable密码
    enpassword = input("请输入enable密码:")
    tel.write("enable".encode() + b'\n')
    data = tel.read_until(b"Password:")
    tel.write(enpassword.encode() + b'\n')
    data = tel.read_very_eager()

#判断enable密码是否正确
if ("Password:" in data.decode()):
    print("您输入的enable密码错误，请重新运行程序！")
    exit()
else:
    print("登录设备成功")
    print("正在执行查询运行时配置文件!")
    tel.write("show run".encode() + b'\n')


print("开始备份文件,请您稍等")

#判断返回结果是否完整，否则循环获取内容
try:
    #如果该内容有错误，就返回错误内容
    while flag:
        data = tel.read_until(b" --More-- ",1)
        #判断是否为“ --More-- ”结尾，如果是就输入空格继续获取结果。否则退出循环
        if data.endswith(b" --More-- "):
            #去掉“ --More-- ”后将返回结果保存在output中
            #以GBK编码显示
            output += data.decode('GBK').strip(" --More-- ")
            for i in range(1):
                #输入空格继续获取配置信息
                tel.write(" ".encode())
                time.sleep(0.1)
        else:
            output += data.decode('GBK')
            tel.write(b'\r\n')
            flag = False
except Exception as e:
    print(e)
print("正在将配置备份写入到文件中：" + filename)


#删除配置文件中多余的空行
for line in output.splitlines():
    #如果该行字符串长度不为零，保存到写入文件的字符串中
    if len(line) != 0:
        pp = pp + line + "\n"



#将配置文件保存在文件中
fp = open(filename, "w")
fp.write(pp)
fp.close()
print("备份完成，备份文件名为：" + filename)
tel.close()