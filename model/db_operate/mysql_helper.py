# -*- coding:utf-8 -*-
import sys
from config.db_operate.mysql_conf import mysql_conf
import pymysql
reload(sys)
sys.setdefaultencoding('utf-8')



class MysqlHelper():
    """
    mysql数据库通用操作类
    """
    @classmethod
    def create_conn(cls):
        """
        创建数据库连接
        :return: conn
        """
        conn = pymysql.connect(host=mysql_conf["host"], charset=mysql_conf["charset"], port=mysql_conf["port"],
                               user=mysql_conf["user"], password=mysql_conf["password"])

        return conn

    @classmethod
    def create_database(cls, db_name):
        """
        库名建库,按照设计,一个来源一个库
        :param db_name:
        :return:
        """
        conn = cls.create_conn()
        cur = conn.cursor()
        sql_statement = "create database if not exists %s;" % str(db_name)
        cur.execute(sql_statement)
        cur.close()
        conn.close()

    @classmethod
    def create_news_table_full(cls, db_name, table_name):
        """
        表名建表,按照设计,每个来源每天一张表
        表的格式暂定为一致
        :param table_name:
        :return:
        """
        try:
            conn = cls.create_conn()
            cur = conn.cursor()
            sql_statement = "use %s" % str(db_name)
            cur.execute(sql_statement)
            sql_statement = "create table if not exists %s(" \
                            "id int PRIMARY KEY AUTO_INCREMENT, " \
                            "news_title varchar(100) not null, " \
                            "author varchar(10), " \
                            "pub_time datetime, " \
                            "content text, " \
                            "news_src varchar(50), " \
                            "news_link VARCHAR (200), " \
                            "category varchar(50), " \
                            "topic text, " \
                            "summary text, " \
                            "view_cnt int, " \
                            "comment_cnt int," \
                            "favor_cnt int, " \
                            "hate_cnt int, " \
                            "heat float, " \
                            "polarity int) DEFAULT CHARSET=utf8;" % str(table_name)
            cur.execute(sql_statement)
            cur.close()
            conn.close()
        except Exception, e:
            print e

    @classmethod
    def create_news_table_mid(cls, db_name, table_name):
        """
        中等规模表,只是不要那些评论热度统计数据
        表的格式暂定为一致
        :param table_name:
        :return:
        """
        try:
            conn = cls.create_conn()
            cur = conn.cursor()
            sql_statement = "use %s" % str(db_name)
            cur.execute(sql_statement)
            sql_statement = "create table if not exists %s(" \
                            "id int PRIMARY KEY AUTO_INCREMENT, " \
                            "news_title varchar(100) not null, " \
                            "pub_time datetime, " \
                            "content text, " \
                            "news_src varchar(50), " \
                            "news_link VARCHAR (200), " \
                            "category varchar(50), " \
                            "topic text, " \
                            "summary text, " \
                            "polarity int, " \
                            "UNIQUE (news_link)) DEFAULT CHARSET=utf8;" % str(table_name)
            cur.execute(sql_statement)
            cur.close()
            conn.close()
        except Exception, e:
            print e

    @classmethod
    def create_news_table_simple(cls, db_name, table_name):
        """
        突然觉得没什么必要存下全文信息,
        只需要一个标题和链接就可以了,
        产品归产品,研究归研究
        :param db_name:
        :param table_name:
        :return:
        """
        try:
            conn = cls.create_conn()
            cur = conn.cursor()
            sql_statement = "use %s" % str(db_name)
            cur.execute(sql_statement)
            sql_statement = "create table if not exists %s(" \
                            "id int PRIMARY KEY AUTO_INCREMENT, " \
                            "news_title varchar(100) not null, " \
                            "pub_time datetime, " \
                            "news_src varchar(50), " \
                            "news_link VARCHAR (200), " \
                            "category varchar(50), " \
                            "topic text, " \
                            "polarity int, " \
                            "UNIQUE (new_link)) DEFAULT CHARSET=utf8;" % str(table_name)
            cur.execute(sql_statement)
            cur.close()
            conn.close()
        except Exception, e:
            print e




    @classmethod
    def insert_news_full(cls, db_name, table_name, news_title, author, pub_time, content, news_src, news_link,
                    category, topic, summary, view_cnt, comment_cnt, favor_cnt, hate_cnt, heat, polarity):
        """
        往新闻数据库插入新闻
        :param db_name:
        :param table_name:
        :param news_title:
        :param author:
        :param pub_time:
        :param content:
        :param news_src:
        :param news_link:
        :param category:
        :param topic:
        :param summary:
        :param view_cnt:
        :param comment_cnt:
        :param favor_cnt:
        :param hate_cnt:
        :param heat:
        :param polarity:
        :return:
        """
        try:
            conn = cls.create_conn()
            cur = conn.cursor()
            sql_statement = "insert into %s.%s(news_title, author, pub_time, content, news_src, news_link, category, " \
                            "topic, summary, view_cnt, comment_cnt, favor_cnt, hate_cnt, heat, polarity) values('%s', " \
                            "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %s, %s, %s, %s, %s, %s);" % \
                            (db_name, table_name, news_title, author, pub_time, content, news_src, news_link, category,
                             topic, summary, view_cnt, comment_cnt, favor_cnt, hate_cnt, heat, polarity)
            # print sql_statement
            cur.execute(sql_statement)
            conn.commit()
            cur.close()
            conn.close()
        except Exception, e:
            print e

    @classmethod
    def insert_news_mid(cls, db_name, table_name, news_title, pub_time, content, news_src, news_link, category, topic, summary, polarity):
        """
        插入中等规模新闻数据
        :param db_name:
        :param table_name:
        :param news_title:
        :param pub_time:
        :param content:
        :param news_src:
        :param news_link:
        :param category:
        :param topic:
        :param summary:
        :param polarity:
        :return:
        """
        try:
            conn = cls.create_conn()
            cur = conn.cursor()
            sql_statement = "insert into %s.%s(news_title, pub_time, content, news_src, news_link, category, " \
                            "topic, summary, polarity) values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %s);" % \
                            (db_name, table_name, news_title, pub_time, content, news_src, news_link, category, topic, summary, polarity)
            # print sql_statement
            cur.execute(sql_statement)
            conn.commit()
            cur.close()
            conn.close()
        except Exception, e:
            print e

    @classmethod
    def insert_news_simple(cls, db_name, table_name, news_title, pub_time, news_src, news_link, category, topic, polarity):
        """
        往简版新闻表里插数据
        :param db_name:
        :param table_name:
        :param news_title:
        :param pub_time:
        :param news_src:
        :param news_link:
        :param category:
        :param topic:
        :param polarity:
        :return:
        """
        try:
            conn = cls.create_conn()
            cur = conn.cursor()
            sql_statement = "insert into %s.%s(news_title, pub_time, news_src, news_link, category, topic, polarity) values('%s', '%s', '%s', '%s', '%s', '%s', %s);" % (db_name, table_name, news_title, pub_time, news_src, news_link, category, topic, polarity)
            # print sql_statement
            cur.execute(sql_statement)
            conn.commit()
            cur.close()
            conn.close()
        except Exception, e:
            print e





# MysqlHelper.create_database('renmingwang')
# MysqlHelper.create_news_table('renmingwang', 'tb20180325')
# MysqlHelper.insert_news('renmingwang', 'tb20180325', '中国', 'bbb', '2018-03-25 00:00:00', '世界', 'ddd', 'eee', 'fff',
#                         'ggg', 'hhh', '10', '11', '12', '13', '14.4', '-1')



