# -*- coding:utf-8 -*-
import sys
import re
from bs4 import BeautifulSoup
import json
import demjson
import time
from config.news_crawler.xinhua_news.xinhua_news_conf import sub_site_dict
from config.news_crawler.xinhua_news.xinhua_news_conf import xinhua_session
from config.news_crawler.xinhua_news.xinhua_news_conf import xinhua_headers
from model.news_crawler.html2article.html2article import Html2Article
from model.sentiment_calc.dict_based_demo.senti_calc_dict import SentiCalc
reload(sys)
sys.setdefaultencoding('utf-8')


class XinhuaNewsExtractor():
    """
    网易新闻页解析类,主要是获取标题与链接列表
    """

    @classmethod
    def legal_url(cls, url):
        """
        判断链接地址是否为网易新闻站内链接
        :param url:
        :return: 返回对应子站即文章分类,不合法返回None
        """
        for sub_site in sub_site_dict:
            if sub_site in url:
                return sub_site_dict[sub_site]
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
                if cls.legal_url(link):
                    if ('htm' in link or 'html' in link) and ('0000-00/00' in num_star_str):
                        article_link.append(link.strip('/'))
                    else:
                        site_link.append(link.strip('/'))
            return {"article_link": article_link, "site_link": site_link}
        except Exception, e:
            print e
        return {"article_link": [], "site_link": []}


    @classmethod
    def news_info_by_url(cls, url):
        """
        抽取整理一篇文章的信息,通过他的地址
        :param url:
        :return:
        """
        try:
            res = xinhua_session.get(url, headers=xinhua_headers, timeout=10)
            page_content = res.content
            # print page_content
            title_pattern = re.compile(u'<title>([\w\W]*?)</title>')
            time_pattern_1 = re.compile(u'(20\d\d-\d\d-\d\d \d\d:\d\d:\d\d)')
            time_pattern_2 = re.compile(u'(20\d\d年\d\d月\d\d日 \d\d:\d\d:\d\d)')
            title = re.findall(title_pattern, page_content)[0].split('-')[0].strip()
            pub_time_list = re.findall(time_pattern_1, unicode(page_content))
            # 两种日期格式,都试一下
            if len(pub_time_list) > 0:
                pub_time = pub_time_list[0]
            else:
                pub_time = re.findall(time_pattern_2, unicode(page_content))[0].replace(u'年', '-').replace(u'月', '-').replace(u'日', '')
            article_content = Html2Article.url2article(url)
            category = cls.legal_url(url)
            polarity = SentiCalc.score_calc(title)


            news_info = {"title": title, "time": pub_time, 'url': url, "content": article_content, "category": category, "polarity": polarity}
            return news_info
        except Exception, e:
            print e
            return None



# print XinhuaNewsExtractor.news_info_by_url('http://ent.news.cn/2018-04/03/c_1122628808.htm')









