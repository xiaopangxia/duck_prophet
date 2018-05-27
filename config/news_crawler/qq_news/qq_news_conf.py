# -*- coding:utf-8 -*-
import sys
import requests
reload(sys)
sys.setdefaultencoding('utf-8')

sub_site_dict = {
    "news.qq.com": '新闻',
    "mil.qq.com": '军事',
    "finance.qq.com": '财经',
    "sports.qq.com": '体育',
    "ent.qq.com": '娱乐',
    "fashion.qq.com": '时尚',
    "health.qq.com": '健康',
    "baby.qq.com": '育儿',
    "auto.qq.com": '汽车',
    "house.qq.com": '房产',
    "tech.qq.com": '科技',
    "edu.qq.com": '教育',
    "cul.qq.com": '文化',
    "gongyi.qq.com": '公益',
}

entrance_list = ["http://news.qq.com/",
                "http://mil.qq.com/",
                "http://finance.qq.com/",
                "http://sports.qq.com/",
                "http://ent.qq.com/",
                "http://fashion.qq.com/",
                "http://health.qq.com/",
                "http://baby.qq.com/",
                "http://auto.qq.com/",
                "http://house.qq.com/",
                "http://tech.qq.com/",
                "http://edu.qq.com/",
                "http://cul.qq.com/",
                "http://gongyi.qq.com/"]


