#!/usr/bin/python3
# -*- coding: utf-8 -*-
import time
import sys
import random
import requests
import logging
import http.client as http_client

# These two lines enable debugging at httplib level (requests->urllib3->http.client)
# You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# The only thing missing will be the response.body which is not logged.

# 设置请求log
http_client.HTTPConnection.debuglevel = 1
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

# 设置登录cookie
headers = {'Cookie': '_bl_uid=jykp9ueX2UsaUz23biev0URswg7a; lastCity=101020100; wd_guid=f91103c6-0db4-4aed-b2fc-4e35b06b6ce1; historyState=state; __g=-; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1635497013; acw_tc=0b6e704216365081974291806e01997a00b870b68a2fc02c8ad475b4f0d122; wt2=D4SzGVaHizNjijcWYR0omQp3UE6Bv-VtUn9eU0MZ4SCnIcNIB_aJRFMWGz_O69i3Ru8GKV74H7Ema52B74Uc4EA~~; __f=d1e22b6a5f1e40ad275aaebfda5d8be5; zp_token=V1RNgvGef_3F1gXdNqyRgZKSu45T_ezQ%7E%7E; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1636509550; __l=l=%2Fwww.zhipin.com%2Fweb%2Fboss%2Frecommend&r=&g=&s=3&friend_source=0&s=3&friend_source=0; __c=1635497013; __a=83359083.1632724596.1633158678.1635497013.68.3.28.68'}
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
    "page": page
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
  lists = getCandidateList(page).json()
  print(lists)
  return
  for someGuy in lists['data']['zpData']['geekList']:
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