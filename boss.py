#!/usr/bin/python3
# -*- coding: utf-8 -*-
import time
import sys
import random
import requests
import json
import logging
import http.client as http_client

# These two lines enable debugging at httplib level (requests->urllib3->http.client)
# You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# The only thing missing will be the response.body which is not logged.

# 设置请求log。(调试用)
# http_client.HTTPConnection.debuglevel = 1
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

# 设置登录cookie
headers = {
  'Cookie': '_bl_uid=jykp9ueX2UsaUz23biev0URswg7a; lastCity=101020100; wd_guid=f91103c6-0db4-4aed-b2fc-4e35b06b6ce1; historyState=state; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1644200722; __g=mail_resume_niu; wt2=DJytreOQ5YChQDe0PAccgksunzHy4Jbuz6fYAfj7reJ92XAKnm5MmAycwGTdNG9Wj1KR6FyIj2f6LxIqjXxY_GQ~~; acw_tc=0bdccfef16463744485864324e50890bdafd7f949200f9151d3e3ced9cf6d2; zp_token=V1RNkjEuf52FhsVtRvyxsbLi-55DPVzS0%7E; __l=l=%2Fwww.zhipin.com%2Fweb%2Fboss%2Findex&r=&g=%2Fm.zhipin.com%2Fweb%2Fcommon%2Fmail%2Fresume-page.html%3Fuuid%3D1942b20a6fcd002f1nV43tW1EFVTwpG-UfuWRuOqnvfNMxNm3aRXmLnq%26sid%3Dmail_resume_niu&s=3&friend_source=0&s=3&friend_source=0; __fid=6b4d2f5c6794da65d1606cc052ae1e53; geek_zp_token=V1RNkjEuf52FhsVtRvyxsbLi6w7jjXwiQ~; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1646374482; __c=1639706409; __a=83359083.1632724596.1635497013.1639706409.189.4.77.22',
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
}
listUrl = 'https://www.zhipin.com/wapi/zpjob/rec/geek/list'
helloUrl = 'https://www.zhipin.com/wapi/zpboss/h5/chat/start?_=1636084604512'
times = 100 # 设置打招呼次数上限
limit = { # 设置打招呼的限制条件
  # 高级后端开发工程师_上海_18-35k: 3279316d461a6b0f1nF52dS0FFRT
  # nodejs开发工程师: 3860f840951b69af1nF52NS_EVtX
  # java后端开发工程师: 2b3949330e4897281nF52dS6GFVU
  # 高级前端开发工程师: 1ae02c00f080d8231nF52NS8FFVU
  # 前端开发工程师: b2a4396cd9b5ae401nx40t28EVdR
  "jobId": "3279316d461a6b0f1nF52dS0FFRT", # 职位id
  'intention': 'Java', # 求职意向: Java Node.js 前端
  "major": '809,807', # 专业: 计算机、电子信息
  "experience": '106', # 经验: '105,106'，3-5年，5-10年
  "degree": '203,204', # 学历: 本科、硕士
  "age": "16,-1", # 年龄: 16-不限
  "company": {'美团', '点评', '平安', '拉扎斯', '百度', '顺丰', '申通'}, # 公司限制（一二线互联网）
}

# 获取候选人列表
# @param page 当前页数。从1开始
def getCandidateList(page):
  listData = {
    "age": limit['age'],
    "gender": 0,
    "exchangeResumeWithColleague": 0,
    "switchJobFrequency": 0,
    "activation": 0,
    "recentNotView": 0,
    "school": 0,
    "major": limit['major'],
    "experience": limit['experience'],
    "degree": limit['degree'],
    "salary": 0,
    "intention": 0,
    "jobId": limit['jobId'],
    "page": page
  }
  return requests.get(listUrl, headers=headers, params=listData)

# 候选人打招呼限制：根据条件过滤
def filterGuy(limit, someGuy):
  # 期望职位过滤
  isIntention = limit['intention'] in someGuy['geekCard']['expectPositionName']
  isCompany = False
  isPositionName = True
  for work in someGuy['geekCard']['geekWorks']:
    # 过往履职关键字过滤
    if limit['intention'] not in work['positionName']:
      isPositionName = False
      break
    # 公司过滤
    for companyKey in limit['company']:
      if companyKey in work['company']:
        isCompany = True
        break
  return isIntention and isPositionName# and isCompany

# 打招呼
def sayHelloToSomeGuy(encryptJobId, expectId, securityId, someGuy):
  print('打招呼To：' + someGuy['geekCard']['geekName'] + '...')
  helloData = {
    "jid": encryptJobId,
    "expectId": expectId,
    "securityId": securityId
  }
  hello = requests.post(helloUrl, headers=headers, data=helloData).json()
  if hello['code'] == 0: print("打招呼成功！")
  else: print('打招呼失败：' + hello['message'])


# 批量打招呼
def main(page):
  lists = getCandidateList(page).json()
  # print(lists['zpData']['geekList'])
  # return
  encryptJobId = lists['zpData']['encryptJobId']
  for someGuy in lists['zpData']['geekList']:
    global times
    print(times)
    if times > 0 and filterGuy(limit, someGuy):
      expectId = someGuy['geekCard']['expectId']
      securityId = someGuy['geekCard']['securityId']
      sayHelloToSomeGuy(encryptJobId, expectId, securityId, someGuy)
      times -= 1
      waitingSecond = random.randint(3, 10) # 随机等3-10s
      time.sleep(waitingSecond)
      sys.stdout.flush()
    else:
      break
  if  times > 0:
    page += 1
    main(page)

main(1)