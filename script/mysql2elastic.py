# -*- coding:utf-8 -*-
import sys
import requests
import pymysql
from elasticsearch import Elasticsearch
from model.db_operate.mysql_helper import MysqlHelper
reload(sys)
sys.setdefaultencoding('utf-8')



# 从mysql数据库全量导入到elastcisearch
conn = MysqlHelper.create_conn()
cur = conn.cursor()

es = Elasticsearch()

db_table_list = ["qq_news.qq_mid", "sina_news.sina_mid", "souhu_news.souhu_mid", "wangyi_news.wangyi_mid", "xinhua_news.xinhua_mid"]
for db_table in db_table_list:
    sql_statement = "select * from %s;" % db_table
    cur.execute(sql_statement)
    res = cur.fetchall()

    for news in res:
        try:
            title = news[1]
            pub_time = str(news[2]).split()[0]
            news_content = news[3]
            src = news[4]
            url = news[5]
            category = news[6]
            topic = news[7]
            polarity = news[9]
            news_data = {
                "title": title,
                "content": news_content,
                "url": url,
                "keywords": topic,
                "pub_time": pub_time,
                "polarity": polarity,
                "category": category,
                "src": src
            }
            es.index(index='blend_news', doc_type='news_doc', body=news_data)
            print src, title
        except Exception, e:
            print e

cur.close()
conn.close()





