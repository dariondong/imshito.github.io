import poplib
import base64
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import time

def get_email_content():
    useraccount = 'm14718118006@163.com'
    password = 'URENMUWNEUURRFMW'
    # 邮件服务器地址,以下为网易邮箱
    pop3_server = 'pop.163.com'
    # 开始连接到服务器
    server = poplib.POP3(pop3_server)

    # 打开或者关闭调试信息，为打开，会在控制台打印客户端与服务器的交互信息
    server.set_debuglevel(1)

    # 打印POP3服务器的欢迎文字，验证是否正确连接到了邮件服务器
    print(server.getwelcome().decode('utf8'))

    # 开始进行身份验证
    server.user(useraccount)
    server.pass_(password)

    # 返回邮件总数目和占用服务器的空间大小（字节数）， 通过stat()方法即可
    email_num, email_size = server.stat()
    print("消息的数量: {0}, 消息的总大小: {1}".format(email_num, email_size))

    # 使用list()返回所有邮件的编号，默认为字节类型的串
    rsp, msg_list, rsp_siz = server.list()
    print("服务器的响应: {0},\n消息列表： {1},\n返回消息的大小： {2}".format(rsp, msg_list, rsp_siz))

    print('邮件总数： {}'.format(len(msg_list)))

    # 下面单纯获取最新的一封邮件
    total_mail_numbers = len(msg_list)
    rsp, msglines, msgsiz = server.retr(total_mail_numbers)
    print("服务器的响应: {0},\n原始邮件内容： {1},\n该封邮件所占字节大小： {2}".format(rsp, msglines, msgsiz))
    msg_content = b'\r\n'.join(msglines).decode('gbk')

    msg = Parser().parsestr(text=msg_content)
    print('解码后的邮件信息:\n{}'.format(msg))

    # 关闭与服务器的连接，释放资源
    server.close()

    return msg
import quopri
global oldmsg
import os

import re

def batch_rename(file_dir, old_ext, new_ext):
    list_file = os.listdir(file_dir) # 返回指定目录
    for file in list_file:
        ext = os.path.splitext(file) # 返回文件名和后缀
        if old_ext == ext[1]:   # ext[1]是.doc,ext[0]是1
            newfile = ext[0] + new_ext
            os.rename(os.path.join(file_dir, file),
                      os.path.join(file_dir, newfile))


import webbrowser
oldmsg = ["", "", "", "", ""]
def main():
    global oldmsg

    msg=get_email_content()
    print("文件：{}".format(msg))
    msg=str(msg)[(str(msg).index('Content-Transfer-Encoding: quoted-printable')+45):(str(msg).index('Email sent via EmailJS.com')-2)]
    print("内容文件：{}".format(msg))
    # 正文信息是被base64编码后的串，需要获取编码格式进行解码
    utf8msg=quopri.decodestring(msg, header=False)
    print("utf8文件：{}".format(utf8msg))
    cnmsg=utf8msg.decode('utf8')
    print(cnmsg)
    cnmsg= cnmsg.split("，")
    print(cnmsg[0])
    if str(cnmsg[0])!='tie':
        print("不属于tie")
        exit()
    print("标题："+str(cnmsg[1]))
    print("内容："+str(cnmsg[2]))
    print("用户："+str(cnmsg[3]))
    print("时间："+str(cnmsg[4]))
    if oldmsg==cnmsg:
        print("重复了")
        old=True
    else:
        print("新的")
        old=False
    oldmsg=cnmsg
    if old!=True:
        batch_rename("./", ".html", ".txt")
        wedpage=open("tieba.txt","a+",encoding='utf-8')
        html='''
        <div style="width: 90%;background-color: white; margin: 20px auto;height: 200px;" class="wow bounceInUp" >
            <div style="width: 90%;margin: 50px auto;">
                <h1 style="margin-top: 30px;"><strong>{}</strong></h1>
                <p>{}</p>
                <div style="text-align: right;">
                    <p>{}</p>
                    <p>{}</p>
                </div>
            </div>
        </div>
        <!--tiezhi-->'''.format(cnmsg[1],cnmsg[2],cnmsg[3],cnmsg[4])

        htmlpage= wedpage.read()
        print(htmlpage)
        wedpage.write(html)
        wedpage.close()
        batch_rename("./", ".txt", ".html")
        print(htmlpage)


    f=open('log.log',"a")
    f.write(str(cnmsg)+"\n"+"是否重复："+str(old)+"\n")






miao=30
while True:
    main()
    while True:
        time.sleep(1)
        miao=miao-1
        if miao==0:
            miao=30
            break
        else:
            print( "\b"*8+"将在{}秒后索取".format(miao),end="")
