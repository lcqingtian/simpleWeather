#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
import urllib.request as request
import urllib.error as error
import json
import smtplib
from email.mime.text import MIMEText
import schedule
import time
#发送多种类型的邮件
from email.mime.multipart import MIMEMultipart
def my_task():
    # 在这里编写你要执行的任务
    getw()


# 天气预报查询示例
def getw():
    api_url = 'http://apis.juhe.cn/simpleWeather/query'
    params_dict = {
        "city": "西安",  # 查询天气的城市名称，如：北京、苏州、上海
        "key": "",  # 您申请的接口API接口请求Key
    }
    params = urllib.parse.urlencode(params_dict)
    try:
        req = request.Request(api_url, params.encode())
        response = request.urlopen(req)
        content = response.read()
        if content:
            try:
                result = json.loads(content)
                error_code = result['error_code']
                if (error_code == 0):
                    temperature = result['result']['realtime']['temperature']
                    humidity = result['result']['realtime']['humidity']
                    info = result['result']['realtime']['info']
                    wid = result['result']['realtime']['wid']
                    direct = result['result']['realtime']['direct']
                    power = result['result']['realtime']['power']
                    aqi = result['result']['realtime']['aqi']
                    body = "温度：%s\n湿度：%s\n天气：%s\n天气标识：%s\n风向：%s\n风力：%s\n空气质量：%s" % (
                        temperature, humidity, info, wid, direct, power, aqi)
                    print("温度：%s\n湿度：%s\n天气：%s\n天气标识：%s\n风向：%s\n风力：%s\n空气质量：%s" % (
                        temperature, humidity, info, wid, direct, power, aqi))
                    # 发送多种类型的邮件
                    msg_from = ''  # 发送方邮箱
                    passwd = ''  # 就是上面的授权码

                    to = ['']  # 接受方邮箱

                    # 设置邮件内容
                    # MIMEMultipart类可以放任何内容
                    msg = MIMEMultipart()
                    conntent = body
                    # 把内容加进去
                    msg.attach(MIMEText(conntent, 'plain', 'utf-8'))

                    # 设置邮件主题
                    msg['Subject'] = "今日天气"

                    # 发送方信息
                    msg['From'] = msg_from

                    # 开始发送

                    # 通过SSL方式发送，服务器地址和端口
                    s = smtplib.SMTP_SSL("smtp.qq.com", 465)
                    # 登录邮箱
                    s.login(msg_from, passwd)
                    # 开始发送
                    s.sendmail(msg_from, to, msg.as_string())
                    print("邮件发送成功")
                else:
                    print("请求失败:%s %s" % (result['error_code'], result['reason']))
            except Exception as e:
                print("解析结果异常：%s" % e)
        else:
            # 可能网络异常等问题，无法获取返回内容，请求异常
            print("请求异常")
    except error.HTTPError as err:
        print(err)
    except error.URLError as err:
        # 其他异常
        print(err)


if __name__ == '__main__':
    # 设置定时任务
    schedule.every().days.at("07:00").do(my_task)
    # 无限循环执行定时任务
    while True:
        schedule.run_pending()
        time.sleep(1)
