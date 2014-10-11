#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = "jiangjun"

import os
import shutil
import tornado.web
import tornado.httpserver
from tornado.options import define, options

define("port", default=8888, type=int)


class MainHanlder(tornado.web.RequestHandler):

    def get(self):

        self.render("index.html")


class UploadHandler(tornado.web.RequestHandler):

    '''handle the upload request
    '''

    def initialize(self):

        self.upload_path = os.path.join(os.getcwd(), "upload")
        self.file_name = self.get_argument("resumableFilename", "data")
        self.tmp_dir = os.path.join(
            self.upload_path,
            self.get_argument("resumableIdentifier")
        )
        self.chunk = os.path.join(
            self.tmp_dir,
            "part" + str(self.get_argument("resumableChunkNumber"))
        )
        self.chunk_num = int(self.get_argument("resumableChunkNumber"))
        self.chunk_size = int(self.get_argument("resumableChunkSize"))
        self.total_size = int(self.get_argument("resumableTotalSize"))

    def prepare(self):
        pass

    def get(self):
        '''first, if the file to be uploaded exists, do nothing.
            when the chunk to be uploaded exists, we return status code 200, 
           otherwise return 404, so that this chunk could be posted again.
        '''
        if os.path.exists(os.path.join(self.upload_path, self.file_name)):
            self.set_status(200)
        elif os.path.exists(self.chunk):
            self.set_status(200)
        else:
            self.set_status(404)

    def post(self):
        '''save every chunk uploaded to a temporary directory, 
           and name the file as "part"+resumableChunkNumber
        '''

        if not os.path.exists(self.tmp_dir):
            os.mkdir(self.tmp_dir)

        with open(self.chunk, "wb") as f:
            f.write(self.request.files["file"][0]["body"])

        self.check_complete()

    def check_complete(self):
        '''check if all the chunks have been uploaded, if so, 
           concatenate all the chunks.
        '''

        uploaded_chunk_size = self.chunk_num * self.chunk_size
        current_chunk_size = int(self.get_argument("resumableCurrentChunkSize"))

        if uploaded_chunk_size + current_chunk_size >= self.total_size:
            
            save_path = os.path.join(self.upload_path, self.file_name )
            with open(save_path, "w+") as f:
                for i in range(1, self.chunk_num + 1):
                    chunk_file = os.path.join(
                        self.tmp_dir,
                        "part" + str(i)
                    )
                    with open(chunk_file) as g:
                        f.write(g.read())
            self.remove_tmpfiles()

    def remove_tmpfiles(self):
        
        if os.path.exists(self.tmp_dir):
            shutil.rmtree(self.tmp_dir)


class Application(tornado.web.Application):

    def __init__(self):

        handlers = [
            (r"/", MainHanlder),
            (r"/upload", UploadHandler)
        ]

        settings = {
            "static_path": os.path.join(os.path.dirname(__file__), "static"),
            "debug": True
        }

        tornado.web.Application.__init__(self, handlers, **settings)


def main():

    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
