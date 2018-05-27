#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
#Html2Article.py:基于统计的正文提取
import urllib
import urllib2
import zlib
import cookielib
import re
import requests
import sys

# 有了这个脚本,文章正文提取通用搞定
# 是基于字符密度统计的方法,不算完美,可以接受

threshold_of_article = 180  #maybe not good enough.
class Html2Article():

    @classmethod
    def get_html(cls, url):
        try:
            cookie = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
            headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
            request = urllib2.Request(url=url, headers=headers)
            request.add_header('Accept-encoding', 'gzip,utf-8')
            #print request.headers
            response = opener.open(request)
            html = response.read()
            gzipped = response.headers.get('Content-Encoding')
            if gzipped:
                html = zlib.decompress(html, 16+zlib.MAX_WBITS)
            try:
                re_type = re.compile(r'charset=".*?"')
                char_type = re_type.search(html).group()
            except Exception, e:
                char_type = "utf8"
            if len(char_type) >= 10:
                #print char_type[9:-1]
                char_type = char_type[9:-1].upper()
            else:
                char_type = "utf8"
            if html:
                try:
                    return html.decode(char_type).encode('UTF-8')
                except Exception, e:
                    return html.decode('gbk').encode('UTF-8')
            else:
                return None
        except Exception, e:
            return None

    @classmethod
    def html2Article(cls, html_file):
        #首先去除可能导致误差的script和css，之后再去标签
        tempResult = re.sub('<script([\s\S]*?)</script>','',html_file)
        tempResult = re.sub('<style([\s\S]*?)</style>','',tempResult)
        tempResult = re.sub('(?is)<.*?>','',tempResult)
        tempResult = tempResult.replace(' ','')
        tempResultArray = tempResult.split('\n')
        #print tempResult

        data = []
        string_data = []
        result_data = ''
        summ = 0
        count = 0

        #计算长度非零行的行数与总长度
        for oneLine in tempResultArray:
            if(len(oneLine)>0):
                data.append(len(oneLine))
                string_data.append(oneLine)
                summ += len(oneLine)
                count += 1
        #print 'averange is:'+ str(summ/count)
        for oneLine in string_data:
            #if len(oneLine) >= summ/count+180:
            if len(oneLine) >= 180:
                # print oneLine
                result_data += oneLine
        return result_data


    @classmethod
    def url2article(cls, url):
        """
        输入文章链接,输出页面正文内容
        :param url:
        :return:
        """
        html_data = cls.get_html(url)
        if html_data:
            article_content = cls.html2Article(html_data)
            return article_content
        else:
            return None

# print Html2Article.url2article('http://theory.people.com.cn/n1/2018/0329/c40531-29895329.html')

# 头条不行,防爬
# print requests.get('https://www.toutiao.com/a6538522070295249421/').content
