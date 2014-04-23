#!/usr/bin/env python
# fixture - remote presence
# 2014 AKA MEDIA SYSTEM

from handlers.BaseHandler import BaseHandler
import logging
import datetime
from bson import json_util
import tornado
from tornado import gen
import ResponseObject
import requests

class FixtureHandler(BaseHandler):
    """Accept a URL and timestamp submission; do topic analysis"""
    def __init__(self, *args, **kwargs):
        BaseHandler.__init__(self,  *args, **kwargs)  

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        
        logging.debug('hit the fixture endpoint')
        if self.isAuth():
            logging.info('we are authenticated and ready to debug data')
            # timestamp = datetime.datetime.utcnow()
            logging.info(self.get_arguments())
        else:
            self.write('Something is wack in FixtureHandler, self.isAuth wasnt True.')