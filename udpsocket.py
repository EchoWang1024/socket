# coding=utf-8

from socket import *

# 1. 创建套接字
udpSocket = socket(AF_INET, SOCK_DGRAM)

# 2. 准备接收方的地址
sendAddr = ('172.21.0.65',8080)

# 3. 从键盘获取数据
sendData = "madezhizhang"

# 4. 发送数据到指定的电脑上
udpSocket.sendto(sendData, sendAddr)

# 5. 关闭套接字
udpSocket.close()