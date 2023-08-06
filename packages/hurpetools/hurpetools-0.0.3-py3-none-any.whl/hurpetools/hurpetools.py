# -*- coding:utf-8 _*-
"""
@author:Hurpe
@file：hurpetools.py
@time: 2018/1/1
@desc：my tools
"""
import logging
import os
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from requests_toolbelt import MultipartEncoder
import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def query(cursor, sql) -> tuple:
    cursor.execute(sql)
    res = cursor.fetchall()
    return res


def action(conn, cursor, sql) -> None:
    cursor.execute(sql)
    conn.commit()


def logclass(name):
    """
    return logger 对象
    可以将日志按照时间和日期保存到当前目录log下
    :param name: app name
    :return:
    """
    logger = logging.getLogger("mainModule")
    logger.setLevel(level=logging.INFO)
    if not os.path.exists('logs'):
        os.mkdir('logs')
    today = time.strftime('%Y%m%d', time.localtime())
    handler = logging.FileHandler('logs/' + name + '_' + today + '.txt', mode='a', delay=False)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s-%(filename)s[%(lineno)d]-%(levelname)s:%(message)s")
    handler.setFormatter(formatter)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    logger.addHandler(handler)
    logger.addHandler(console)
    return logger


def mail(my_sender, my_pass, my_user, subject, filepath, filename):
    """
    :param my_sender: 发件人邮箱账号
    :param my_pass: 发件人邮箱授权码
    :param my_user: 收件人
    :param subject: 邮件的主题，也可以说是标题
    :param filename: 文件名
    :param filepath: 文件绝对路径
    :return: 是否成功，true成功，false失败
    """
    ret = True
    try:
        msg = MIMEMultipart()
        msg['From'] = my_sender  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = ','.join(my_user)  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = subject  #
        msg.attach(MIMEText(" ", 'plain', 'utf-8'))

        # 构造附件1，传送当前目录下文件，附件2同样
        att1 = MIMEText(open(filepath + filename + '.xlsx', 'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
        att1["Content-Disposition"] = 'attachment; filename="'+filename+'.xlsx"'
        msg.attach(att1)

        server = smtplib.SMTP_SSL("smtp.163.net", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, my_user, msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception as e:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
        print("邮件发送有问题，问题原因：%s" % e)
    return ret


def send_file_message_to_wework(agent_id, secret, company_id, filepath, filename, receive):
    """
    发送文件消息到企业微信
    :param agent_id: 企业微信
    :param secret:
    :param company_id:
    :param filepath:
    :param filename:
    :param receive:
    :return:
    """

    url = f'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={company_id}&corpsecret={secret}'
    response = requests.get(url=url, verify=False)
    access_token = response.json().get('access_token')  # 获取access_token, access_token默认两小时失效一次，所以每次发送，重新获取
    """ 上传素材，获取 media_id """
    post_file_url = f"https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={access_token}&type=file"

    # key一定是文件名，value：(文件类型，二进制的文件，文件传输格式)
    m = MultipartEncoder(
        fields={filename: (f'{filename}', open(filepath + filename, 'rb'), 'text/plain')},
    )
    r = requests.post(url=post_file_url, data=m, headers={'Content-Type': m.content_type}, verify=False)
    media_id = json.loads(r.text)['media_id']

    data = {
        "toparty": f"{receive}",  # 向这些用户账户发送
        "msgtype": "file",
        "agentid": agent_id,  # 应用的 id 号
        "file": {
            "media_id": media_id
        },
        "safe": 0
    }
    r = requests.post(url="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}".format(access_token),
                      data=json.dumps(data), verify=False)

    return r.json()


def send_text_message_to_wework(agent_id, secret, company_id, text, receive):
    """
    发送文字消息到企业微信
    :param agent_id:
    :param secret:
    :param company_id:
    :param text:
    :param receive:
    :return:
    """
    url = f'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={company_id}&corpsecret={secret}'
    response = requests.get(url=url, verify=False)

    access_token = response.json().get('access_token')  # 获取access_token, access_token默认两小时失效一次，所以每次发送，重新获取

    data = {
       "toparty": f"{receive}",   # 向这些用户账户发送
       "msgtype": "markdown",
       "agentid": agent_id,   # 应用的 id 号
       "markdown": {
           "content": text
       }
    }
    time.sleep(1)
    r = requests.post(url="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}".format(access_token),
                      data=json.dumps(data), verify=False)

    return r.json()
