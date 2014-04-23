#!/usr/bin/env python
# fixture - remote presence
# 2014 AKA MEDIA SYSTEM

import datetime
import json
import logging
import tornado
from tornado import gen
import tornado.ioloop
import tornado.web
import tornado.options
import tornado.template
from bson import json_util
import ResponseObject
import traceback

class BaseHandler(tornado.web.RequestHandler):

    def __init__(self, *args, **kwargs):
        # logging.debug('entering init funciton of BaseHandler')
        try:
            tornado.web.RequestHandler.__init__(self,  *args, **kwargs)
            self.set_header("Access-Control-Allow-Origin", "*")
            #self.set_header("Content-Type", "text/html")
            self.token = self.get_argument('token')
            self.id = self.get_argument('id')
            self.response = ResponseObject.ResponseObject()
        except Exception as reason:
            print reason, traceback.format_exc()

    
    def write_response(self):
        try:
            self.write(self.response.response)
        except Exception as reason:
            print reason, traceback.format_exc()
            print self.response.response

    def isAuth(self):
        logging.info('entering isAuth function in BaseHandler')
        return (dict({'id':self.id, 'token':self.token}) in groups.grouplist)