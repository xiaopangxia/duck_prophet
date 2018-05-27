# -*- coding:utf-8 -*-
import sys
from model.news_crawler.qq_news.qq_news_fetch import QQNewsFetch
from model.news_crawler.sina_news.sina_news_history import SinaNewsHistory
from model.news_crawler.souhu_news.souhu_news_fetch import SouhuNewsFetch
from model.news_crawler.wangyi_news.wangyi_news_fetch import WangyiNewsFetch
from model.news_crawler.xinhua_news.xinhua_news_fetch import XinhuaNewsFetch
import time
reload(sys)
sys.setdefaultencoding('utf-8')



if __name__ == '__main__':
    QQNewsFetch.fetch_news(5000)
    for back_day in range(30):
        date = time.strftime("%Y-%m-%d", time.localtime(time.time() - 3600 * 24 * back_day))
        SinaNewsHistory.save_old_news_day(date)
    SouhuNewsFetch.fetch_news(5000)
    WangyiNewsFetch.fetch_news(3000)
    XinhuaNewsFetch.fetch_news(5000)




