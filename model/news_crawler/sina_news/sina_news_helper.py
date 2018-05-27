# -*- coding:utf-8 -*-
import sys
from config.news_crawler.sina_news.sina_news_conf import entrance_list
import re
import requests
from bs4 import BeautifulSoup
import json
import demjson
import time
reload(sys)
sys.setdefaultencoding('utf-8')


class SinaNewsExtract():
    """
    新闻页面分析文章内容抽取类,
    关注新闻全文
    主要区别PC站和手机站
    """
    @classmethod
    def extract_title(cls, page_content, device='pc'):
        try:
            if device is 'pc':
                title_pattern = re.compile(u'<h1 class="main-title">(.*?)</h1>')
                title_list = re.findall(title_pattern, page_content)
                return title_list[0]
            elif device is 'phone':
                title_pattern = re.compile(u'<h1 class="art_tit_h1">(.*?)</h1>')
                title_list = re.findall(title_pattern, page_content)
                return title_list[0]
        except Exception, e:
            print e
            print 'title_failed'
        return None



    @classmethod
    def extract_content(cls, page_content, device='pc'):
        try:
            mysoup = BeautifulSoup(page_content, 'lxml')
            if device is 'pc':
                article_content = mysoup.find('div', attrs={"class": "article"})
            elif device is 'phone':
                article_content = mysoup.find('article', attrs={"class": "art_box"})
            text_list = article_content.stripped_strings
            content_text = ''
            for text in text_list:
                content_text += text
            return content_text
        except Exception, e:
            print e
            print 'content_failed'
        return None



    @classmethod
    def extract_keywords(cls, page_content, device='pc'):
        try:
            if device is 'pc':
                keywords_pattern = re.compile(u'<div class="keywords" id="keywords" data-wbkey="(.*?)"')
                keywords_list = re.findall(keywords_pattern, page_content)
                return keywords_list[0]
            elif device is 'phone':
                pass  # 手机版没有标关键词,回头通过算法抽取
        except Exception, e:
            # print e
            # print 'keywords_failed'
            pass
        return None



    @classmethod
    def extract_pub_time(cls, page_content, device='pc'):
        try:
            if device is 'pc':
                pub_time_pattern = re.compile(u'<span class="date">(.*?)</span>')
                pub_time_list = re.findall(pub_time_pattern, page_content)
                return pub_time_list[0]
            elif device is 'phone':
                pub_time_pattern = re.compile(u'<time class="art_time">(.*?)<cite class="art_cite">')
                pub_time_list = re.findall(pub_time_pattern, page_content)
                return pub_time_list[0]
        except Exception, e:
            # print e
            # print 'pub_time_failed'
            pass
        return None


    @classmethod
    def comment_cnt(cls, page_content, device='pc'):
        # 新浪新闻这里只考虑参与评论数
        try:
            if device=='pc':
                mysoup = BeautifulSoup(page_content, 'lxml')
                com_cnt = mysoup.find('span', attrs={"class": "num", "node-type": "comment-num"})
                print com_cnt
                return int(com_cnt.string)
            elif device == 'phone':
                com_cnt_pattern = re.compile('<em class ="fl_words_num j_cmnt_bottom_num">(.*?)</em>')
                com_cnt_list = re.findall(com_cnt_pattern, page_content)
                return int(com_cnt_list[0])
        except Exception, e:
            # print e
            # print 'com_cnt_failed'
            pass
        return None

    @classmethod
    def extract_link(cls, page_content):
        try:
            link_pattern_1 = re.compile(u'href="(.*?)"')
            link_pattern_2 = re.compile(u'src="(.*?)"')
            link_list_large = []
            link_list_href = re.findall(link_pattern_1, page_content)
            link_list_src = re.findall(link_pattern_2, page_content)
            link_list_large.extend(link_list_href)
            link_list_large.extend(link_list_src)
            article_link = []  # 疑似文章链接
            site_link = []  # 非文章,站内链接
            for link in link_list_large:
                num_star_str = re.sub('\d', '0', link)  # 将数字全部替换为0,用于判断是否包含日期串
                # print num_star_str
                if ('sina.com.cn' in link or 'sina.cn' in link) and ('html' in link or 'shtml' in link) and ('0000-00-00' in num_star_str):
                    article_link.append(link.strip('/'))
                elif ('sina.com.cn' in link or 'sina.cn' in link):
                    site_link.append(link.strip('/'))
            return {"article_link": article_link, "site_link": site_link}
        except Exception, e:
            print e
        return {"article_link": [], "site_link": []}

class SinaNewsBrief():
    """
    不关注新闻全文,只关注标题
    从新闻中心,rss以及搜索列表获取
    """
    @classmethod
    def fetch_news_10000(cls):
        """
        从新浪新闻抓取一万条新闻
        :return:
        """

        # 直接调接口,可惜拿到的不是json串,var jsonData = { };需要自己解析
        res = requests.get('http://roll.news.sina.com.cn/interface/rollnews_ch_out_interface.php?col=89&num=10000&page=1')
        data_text = unicode(res.content.decode('gbk', 'ignore'))
        data_dict = demjson.decode(data_text.replace('var jsonData = ', '').strip(';'))
        news_list = data_dict["list"]
        news_res_list = []
        for news_block in news_list:
            try:
                category = news_block['channel']['title']
                news_title = news_block['title']
                news_url = news_block['url']
                news_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(news_block['time']))
                news_res_list.append({"title": news_title, "url": news_url, "category": category, "time": news_time})
            except Exception, e:
                print e
        return news_res_list


    @classmethod
    def fetch_news_100(cls):
        """
        从新浪新闻日常取一百条新闻
        :return:
        """
        res = requests.get(
            'http://roll.news.sina.com.cn/interface/rollnews_ch_out_interface.php?col=89&num=100&page=1')
        data_text = unicode(res.content.decode('gbk', 'ignore'))
        data_dict = demjson.decode(data_text.replace('var jsonData = ', '').strip(';'))
        news_list = data_dict["list"]
        news_res_list = []
        for news_block in news_list:
            try:
                category = news_block['channel']['title']
                news_title = news_block['title']
                news_url = news_block['url']
                news_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(news_block['time']))
                news_res_list.append({"title": news_title, "url": news_url, "category": category, "time": news_time})
            except Exception, e:
                print e
        return news_res_list


    @classmethod
    def fetch_news_by_day(cls, date):
        """
        以历史上某日为时间点取新闻,2000条
        例如:date=2014-05-22
        :param date:
        :return:
        """
        res = requests.get(
            'http://roll.news.sina.com.cn/interface/rollnews_ch_out_interface.php?col=89&num=2000&page=1&date=%s' % str(date))
        data_text = unicode(res.content.decode('gbk', 'ignore'))
        data_dict = demjson.decode(data_text.replace('var jsonData = ', '').strip(';'))
        news_list = data_dict["list"]
        news_res_list = []
        for news_block in news_list:
            try:
                category = news_block['channel']['title']
                news_title = news_block['title']
                news_url = news_block['url']
                news_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(news_block['time']))
                news_res_list.append({"title": news_title, "url": news_url, "category": category, "time": news_time})
            except Exception, e:
                print e
        return news_res_list


# page = requests.get('http://sports.sina.com.cn/cba/2018-03-29/doc-ifysthxa5037874.shtml')
# # print page.content
# print SinaNewsExtract.extract_title(page.content)
# print SinaNewsExtract.extract_keywords(page.content)
# print SinaNewsExtract.extract_pub_time(page.content)
# print SinaNewsExtract.extract_content(page.content)
# # for link in SinaNewsExtract.extract_link(page.content)["article_link"]:
# #     print link
# print SinaNewsExtract.comment_cnt(page.content)
#
# page = requests.get('https://news.sina.cn/gn/2018-03-26/detail-ifysreum7903100.d.html')
# print page.content
# print SinaNewsExtract.extract_title(page.content, device='phone')
# print SinaNewsExtract.extract_pub_time(page.content, device='phone')
# print SinaNewsExtract.extract_content(page.content, device='phone')
#
# # for link in SinaNewsExtract.extract_link(page.content)["site_link"]:
# #     print link
# SinaNewsExtract.comment_cnt(page.content, device='phone')

# SinaNewsBrief.fetch_news_10000()



