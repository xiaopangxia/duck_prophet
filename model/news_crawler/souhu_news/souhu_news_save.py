# -*- coding:utf-8 -*-
import sys
from souhu_news_helper import SouhuNewsExtractor
from model.db_operate.mysql_helper import MysqlHelper

reload(sys)
sys.setdefaultencoding('utf-8')


class SouhuNewsSave():
    """
    迭代获取并保存新闻
    """
    @classmethod
    def save_one_news(cls, url, db_name, table_name):
        news_info = SouhuNewsExtractor.news_info_by_url(url)
        if news_info:
            MysqlHelper.insert_news_mid(db_name=db_name, table_name=table_name, news_title=news_info["title"], pub_time=news_info["time"], content=news_info["content"], news_src="搜狐", news_link=news_info["url"], category=news_info["category"], topic='', summary='', polarity=news_info["polarity"])





# MysqlHelper.create_database('souhu_news')
# MysqlHelper.create_news_table_mid('souhu_news', 'souhu_mid')
# SouhuNewsSave.save_one_news('http://www.sohu.com/a/226884978_247380', 'souhu_news', 'souhu_mid')






