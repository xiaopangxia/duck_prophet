# -*- coding:utf-8 -*-
import sys
from qq_news_helper import QQNewsExtractor
from model.db_operate.mysql_helper import MysqlHelper

reload(sys)
sys.setdefaultencoding('utf-8')


class QQNewsSave():
    """
    迭代获取并保存新闻
    """
    @classmethod
    def save_one_news(cls, url, db_name, table_name):
        news_info = QQNewsExtractor.news_info_by_url(url)
        if news_info:
            MysqlHelper.insert_news_mid(db_name=db_name, table_name=table_name, news_title=news_info["title"], pub_time=news_info["time"], content=news_info["content"], news_src="腾讯", news_link=news_info["url"], category=news_info["category"], topic='', summary='', polarity=news_info["polarity"])


# MysqlHelper.create_database('qq_news')
# MysqlHelper.create_news_table_mid('qq_news', 'qq_mid')
# QQNewsSave.save_one_news('http://sports.qq.com/a/20180403/004097.htm', 'qq_news', 'qq_mid')
#
