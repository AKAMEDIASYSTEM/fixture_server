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
import groups

class FixtureHandler(BaseHandler):

    """Accept a file (CSV) with accelerometer samples in it"""
    def __init__(self, *args, **kwargs):
        BaseHandler.__init__(self,  *args, **kwargs)  

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        
        logging.debug('hit the fixture endpoint')
        if self.isAuth():
            logging.info('we are authenticated and ready to debug data')
            # timestamp = datetime.datetime.utcnow()
            logging.info(self.request.files['fixture_payload'][0]['body'])
            for line in self.request.files['fixture_payload'][0]['body'].split('\n'):
                entries = line.split(',')
                if len(entries) % 4 == 0: # sanity check to make sure we are dealing with a full deck, so to speak
                    self.process(entries)
                
            ''' here is an example line of payload:
            1398221223683,-5.5385894775390625,-0.2913665771484375,7.8047637939453125
            that is: UTC timestamp in millis, X, Y, and Z.
            X, Y, and Z are in meters per second per second, so when lying on a table, Z=-9.8
            so in general, each axis can vary from 11 to -11. 
            Map this to the (0,255) range for RGB Neopixel values.

            for line in fixture_payload[0]['body']:
                vars = line.split(',')
                look at the timestamp, vars[0]
                if the timestamp is more than INTERVAL from last update sent:
                    # this means we have been motionless for longer than INTERVAL, so we should send (thisTimestamp-lastTimestamp)/INTERVAL duplicate updates
                    # so the neopixel reports the right amount of motionlessness
                    updateSpark(last_scaledX, last_scaledY, last_scaledZ)
                else:
                    # we are up-to-date, send this one out
                    scaledX = map(vars[0])
                    scaledY = map(vars[1])
                    scaledZ = map(vars[2])
                    updateSpark(scaledX, scaledY, scaledZ)
                    last_scaledX = map(vars[0])
                    last_scaledY = map(vars[1])
                    last_scaledZ = map(vars[2])
            '''
        else:
            self.write('Something is wack in FixtureHandler, self.isAuth wasnt True.')

    def mapVals(val, inMin, inMax, outMin, outMax):
        toRet = float(outMin + (float(outMax - outMin) * (float(val - inMin) / float(inMax - inMin))))
        # return clamp(toRet, outMin, outMax)
        return toRet

    def process(entries, self):
        l = len(entries)/4
        logging.info('there are %s entries to parse' % l)
        for i in reversed(range(l-1)):
            thisTime = entries[i*4-4]
            thisX = self.mapVals(entries[i*4-3], -11.0, 11.0, 0.0, 255)
            thisY = self.mapVals(entries[i*4-2], -11.0, 11.0, 0.0, 255)
            thisZ = self.mapVals(entries[i*4-1], -11.0, 11.0, 0.0, 255)
            logging.info('mapped x is %s' % thisX)
            logging.info('mapped y is %s' % thisY)
            logging.info('mapped z is %s' % thisZ)
            seq = (thisX, thisY, thisZ)
            toSend = ','.join(seq)
            logging.info('about to try to send %s ' % toSend)
            self.updateSpark(toSend)

    def updateSpark(textData, self):
        payment = {'access_token':groups.keylist['spark_token'],'args':textData}
        url = groups.url
        q = requests.post(url,data=payment)
        logging.info(q.url)
        logging.info(q.text)
        logging.info(q.status_code)