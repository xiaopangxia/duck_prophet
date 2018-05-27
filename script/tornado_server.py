# -*- coding:utf-8 -*-
import sys
import tornado
import tornado.web
import tornado.ioloop
import tornado.escape
from tornado.httpserver import HTTPServer
from model.web_service.tornado_elasticsearch import TornadoElasticsearch
import json
reload(sys)
sys.setdefaultencoding('utf-8')


# tornado服务脚本
class MainHandler(tornado.web.RequestHandler):
    def post(self):
        target = self.get_argument("target")
        if target == "news_search":
            # 获取舆情,新闻列表
            print self.request.body
            query_body = json.loads(self.request.body)
            print query_body
            try:
                page_num = self.get_argument("page_num")
            except Exception, e:
                page_num = 1
            res = TornadoElasticsearch.news_search(query_body, page_num)
            if res:
                res_json = json.dumps(res)
                self.write(res_json)
            else:
                self.write("500")
        elif target == "news_analyze":
            # 单篇分析
            query_body = json.loads(self.request.body)
            res = TornadoElasticsearch.news_analyze(query_body)
            if res:
                res_json = json.dumps(res)
                self.write(res_json)
            else:
                self.write("500")
        elif target == "topic_trend":
            # 话题趋势
            query_body = json.loads(self.request.body)
            res = TornadoElasticsearch.topic_trend(query_body)
            if res:
                res_json = json.dumps(res)
                self.write(res_json)
            else:
                self.write("500")
        else:
            self.write("bad request!")




    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Content-type', 'application/json')


application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()















