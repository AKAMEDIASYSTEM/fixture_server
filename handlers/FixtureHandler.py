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

class SubmitHandler(BaseHandler):
    """Accept a URL and timestamp submission; do topic analysis"""
    def __init__(self, *args, **kwargs):
        BaseHandler.__init__(self,  *args, **kwargs)  

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        
        logging.debug('hit the submit endpoint')
        if self.isAuth():
            db = self.settings['db']
            url = self.get_argument('url')
            groupID = self.get_argument('groupID')
            timestamp = datetime.datetime.utcnow()

            # populate Pages collection
            db.pages.update(
                {'url':url, 'groupID':groupID},
                {'$push' : {'timestamp':timestamp}, '$set' : {'latest':timestamp}},
                upsert=True
                )
            # HERE is where to add check-if-recently-queried function
            '''
            if db.pages.find(url:theUrl).count() != 0: #ie, if url has been seen before AND has been seen within THRESHOLD minutes
                # get info about latest visit before this one
                d = db.pages.find(url:theUrl)
                theTimestamp = d['latest']
                timestamp_now = datetime.datetime.utcnow()

                # update the pages store
                db.pages.update(
                    {'url':url},
                    {'$push':{'timestamp':timestamp_now}, '$set':{'latest':timestamp_now}},
                    upsert=True
                    )

                # then update all topics and keywords with the same timestamp
                # by pushing timestamp_now to their respective timestamp[] arrays
                db.keywords.update(
                    {timestamp:{'$in':theTimestamp}},
                    {'$push':{'timestamp':timestamp_now}, '$set' : {'latest':timestamp_now}},
                    upsert=True
                    )
                db.topics.update(
                    {timestamp:{'$in':theTimestamp}},
                    {'$push':{'timestamp':timestamp_now}, '$set' : {'latest':timestamp_now}},
                    upsert=True
                    )

            '''

            # request keyword data
            payload = {
                "url" : url,
                "apikey" : keys['APIKEY'],
                "maxRetrieve" : 10,
                "outputMode" : "json"
                }
            r = requests.get(keys['apiKeywords'], params=payload)
            j = r.json()

            # populate Keywords collection
            if j['status'] == 'OK':
                for k in j['keywords']:
                    if k['relevance'] >= 0.5:
                        d = db.keywords.update(
                            {'keyword':k['text'], 'groupID':groupID},
                            {'$push' : {'timestamp':timestamp, 'url':url}, '$set' : {'latest':timestamp}},
                            upsert=True
                            )

            payload['linkedData'] = 0
            payload['showSourceText'] = 0
            r2 = requests.get(keys['apiConcepts'], params=payload)
            j2 = r2.json()
            logging.debug(j2)
            if j2['status'] == 'OK':
                for c in j2['concepts']:
                    if c['relevance'] >= 0.5:
                        d = db.topics.update(
                            {'topic':c['text'], 'groupID':groupID},
                            {'$push' : {'timestamp':timestamp, 'url':url}, '$set' : {'latest':timestamp}},
                            upsert=True
                            )
        else:
            self.write('Something is wack in SubmitHandler, probably your code.')