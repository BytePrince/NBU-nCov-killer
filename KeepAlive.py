# -*- coding: utf-8 -*-
import requests
import time
import json
import random
from time import strftime, localtime

t = time.time()
t = str(int(round(time.time() * 1000)))

userAgent = "Mozilla/5.0 (Linux; Android 10; TNY-AL00 Build/HUAWEITNY-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/79.0.3945.136 Mobile Safari/537.36 yiban/8.1.9 cpdaily/8.1.9 wisedu/8.1.9"
header = {
    #'Content-Length': '66',
    "origin": "https://nbu.cpdaily.com",
    'Accept': 'application/json, text/plain, */*',
    'X-Requested-With':'XMLHttpRequest',
    "Referer": "https://nbu.cpdaily.com/wec-counselor-collector-apps/stu/mobile/index.html?collectorWid=966&timestamp="+t,
    'User-Agent': userAgent,
    'Cookie':'clientType=cpdaily_student; tenantId=nbu; sessionToken=********; acw_tc=********; MOD_AUTH_CAS=********',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Sec-Fetch-Site':'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
}


body = {
    "pageSize":6,
    "pageNumber":1,
    "formWid":"61",
    "collectorWid":"1222"
}

def getresult():
    postUrl = "https://nbu.cpdaily.com/wec-counselor-collector-apps/stu/collector/getFormFields"
    responseRes = requests.post(postUrl, headers = header,data=json.dumps(body))
    if (responseRes.status_code == 200):
        print('==================获取formwid成功！   ==================\n==================获取wid（collectWid）成功！==================')


if __name__ == "__main__":
    # 返回结果
    now=strftime("%Y-%m-%d %H:%M:%S", localtime())
    print ("-----------------正在为您持续保障登录状态"+"["+now+"]"+"-----------------")
    getresult()
    print(now)
  