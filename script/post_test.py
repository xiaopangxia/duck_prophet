# -*- coding:utf-8 -*-
import sys
import requests
import json
reload(sys)
sys.setdefaultencoding('utf-8')

# 本地请求测试通过
query_body = {"topic": "美国", "time_mode": "day_week"}
json_body = json.dumps(query_body)
res = requests.post("http://localhost:8888/?target=topic_trend", data=json_body)

# print res.content
