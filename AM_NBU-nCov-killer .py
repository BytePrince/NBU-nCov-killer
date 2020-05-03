# -*- coding: utf-8 -*-
import requests
import time
import json
import random
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
from time import strftime, localtime
from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError
import smtplib
import sys
from email.header import Header
from email.mime.text import MIMEText


#邮件配置
mail_host = "********"     
mail_user = "********"         
mail_pass = "********" 
sender = "********@163.com"    

def sendEmail_for_success():
    message = MIMEText("尊敬的主人您好，早晨打卡已经为您完成！", 'plain', 'utf-8')  
    message['From'] = "{}".format("********@163.com")
    message['To'] = "********@163.com"
    message['Subject'] = "打卡成功提醒"
 
    try:
        smtpObj = smtplib.SMTP_SSL("smtp.163.com", 465)  
        smtpObj.login("PwnerZhang", "********")  
        smtpObj.sendmail("********@163.com","********@163.com", message.as_string())  
        print("mail has been send successfully.")
    except smtplib.SMTPException as e:
        print(e)

def sendEmail_for_failure():
    message = MIMEText("尊敬的主人您好，打卡服务异常，请您上线检查！", 'plain', 'utf-8')  
    message['From'] = "{}".format("********@163.com")
    message['To'] = "********@163.com"
    message['Subject'] = "服务异常警告"
 
    try:
        smtpObj = smtplib.SMTP_SSL("smtp.163.com", 465)  
        smtpObj.login("PwnerZhang", "********")  
        smtpObj.sendmail("********@163.com","********@163.com", message.as_string())  
        print("mail has been send successfully.")
    except smtplib.SMTPException as e:
        print(e)

t = time.time()
t = str(int(round(time.time() * 1000)))

formWid_get = ''
collectWid_get = ''
schoolTaskWid_get = ''
itemWid_get = ''
wid1 = ['123','456']
wid3 = []
wid_get = ''

#固定信息
userAgent = "Mozilla/5.0 (Linux; Android 10; TNY-AL00 Build/HUAWEITNY-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/79.0.3945.136 Mobile Safari/537.36 yiban/8.1.9 cpdaily/8.1.9 wisedu/8.1.9"
Cookie = 'clientType=cpdaily_student; tenantId=nbu; sessionToken=********; acw_tc=********; MOD_AUTH_CAS=********'

header_01 = {
    'Connection': 'keep-alive',
    'origin': "https://nbu.cpdaily.com",
    'Accept': 'application/json, text/plain, */*',
    'X-Requested-With':'XMLHttpRequest',
    'Referer': "https://nbu.cpdaily.com/wec-counselor-collector-apps/stu/mobile/index.html?timestamp="+t,
    'Content-Type': 'application/json',
    'User-Agent': userAgent,
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,en-US;q=0.8',
    'Cookie': Cookie
}

body_01 ={
    "pageSize":6,
    "pageNumber":1
}

def getresult_1(formWid_get,collectWid_get):
    print ("正在为您获取【formWid】和【wid1(collectWid)】...")
    postUrl = "https://nbu.cpdaily.com/wec-counselor-collector-apps/stu/collector/queryCollectorProcessingList"
    responseRes = requests.post(postUrl, headers = header_01,data=json.dumps(body_01),verify = False)
    dict_text = json.loads(responseRes.text)
    if (responseRes.status_code == 200):
        print('服务器响应正常！')
        try:
            formWid_get = dict_text['datas']['rows'][0]['formWid'] 
            collectWid_get = dict_text['datas']['rows'][0]['wid']      
            wid1 = [formWid_get,collectWid_get]
            return wid1
        except:
            print('获取【formWid】和【wid1(collectWid)】结束')   
        else:
            print('获取【formWid】和【wid1(collectWid)】结束')
        
wid1 = getresult_1(formWid_get,collectWid_get)

header_02 = {
    'Connection': 'keep-alive',
    'origin': "https://nbu.cpdaily.com",
    'Accept': 'application/json, text/plain, */*',
    'X-Requested-With':'XMLHttpRequest',
    'Referer': "https://nbu.cpdaily.com/wec-counselor-collector-apps/stu/mobile/index.html?collectorWid=%s&timestamp=%s"%(wid1[1],t),
    'Content-Type': 'application/json',
    'User-Agent': userAgent,
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,en-US;q=0.8',
    'Cookie': Cookie
	}

body_02 = {
    "collectorWid": wid1[1]
}


def getresult_2(schoolTaskWid_get):
    print ("正在为您获取【schoolTaskWid】...")
    postUrl = "https://nbu.cpdaily.com/wec-counselor-collector-apps/stu/collector/detailCollector"
    responseRes = requests.post(postUrl, headers = header_02,data=json.dumps(body_02),verify = False)
    dict_text = json.loads(responseRes.text)
    if (responseRes.status_code == 200):
        print('服务器响应正常！')
    try:
        schoolTaskWid_get = dict_text['datas']['collector']['schoolTaskWid']
        return schoolTaskWid_get
    except:
        print('获取【schoolTaskWid】失败')   
    else:
        print('获取【schoolTaskWid】成功！') 
 
schoolTaskWid_get = getresult_2(schoolTaskWid_get)


header_03 = {
    'Connection': 'keep-alive',
    'origin': "https://nbu.cpdaily.com",
    'Accept': 'application/json, text/plain, */*',
    'X-Requested-With':'XMLHttpRequest',
    'Referer': "https://nbu.cpdaily.com/wec-counselor-collector-apps/stu/mobile/index.html?collectorWid=%s&timestamp=%s"%(wid1[1],t),
    'Content-Type': 'application/json',
    'User-Agent': userAgent,
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,en-US;q=0.8',
    'Cookie': Cookie
}
body_03 = {
    "pageSize":10,
    "pageNumber":1,
    "formWid": wid1[0],
    "collectorWid": wid1[1]
}


def getresult_3(itemWid_get,wid_get):
    print ("正在为您获取【itemWid_get】和【wid_get】...")
    postUrl = "https://nbu.cpdaily.com/wec-counselor-collector-apps/stu/collector/getFormFields"
    responseRes = requests.post(postUrl, headers = header_03,data=json.dumps(body_03),verify = False)
    dict_text = json.loads(responseRes.text)
    if (responseRes.status_code == 200):
        print('服务器响应正常！')
    try:
        itemWid_get = dict_text['datas']['rows'][0]['fieldItems'][0]['itemWid']
        wid_get = dict_text['datas']['rows'][0]['wid']
        wid3 = [itemWid_get,wid_get]
        return wid3
    except:
        print('获取【itemWid_get】和【wid_get】失败')   
    else:
        print('获取【itemWid_get】和【wid_get】成功！')


wid3 = getresult_3(itemWid_get,wid_get)
wid_01 = str(int(wid3[1]))
itemWid_01 = str(int(wid3[0]))


def printall():
    print('==========获取的参数为==========')
    print('获取到的formWid为：'+str(wid1[0]))
    print('获取到的collectWid为：'+str(wid1[1]))
    print('获取到的schoolTaskWid为：'+str(schoolTaskWid_get))
    print('获取到的itemWid为：'+str(wid3[0]))
    print('获取到的wid为：'+str(wid3[1]))
    print('================================')


header_final ={
    'Connection': 'keep-alive',
    'origin': "https://nbu.cpdaily.com",
    'Accept': 'application/json, text/plain, */*',
    'X-Requested-With':'XMLHttpRequest',
    'Referer': "https://nbu.cpdaily.com/wec-counselor-collector-apps/stu/mobile/index.html?collectorWid=%s&timestamp=%s"%(wid1[1],t),
    'Content-Type': 'application/json',
    'User-Agent': userAgent,
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,en-US;q=0.8',
    'Cookie': Cookie
}

body_final ={
    "formWid": wid1[0],
    "collectWid": wid1[1],
    "schoolTaskWid": schoolTaskWid_get,
    "form":[
        {
            "wid": wid_01,
            "formWid": wid1[0],
            "fieldType": 2,
            "title": "今日上午您的健康情况是",
            "description": "",
            "minLength": 0,
            "sort": "1",
            "maxLength": "",
            "isRequired": 1,
            "imageCount": "",
            "hasOtherItems": 0,
            "colName": "field001",
            "value": "",
            "fieldItems": [
                {
                    "itemWid": itemWid_01,
                    "content": "A.健康",
                    "isOtherItems": 0,
                    "contendExtend": "",
                    "isSelected": 1
                }
            ]
        }
    ]
} 


def postForm():
    print ("开始健康打卡~")
    print ("正在返回您的打卡结果，请稍候...")
    postUrl = "https://nbu.cpdaily.com/wec-counselor-collector-apps/stu/collector/submitForm"
    responseRes = requests.post(postUrl, headers = header_final,data=json.dumps(body_final),verify = False)
    print(f"statusCode = {responseRes.status_code}")
    print(f"text = {responseRes.text}")

    dict_text2 = json.loads(responseRes.text)
    code = dict_text2['code']
    if code == '0':
        print('打卡成功！')
        sendEmail_for_success()
    else:
        print('打卡失败！')
        sendEmail_for_failure()


def runkiller():    
    getresult_1(formWid_get,collectWid_get)
    getresult_2(schoolTaskWid_get) 
    getresult_3(itemWid_get,wid_get)
    printall()
    postForm()

def keepalive():
    now=strftime("%Y-%m-%d %H:%M:%S", localtime())
    print('当前时间：'+now+'\n===================================')

if __name__ == "__main__":
    runkiller()
    
 


