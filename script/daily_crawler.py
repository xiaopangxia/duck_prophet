# -*- coding:utf-8 -*-
import sys
import time
from model.news_crawler.qq_news.qq_news_fetch import QQNewsFetch
from model.news_crawler.sina_news.sina_news_history import SinaNewsHistory
from model.news_crawler.souhu_news.souhu_news_fetch import SouhuNewsFetch
from model.news_crawler.wangyi_news.wangyi_news_fetch import WangyiNewsFetch
from model.news_crawler.xinhua_news.xinhua_news_fetch import XinhuaNewsFetch
reload(sys)
sys.setdefaultencoding('utf-8')


while True:
    QQNewsFetch.fetch_news(2000)
    SouhuNewsFetch.fetch_news(2000)
    WangyiNewsFetch.fetch_news(2000)
    XinhuaNewsFetch.fetch_news(2000)
    date = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    SinaNewsHistory.save_old_news_day(date)
    time.sleep(3600)











