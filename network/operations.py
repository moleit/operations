# -*- conding=utf-8 -*-

#导入包
import telnetlib
import time
import datetime

#获取当前时间
now = datetime.datetime.now()

#获取host地址，用户名以及密码
host = input("请输入需要备份配置的主机IP地址（仅支持Telnet方式）：")
username = input("请输入用户名:")
telpassword = input("请输入telnet密码:")
enpassword = input("请输入enable密码:")
flag = True
#保存配置文件字符串
output = ""
#日志文件名称
filename = "{0}_{1}-{2}-{3}_{4}-{5}-{6}.log".format(host, now.year, now.month, now.day, now.hour,
                                                        now.minute, now.second)
#创建telnet连接对象
tel = telnetlib.Telnet(host)
#开启调试模式
#tel.set_debuglevel(2)

data = tel.read_until(b"Username:")
tel.write(username.encode() + b'\n')
data = tel.read_until(b"Password:")
tel.write(telpassword.encode() + b'\n')
data = tel.read_until(b"PCJYJ_RG-EG2000XE>")
tel.write("enable".encode() +  b'\n')
data = tel.read_until(b"Password:")
tel.write(enpassword.encode() + b'\n')
data = tel.read_until(b"PCJYJ_RG-EG2000XE#")
tel.write("show run".encode() + b'\n')
print("登录设备成功")
print("开始备份文件")
try:
    while flag:
        data = tel.read_until(b" --More-- ",1)
        if data.endswith(b" --More-- "):
            output += data.decode('GBK').strip(" --More-- ")
            for i in range(1):
                tel.write(" ".encode())
                time.sleep(0.1)
        else:
            output += data.decode('GBK')
            tel.write(b'\r\n')
            flag = False
except Exception as e:
    print(e)
print("正在将配置备份写入到文件中：" + filename)
#将配置文件保存在文件中
fp = open(filename, "w")
fp.write(output)
fp.close()
print("备份完成，备份文件名为：" + filename )