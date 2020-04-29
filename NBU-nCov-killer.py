# -*- coding: utf-8 -*-
import requests
import sys
import time
import json
import random
import smtplib
import datetime
from time import strftime, localtime
from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError
from email.header import Header
from email.mime.text import MIMEText
from apscheduler.schedulers.blocking import BlockingScheduler





def sendEmail_for_success():
    message = MIMEText("尊敬的主人您好，今天的打卡已经为您完成！", 'plain', 'utf-8')  
    message['From'] = "{}".format("xxx@xxx.com")
    message['To'] = "xxx@xxx.cn"
    message['Subject'] = "打卡成功提醒"
 
    try:
        smtpObj = smtplib.SMTP_SSL("smtp.163.com", 465)  
        smtpObj.login("zzzain46", "AAAAAAAAAAAA")  
        smtpObj.sendmail("xxx@xxx.com","xxx@xxx.cn", message.as_string())  
        print("mail has been send successfully.")
    except smtplib.SMTPException as e:
        print(e)

def sendEmail_for_failure():
    message = MIMEText("尊敬的主人您好，服务异常，请您上线检查！", 'plain', 'utf-8')  
    message['From'] = "{}".format("xxx@xxx.com")
    message['To'] = "xxx@xxx.cn"
    message['Subject'] = "服务异常警告"
 
    try:
        smtpObj = smtplib.SMTP_SSL("smtp.163.com", 465)  
        smtpObj.login("zzzain46", "AAAAAAAAAAAA")  
        smtpObj.sendmail("xxx@xxx.com","xxx@xxx.cn", message.as_string())  
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


userAgent = "Mozilla/5.0 (Linux; Android 10; TNY-AL00 Build/HUAWEITNY-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/79.0.3945.136 Mobile Safari/537.36 yiban/8.1.9 cpdaily/8.1.9 wisedu/8.1.9"
Cookie = 'clientType=cpdaily_student; tenantId=nbu; sessionToken=; acw_tc=; MOD_AUTH_CAS='

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
wid_02 = str(int(wid3[1])+1)
wid_03 = str(int(wid3[1])+2)
wid_04 = str(int(wid3[1])+3)
wid_05 = str(int(wid3[1])+4)
wid_06 = str(int(wid3[1])+5)
wid_07 = str(int(wid3[1])+6)
wid_08 = str(int(wid3[1])+7)
wid_09 = str(int(wid3[1])+8)
wid_10 = str(int(wid3[1])+9)

itemWid_01 = str(int(wid3[0]))
itemWid_02 = str(int(wid3[0])+5)
itemWid_03 = str(int(wid3[0])+8)
itemWid_04 = str(int(wid3[0])+10)
itemWid_05 = str(int(wid3[0])+12)



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
            "fieldType":2,
            "title":"今日你的甬行码是什么颜色？",
            "description":"其他选项请注明具体情况哦。蓝色的同学请你看看二维码颜色",
            "minLength":0,
            "sort":"1",
            "maxLength":"",
            "isRequired":1,
            "imageCount":"",
            "hasOtherItems":1,
            "colName":"field001",
            "value":"",
            "fieldItems":[
                {
                    "itemWid":itemWid_01,
                    "content":"绿色",
                    "isOtherItems":0,
                    "contendExtend":"",
                    "isSelected":1
                }
            ]
        },
        {
            "wid": wid_02,
            "formWid": wid1[0],
            "fieldType":2,
            "title":"今日健康打卡",
            "description":"",
            "minLength":0,
            "sort":"2",
            "maxLength":"",
            "isRequired":1,
            "imageCount":"",
            "hasOtherItems":0,
            "colName":"field002",
            "value":"",
            "fieldItems":[
                {
                    "itemWid":itemWid_02,
                    "content":"健康",
                    "isOtherItems":0,
                    "contendExtend":"",
                    "isSelected":1
                }
            ]
        },
        {
            "wid": wid_03,
            "formWid": wid1[0],
            "fieldType":2,
            "title":"相对昨日，现居住地是否变化？",
            "description":"",
            "minLength":0,
            "sort":"3",
            "maxLength":"",
            "isRequired":1,
            "imageCount":"",
            "hasOtherItems":0,
            "colName":"field003",
            "value":"",
            "fieldItems":[
                {
                    "itemWid":itemWid_03,
                    "content":"无变化",
                    "isOtherItems":0,
                    "contendExtend":"",
                    "isSelected":1
                }
            ]
        },
        {
            "wid": wid_04,
            "formWid": wid1[0],
            "fieldType":2,
            "title":"今日是否从湖北省返回浙江？",
            "description":"请大家仔细、如实填写，不要选错。",
            "minLength":0,
            "sort":"4",
            "maxLength":"",
            "isRequired":1,
            "imageCount":"",
            "hasOtherItems":0,
            "colName":"field004",
            "value":"",
            "fieldItems":[
                {
                    "itemWid":itemWid_04,
                    "content":"否",
                    "isOtherItems":0,
                    "contendExtend":"",
                    "isSelected":1
                }
            ]
        },
        {
            "wid": wid_05,
            "formWid": wid1[0],
            "fieldType":2,
            "title":"今日是否从温州、温岭、黄岩返回宁波？",
            "description":"请大家仔细、如实填写，不要选错。",
            "minLength":0,
            "sort":"5",
            "maxLength":"",
            "isRequired":1,
            "imageCount":"",
            "hasOtherItems":0,
            "colName":"field005",
            "value":"",
            "fieldItems":[
                {
                    "itemWid":itemWid_05,
                    "content":"否",
                    "isOtherItems":0,
                    "contendExtend":"",
                    "isSelected":1
                }
            ]
        },
        {
            "wid": wid_06,
            "formWid": wid1[0],
            "fieldType":1,
            "title":"【没有变化不用填】如有变化，请选择新的现居住地区域。",
            "description":"",
            "minLength":1,
            "sort":"6",
            "maxLength":300,
            "isRequired":0,
            "imageCount":-2,
            "hasOtherItems":0,
            "colName":"field006",
            "value":"",
            "fieldItems":[
    
            ]
        },
        {
            "wid": wid_07,
            "formWid": wid1[0],
            "fieldType":2,
            "title":"【没有异常不用填】目前异常状况是？",
            "description":"异常状况请填写：发热、咳嗽等具体症状",
            "minLength":0,
            "sort":"7",
            "maxLength":"",
            "isRequired":0,
            "imageCount":"",
            "hasOtherItems":1,
            "colName":"field007",
            "value":"",
            "fieldItems":[
            ]
        },
        {
            "wid": wid_08,
            "formWid": wid1[0],
            "fieldType":2,
            "title":"【无情况的不用填】此前集中隔离的，今日是否已解除隔离？",
            "description":"",
            "minLength":0,
            "sort":"8",
            "maxLength":"",
            "isRequired":0,
            "imageCount":"",
            "hasOtherItems":0,
            "colName":"field008",
            "value":"",
            "fieldItems":[
            ]
        },
        {
            "wid": wid_09,
            "formWid": wid1[0],
            "fieldType":2,
            "title":"【没有异常不用填】已采取的措施是？",
            "description":"",
            "minLength":0,
            "sort":"9",
            "maxLength":"",
            "isRequired":0,
            "imageCount":"",
            "hasOtherItems":0,
            "colName":"field009",
            "value":"",
            "fieldItems":[
            ]
        },
        {
            "wid": wid_10,
            "formWid": wid1[0],
            "fieldType":2,
            "title":"【没有异常不用填】是否确诊新型冠状肺炎？",
            "description":"",
            "minLength":0,
            "sort":"10",
            "maxLength":"",
            "isRequired":0,
            "imageCount":"",
            "hasOtherItems":0,
            "colName":"field010",
            "value":"",
            "fieldItems":[
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





def sendmessage():
    try:
     result = ssender.send_with_param(86, phone_number,
      template_id, params, sign=sms_sign, extend="", ext="") 
    except HTTPError as e:
      print(e)
    except Exception as e:
      print(e)
      print(result)    	


if __name__ == "__main__":
    runkiller()
    
 


