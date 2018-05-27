# -*- coding:utf-8 -*-
import sys
from xinhua_news_helper import XinhuaNewsExtractor
from model.db_operate.mysql_helper import MysqlHelper

reload(sys)
sys.setdefaultencoding('utf-8')


class XinhuaNewsSave():
    """
    迭代获取并保存新闻
    """
    @classmethod
    def save_one_news(cls, url, db_name, table_name):
        news_info = XinhuaNewsExtractor.news_info_by_url(url)
        if news_info:
            MysqlHelper.insert_news_mid(db_name=db_name, table_name=table_name, news_title=news_info["title"], pub_time=news_info["time"], content=news_info["content"], news_src="新华", news_link=news_info["url"], category=news_info["category"], topic='', summary='', polarity=news_info["polarity"])


# MysqlHelper.create_database('xinhua_news')
# MysqlHelper.create_news_table_mid('xinhua_news', 'xinhua_mid')
# XinhuaNewsSave.save_one_news('http://www.xinhuanet.com/politics/2018-04/01/c_1122620497.htm', 'xinhua_news', 'xinhua_mid')
#

