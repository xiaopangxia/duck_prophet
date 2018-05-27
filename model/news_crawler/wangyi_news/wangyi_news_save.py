# -*- coding:utf-8 -*-
import sys
from wangyi_news_helper import WangyiNewsExtractor
from model.db_operate.mysql_helper import MysqlHelper

reload(sys)
sys.setdefaultencoding('utf-8')


class WangyiNewsSave():
    """
    迭代获取并保存新闻
    """
    @classmethod
    def save_one_news(cls, url, db_name, table_name):
        news_info = WangyiNewsExtractor.news_info_by_url(url)
        if news_info:
            MysqlHelper.insert_news_mid(db_name=db_name, table_name=table_name, news_title=news_info["title"], pub_time=news_info["time"], content=news_info["content"], news_src="网易", news_link=news_info["url"], category=news_info["category"], topic='', summary='', polarity=news_info["polarity"])






# MysqlHelper.create_database('wangyi_news')
# MysqlHelper.create_news_table_mid('wangyi_news', 'wangyi_mid')
# WangyiNewsSave.save_one_news('http://news.163.com/18/0401/08/DE9V4N450001899N.html', 'wangyi_news', 'wangyi_2018')




