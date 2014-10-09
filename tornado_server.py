#!/usr/bin/env python
# -*- coding:utf-8 -*-


import os
import tornado.web
import tornado.httpserver
from tornado.options import define, options

define("port", default=8880, type=int)


class MainHanlder(tornado.web.RequestHandler):
    
    def get(self):
        self.render("index.html")

@tornado.web.stream_request_body
class UploadHandler(tornado.web.RequestHandler):

    def initialize(self):
        print self.request.headers

    def post(self):
        pass

    def data_received(self, chunk):
        with open("data","wb") as f:
            f.write(chunk)

class Application(tornado.web.Application):
    
    def __init__(self):
        
        handlers = [
            (r"/", MainHanlder),
            (r"/upload", UploadHandler)
        ]

        settings = {
            "static_path": (os.path.dirname(__file__), "static"),
            "debug":True
        }

        tornado.web.Application.__init__(self,handlers,**settings)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()