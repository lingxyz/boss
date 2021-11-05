#!/usr/bin/python3
# -*- coding: utf-8 -*-
import time
import sys
import random
import requests

# 设置登录cookie
headers = {'Cookie': ''}
listUrl = 'https://www.zhipin.com/wapi/zpjob/rec/geek/list'
helloUrl = 'https://www.zhipin.com/wapi/zpboss/h5/chat/start?_=1636084604512'
times = 150 # 设置打招呼次数上限

# 获取候选人列表
# @param page 当前页数。从1开始
def getCandidateList(page):
  listData = {
    "age": "16,-1",
    "gender": 0,
    "exchangeResumeWithColleague": 0,
    "switchJobFrequency": 0,
    "activation": 0,
    "recentNotView": 0,
    "school": 0,
    "major": 0,
    "experience": 0,
    "degree": 0,
    "salary": 0,
    "intention": 0,
    "jobId": "3279316d461a6b0f1nF52dS0FFRT",
    "page": page,
    "_":1636084533629
  }
  return requests.get(listUrl, headers=headers, params=listData)

# 打招呼
def sayHelloToSomeGuy(someGuy):
  helloData = {
    "jid": someGuy.encryptJobId,
    "expectId": someGuy.expectId,
    "securityId": someGuy.securityId
  }
  hello = requests.post(helloUrl, headers=headers, json=helloData)

# 批量打招呼
def main(page):
  lists = getCandidateList(page)
  for someGuy in lists['zpData']['geekList']:
    if times > 0:
      sayHelloToSomeGuy(someGuy)
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