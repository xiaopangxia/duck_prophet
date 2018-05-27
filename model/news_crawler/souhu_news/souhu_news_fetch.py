# -*- coding:utf-8 -*-
import sys
from souhu_news_helper import SouhuNewsExtractor
from souhu_news_save import SouhuNewsSave
from config.news_crawler.souhu_news.souhu_news_conf import entrance_list
import requests
import Queue
reload(sys)
sys.setdefaultencoding('utf-8')


class SouhuNewsFetch():
    @classmethod
    def fetch_news(cls, news_num):
        """
        抓取若干条新闻
        :param new_num:
        :return:
        """
        news_dict = {}
        visited_url_dict = {}
        visit_url_queue = Queue.Queue()
        for entrance in entrance_list:
           visit_url_queue.put(entrance)
        while len(news_dict) < news_num and not visit_url_queue.empty():
            try:
                seed_url = visit_url_queue.get()
                if 'http://' not in seed_url and 'https://' not in seed_url:
                    seed_url = 'http://' + seed_url.strip('/')
                page_content = requests.get(seed_url).content
                link_dict = SouhuNewsExtractor.extract_link(page_content)
                print u'文章'*50
                for article_url in link_dict["article_link"]:
                    if visited_url_dict.get(article_url) is None and news_dict.get(article_url) is None:
                        SouhuNewsSave.save_one_news(article_url, 'souhu_news', 'souhu_mid')
                        visit_url_queue.put(article_url)
                        news_dict[article_url] = 1
                        print article_url
                print u'站内'*50
                for site_url in link_dict["site_link"]:
                    if visited_url_dict.get(site_url) is None:
                        visit_url_queue.put(site_url)
                        print site_url
                visited_url_dict[seed_url] = 1
            except Exception, e:
                print e





    @classmethod
    def fetch_news_by_day(cls, date, news_num):
        """
        抓取某天新闻若干条
        :param date:
        :param news_num:
        :return:
        """
        pass


if __name__ == '__main__':
    SouhuNewsFetch.fetch_news(2000)

