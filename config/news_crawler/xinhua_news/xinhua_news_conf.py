# -*- coding:utf-8 -*-
import sys
import requests
reload(sys)
sys.setdefaultencoding('utf-8')





sub_site_dict = {
    "news.cn/politics": '时政',
    "news.cn/local": '地方',
    "news.cn/legal": '法治',
    "news.cn/renshi": '人事',
    "news.cn/world": '国际',
    "news.cn/mil": '军事',
    "news.cn/gangao": '港澳',
    "news.cn/tw": '台湾',
    "news.cn/overseas": '华人',
    "news.cn/fortune/": '财经',
    "news.cn/auto": '汽车',
    "news.cn/house": '房产',
    "education.news.cn/": '教育',
    "news.cn/tech": '科技',
    "news.cn/energy": '能源',
    "ent.news.cn/": '娱乐',
    "news.cn/fashion": '时尚',
    "news.cn/sports/": '体育',
    "news.cn/food": '食品',
    "travel.news.cn/": '旅游',
    "news.cn/health/": '健康',
    "news.cn/info": '信息化',
    "news.cn/gongyi": '公益',
    "xinhuanet.com/silkroad": '一带一路',
    "xinhuanet.com/politics": '时政',
    "xinhuanet.com/local": '地方',
    "xinhuanet.com/legal": '法治',
    "xinhuanet.com/renshi": '人事',
    "xinhuanet.com/world": '国际',
    "xinhuanet.com/mil": '军事',
    "xinhuanet.com/gangao": '港澳',
    "xinhuanet.com/tw": '台湾',
    "xinhuanet.com/overseas": '华人',
    "xinhuanet.com/fortune/": '财经',
    "xinhuanet.com/auto": '汽车',
    "xinhuanet.com/house": '房产',
    "education.xinhuanet.com/": '教育',
    "xinhuanet.com/tech": '科技',
    "xinhuanet.com/energy": '能源',
    "ent.xinhuanet.com/": '娱乐',
    "xinhuanet.com/fashion": '时尚',
    "xinhuanet.com/sports/": '体育',
    "xinhuanet.com/food": '食品',
    "travel.xinhuanet.com/": '旅游',
    "xinhuanet.com/health/": '健康',
    "xinhuanet.com/info": '信息化',
    "xinhuanet.com/gongyi": '公益',
}

entrance_list = ['http://www.xinhuanet.com/',
                 'http://news.cn/']



# 新华网有请求头部要求
xinhua_session = requests.session()
xinhua_headers = {
    "Host": "www.xinhuanet.com",
    # "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "Upgrade-Insecure-Requests": 1,
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "DNT": 1
}

# print xinhua_session.get('http://www.xinhuanet.com/auto/2018-04/03/c_1122629800.htm', headers=xinhua_headers).content
