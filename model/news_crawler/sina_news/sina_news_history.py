# -*- coding:utf-8 -*-
import sys
import requests
import re
from model.db_operate.mysql_helper import MysqlHelper
from model.news_crawler.sina_news.sina_news_helper import SinaNewsExtract
from model.news_crawler.sina_news.sina_news_helper import SinaNewsBrief
from snownlp import SnowNLP
from model.news_crawler.html2article.html2article import Html2Article
from model.sentiment_calc.dict_based_demo.senti_calc_dict import SentiCalc
import time
reload(sys)
sys.setdefaultencoding('utf-8')


class SinaNewsHistory():
    """
    抓取新浪新闻历史文章,允许指定时间范围
    """
    @classmethod
    def db_prepare(cls):
        """
        为新浪新闻建库建表,暂时考虑2018年
        :return:
        """
        MysqlHelper.create_database('sina_news')
        MysqlHelper.create_news_table_mid('sina_news', 'sina_mid')


    @classmethod
    def save_old_news_day(cls, date):
        news_list = SinaNewsBrief.fetch_news_by_day(date)
        print 'news_list_get'
        count = 0
        for news_block in news_list:
            try:
                news_url = news_block['url']
                news_content = Html2Article.url2article(news_url)
                page_content = requests.get(news_url).content
                news_keyword = SinaNewsExtract.extract_keywords(page_content)
                polarity = SentiCalc.score_calc(news_block["title"])
                MysqlHelper.insert_news_mid('sina_news', 'sina_mid', news_block['title'], news_block['time'], news_content, '新浪', news_block['url'], news_block['category'], news_keyword, '', polarity=str(polarity))
                print count, polarity, news_block['title']
                count += 1
            except Exception, e:
                print e


if __name__ == '__main__':
    # SinaNewsHistory.db_prepare()
    for back_day in range(30):
        date = time.strftime("%Y-%m-%d", time.localtime(time.time()-3600*24*back_day))
        SinaNewsHistory.save_old_news_day(date)







