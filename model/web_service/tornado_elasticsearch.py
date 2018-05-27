# -*- coding:utf-8 -*-
import sys
from model.db_operate.mysql_helper import MysqlHelper
from elasticsearch import Elasticsearch
from model.news_crawler.html2article.html2article import Html2Article
from model.news_text_analyze.text_rank.news_text_rank import NewsTextRank
import time
reload(sys)
sys.setdefaultencoding('utf-8')


class TornadoElasticsearch():
    """
    给web服务提供请求数据,从elasticsearch里拿
    """

    @classmethod
    def news_search(cls, query_body, page_num):
        """
        新闻搜索
        :param page_num: 搜索结果显示页号
        :param query_body: 查询题
        :return:
        """
        try:
            es = Elasticsearch()
            # 查询体
            search_body = {
                "query": {
                    "bool": {
                        "must": [],
                        "should": []
                    }
                }
            }
            if query_body.get("polarity") not in ["all", u"all"]:
                polarity_match = {"match": {"polarity": query_body.get("polarity")}}
                search_body["query"]["bool"]["must"].append(polarity_match)
            if query_body.get("src") not in ["all", u"all"]:
                src_match = {"match": {"src": str(query_body.get("src"))}}
                search_body["query"]["bool"]["must"].append(src_match)
            if len(query_body.get("topic")) > 0:
                title_match = {"match": {"title": str(query_body.get("topic"))}}
                search_body["query"]["bool"]["must"].append(title_match)
                content_match = {"match": {"content": str(query_body.get("topic"))}}
                search_body["query"]["bool"]["should"].append(content_match)


            # 支持两种日期范围格式
            if str(query_body.get("date_range")) is not "":
                date_str = str(query_body.get("date_range"))
                now_day = time.strftime("%Y-%m-%d", time.localtime(time.time()))
                day_ago = time.strftime("%Y-%m-%d", time.localtime(time.time() - 3600 * 24 * 2))
                week_ago = time.strftime("%Y-%m-%d", time.localtime(time.time() - 3600 * 24 * 8))
                month_ago = time.strftime("%Y-%m-%d", time.localtime(time.time() - 3600 * 24 * 31))
                year_ago = time.strftime("%Y-%m-%d", time.localtime(time.time() - 3600 * 24 * 365))
                date_range_dict = {
                    "day": {"start_time": day_ago, "end_time": now_day},
                    "week": {"start_time": week_ago, "end_time": now_day},
                    "month": {"start_time": month_ago, "end_time": now_day},
                    "year": {"start_time": year_ago, "end_time": now_day},
                    "all": {"start_time": "1919-01-01", "end_time": now_day}
                }
                if date_range_dict.get(date_str) is not None:
                    start_date = date_range_dict[date_str]["start_time"]
                    end_date = date_range_dict[date_str]["end_time"]
                else:
                    start_date = date_str.split()[0]
                    end_date = date_str.split()[1]
                date_range = {
                    "range": {
                        "pub_time": {
                            "gte": start_date,
                            "lte": end_date
                        }
                    }
                }
                search_body["query"]["bool"]["must"].append(date_range)
            search_body["from"] = (int(page_num) - 1) * 20
            search_body["size"] = 20

            print search_body
            # 组织查询结果
            whole_res = es.search(index="blend_news", doc_type="news_doc", body=search_body)
            hits_res = whole_res["hits"]
            max_score = hits_res["max_score"]
            final_res = {"total": hits_res["total"], "news_list": []}
            for hit in hits_res["hits"]:
                news_block = {}
                news_block["score"] = (hit["_score"] * 10.0) / max_score  # 相似度采用十分制
                news_block["title"] = hit["_source"]["title"]
                news_block["url"] = hit["_source"]["url"]
                news_block["pub_time"] = hit["_source"]["pub_time"]
                news_block["polarity"] = hit["_source"]["polarity"]
                news_block["category"] = hit["_source"]["category"]
                news_block["src"] = hit["_source"]["src"]
                final_res["news_list"].append(news_block)

            return final_res
        except Exception, e:
            print e
            return None


    @classmethod
    def news_analyze(cls, query_body):
        """
        单篇新闻分析,按url精准取新闻内容,从mysql里取,其次从网络抓取
        :param query_body:
        :return:
        """
        news_content = ""
        news_url = query_body["news_url"]
        news_src = query_body["news_src"]
        src_dict = {
            "新浪": "sina_news.sina_mid",
            "网易": "wangyi_news.wangyi_mid",
            "腾讯": "qq_news.qq_mid",
            "搜狐": "souhu_news.souhu_mid",
            "新华": "xinhua_new.xinhua_mid"}
        try:
            sql_statement = "select * from %s where news_link='%s';" % (src_dict[news_src], news_url)
            conn = MysqlHelper.create_conn()
            cur = conn.cursor()
            cur.execute(sql_statement)
            mysql_res = cur.fetchall()
            if len(mysql_res) > 0:
                news_content = mysql_res[0][3]
            else:
                # 数据库搜不到,从网络爬,用新华网的session来抓
                news_content = Html2Article.url2article(news_url)
        except Exception, e:
            # 数据库搜不到,从网络爬,用新华网的session来抓
            news_content = Html2Article.url2article(news_url)
        if len(news_content) < 50:
            return None

        news_keywords = NewsTextRank.news_keywords_23(news_content)
        news_summary = NewsTextRank.news_summary(news_content)
        # print news_keywords
        # print news_summary
        res_dict = {"news_keywords": news_keywords, "news_summary": news_summary}
        return res_dict




    @classmethod
    def topic_trend(cls, query_body):
        """
        话题趋势分析
        :param query_body: 请求参数,有topic和time_mode
            time_mode分五类:
                day_week
                day_month
                day_year
                week_year
                month_year
        :return:
        """
        try:
            now_day = time.strftime("%Y-%m-%d", time.localtime(time.time()))
            week_ago = time.strftime("%Y-%m-%d", time.localtime(time.time()-3600*24*8))
            month_ago = time.strftime("%Y-%m-%d", time.localtime(time.time()-3600*24*31))
            year_ago = time.strftime("%Y-%m-%d", time.localtime(time.time()-3600*24*365))
            time_mode_dict = {
                "day_week": {"interval": "day", "start_time": week_ago, "end_time": now_day},
                "day_month": {"interval": "day", "start_time": month_ago, "end_time": now_day},
                "day_year": {"interval": "day", "start_time": year_ago, "end_time": now_day},
                "week_year": {"interval": "week", "start_time": year_ago, "end_time": now_day},
                "month_year": {"interval": "month", "start_time": month_ago, "end_time": now_day}
            }

            topic = query_body.get("topic")
            time_mode = query_body.get("time_mode")
            interval = time_mode_dict[time_mode]["interval"]
            start_time = time_mode_dict[time_mode]["start_time"]
            end_time = time_mode_dict[time_mode]["end_time"]

            # 查询体
            search_body = {
                "size": 0,
                "query": {
                    "bool": {
                        "must": [
                            {"match": {"title": topic}},
                            {"range": {"pub_time": {"gte": start_time, "lte": end_time}}}
                        ],
                        "should": [
                            {"match": {"content": topic}}
                        ]
                    }
                },
                "aggs": {
                    "daily_count": {
                        "date_histogram": {
                            "field": "pub_time",
                            "interval": interval,
                            "format": "yyyy-MM-dd",
                            "min_doc_count": 0,
                            "extended_bounds": {
                                "min": start_time,
                                "max": end_time
                            }
                        }
                    }
                }
            }

            # 查询
            es = Elasticsearch()
            res = es.search(index="blend_news", doc_type="news_doc", body=search_body)["aggregations"]["daily_count"]["buckets"]
            # print res
            return res
        except Exception, e:
            print e
            return None


query_body = {u'polarity': u'all', u'src': u'all', u'topic': u'', u'date_range': u''}
print TornadoElasticsearch.news_search(query_body, 1)


# query_body = {
#     "news_url": "http://news.163.com/18/0322/17/DDH5MPEF000189DH.html",
#     "news_src": "腾讯"
# }
# TornadoElasticsearch.news_analyze(query_body)


# query_body = {
#     "topic": "中美",
#     "time_mode": "day_month"
# }
# TornadoElasticsearch.topic_trend(query_body)

