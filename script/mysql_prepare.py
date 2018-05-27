# -*- coding:utf-8 -*-
import sys
from model.db_operate.mysql_helper import MysqlHelper
import pymysql
reload(sys)
sys.setdefaultencoding('utf-8')

# create db and tables
if __name__ == "__main__":
    MysqlHelper.create_database('souhu_news')
    MysqlHelper.create_news_table_mid('souhu_news', 'souhu_mid')
    MysqlHelper.create_database('qq_news')
    MysqlHelper.create_news_table_mid('qq_news', 'qq_mid')
    MysqlHelper.create_database('wangyi_news')
    MysqlHelper.create_news_table_mid('wangyi_news', 'wangyi_mid')
    MysqlHelper.create_database('xinhua_news')
    MysqlHelper.create_news_table_mid('xinhua_news', 'xinhua_mid')
    MysqlHelper.create_database('sina_news')
    MysqlHelper.create_news_table_mid('sina_news', 'sina_mid')
    print "db and table created!"





