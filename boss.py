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
  'Cookie': '',
  'User-Agent': 'PostmanRuntime/7.26.8'
}
listUrl = 'https://www.zhipin.com/wapi/zpjob/rec/geek/list'
helloUrl = 'https://www.zhipin.com/wapi/zpboss/h5/chat/start?_=1636084604512'
times = 150 # 设置打招呼次数上限
limit = { # 设置打招呼的限制条件
  # 高级后端开发工程师_上海_18-35k: 3279316d461a6b0f1nF52dS0FFRT
  # nodejs开发工程师: 3860f840951b69af1nF52NS_EVtX
  # java后端开发工程师: 2b3949330e4897281nF52dS6GFVU
  "jobId": "2b3949330e4897281nF52dS6GFVU", # 职位id
  'intention': 'Java', # 求职意向：Java Node.js 前端
  "major": '809,807', # 专业：计算机、电子信息
  "experience": '105,106', # 经验：3-5年，5-10年
  "degree": '203,204', # 学历：本科、硕士
  "age": "16,-1", # 年龄：16-不限
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
  return limit['intention'] in someGuy['geekCard']['expectPositionName']

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