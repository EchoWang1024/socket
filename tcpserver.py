# coding=utf-8
import subprocess
import urllib
import os
import time
import requests
from socket import *


def pid_tomcat():
    child = subprocess.Popen(['pgrep', '-f', "tomcat"], stdout=subprocess.PIPE, shell=False)
    response = child.communicate()[0]
    tomcat = [int(pid) for pid in response.split()]
    return tomcat


def simulation_login(warpath, warname, afterurl):
    login_validurl = "http://192.168.128.58:8080/j_acegi_security_check"
    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
               "Accept-Encoding": "gzip, deflate",
               "Accept-Language": "zh-CN,zh;q=0.9",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64)"
                             " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}
    data = {
        "j_username": "wangliming",
        "j_password": "pachira123",
        "form": "/",
        "json": '{"j_username": "wangliming", "j_password": "pachira123", "remember_me": false, "from": "/"}',
        "Submit": "登录"
    }
    s = requests.session()
    login = s.post(login_validurl, data=data, headers=headers)
    response = s.get(afterurl, cookies=login.cookies, headers=headers)
    with open(warpath + warname, "wb") as code:
        code.write(response.content)
    print warname + " download over!!!"

if __name__ == "__main__":
    tcpserver = socket(AF_INET, SOCK_STREAM)
    # 本地信息绑定
    tcpserver.bind(("192.168.128.57", 7788))
    # 进行监听
    tcpserver.listen(1)
    # 客户端接受
    while True:
        print "持续监听中..."
        newsocket, clientaddr = tcpserver.accept()
        recdata = newsocket.recv(1024)
        recdata = eval(recdata)
        print "接收到的数据为:" + str(recdata)
        while True:
            pid = pid_tomcat()
            try:
                tomcat_pid = pid[0]
                os.system("kill -9 " + str(tomcat_pid))
            except:
                break
            print("获取到的tomcat的pid为" + str(tomcat_pid))

        # 下载新的war包
        war_path = '/opt/Tomcat7_nlu/webapps/'
        for key in recdata:
            url = recdata[key]
            war_name = (url.split("/")[-1]).split("-")[0]
            if ".war" in war_name:
                pass
            else:
                war_name += ".war"
            will_del = war_name.split(".")[0]
            # 删除掉旧的war包和文件夹
            os.system("rm -rf /opt/Tomcat7_nlu/webapps/" + will_del + "*")
            # 下载新的war包
            simulation_login(war_path, war_name, url)
        # 启动tomcat
        os.system("/opt/Tomcat7_nlu/bin/startup.sh")
        time.sleep(250)
        # 操作完成后,给客户端返回信息,让客户端继续执行
        newsocket.send("server has been restart!!!")
        newsocket.close()
