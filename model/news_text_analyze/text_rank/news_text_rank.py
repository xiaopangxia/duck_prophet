# -*- coding:utf-8 -*-
import sys
import requests
from elasticsearch import Elasticsearch
from textrank4zh import TextRank4Keyword
from textrank4zh import TextRank4Sentence
reload(sys)
sys.setdefaultencoding('utf-8')



class NewsTextRank():
    """
    新闻关键词
    """
    @classmethod
    def news_keywords(cls, news_text, key_num, key_len):
        """
        生产新闻文章关键词
        :param new_text:新闻文本
        :param key_num: 关键词数量
        :return: 关键词列表
        """
        tr4w = TextRank4Keyword()
        tr4w.analyze(text=news_text, lower=True, window=4, vertex_source="no_stop_words", edge_source="no_stop_words")
        keywords_list = tr4w.get_keywords(key_num, word_min_len=key_len)
        return keywords_list

    @classmethod
    def news_keywords_23(cls, news_text):
        """
        组合关键词套餐,2个字与3个以上
        :param new_text:
        :return:
        """
        key_list_2 = cls.news_keywords(news_text, 20, 2)
        key_list_3 = cls.news_keywords(news_text, 50, 3)
        for item in key_list_2:
            if len(item['word']) < 3:
                key_list_3.append(item)
        for item in key_list_3:
            item["weight"] = int(round(item["weight"]*3001))  # 把权值放大
            item["text"] = item["word"]  # 为了做jquery词云,加一项text
        return key_list_3


    @classmethod
    def news_summary(cls, news_text):
        """
        返回top3的摘要句
        :param new_text:
        :return:
        """
        tr4s = TextRank4Sentence()
        tr4s.analyze(text=news_text, lower=True, source="all_filters")
        summary_list = []
        for item in tr4s.get_key_sentences(num=3):
            summary_list.append(item.sentence)

        return summary_list




# text_test = ""
# res_list = NewsKeywords.news_keywords_23(text_test)
# for item in res_list:
#     print item['word'], item["weight"]
