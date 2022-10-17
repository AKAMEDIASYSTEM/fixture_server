#!/usr/bin/env python
# fixture - remote presence
# 2014 AKA MEDIA SYSTEM

from handlers.BaseHandler import BaseHandler
import logging
import datetime
import tornado
from tornado import gen
import ResponseObject
import requests
import groups
import state

'''
implementing this on your own? You need a file called groups.py with your keys.

this is what groups.py should look like. It should be one directory above FixtureHandler.py.

#!/usr/bin/env python
# fixture - remote presence
# 2014 AKA MEDIA SYSTEM
grouplist = [
    {'id':'YOUR_ID', 'token':'A_SECRET_TOKEN_YOU_MADE_UP'},
    {'id':'ANOTHER_ID_IF_YOU_WANT', 'token':'ANOTHER_SCRET_TOKEN'}
]

'''

class FixtureHandler(BaseHandler):

    """Accept a file (CSV) with accelerometer samples in it"""
    def __init__(self, *args, **kwargs):
        BaseHandler.__init__(self,  *args, **kwargs)
        logging.info(state.lastState)  

    # @tornado.web.asynchronous
    # @tornado.gen.coroutine
    def post(self):
        logging.info('hit the fixture endpoint')
        # logging.info(self.request)
        self.payload = self.get_argument('fixture_payload')
        if self.isAuth():
            logging.info('we are authenticated and ready to debug data')
            # timestamp = datetime.datetime.utcnow()
            logging.info(self.payload)
            for line in self.payload.split('\n'):
                entries = line.split(',')
                if len(entries) % 4 == 0: # sanity check to make sure we are dealing with a full deck, so to speak
                    self.process(entries)
                
            ''' here is an example line of payload:
            1398221223683,-5.5385894775390625,-0.2913665771484375,7.8047637939453125
            that is: UTC timestamp in millis, X, Y, and Z.
            X, Y, and Z are in degrees ranging (-180,180)
            Map this to the (0,255) range for RGB Neopixel values.
            '''
        else:
            self.write('Something is wack in FixtureHandler, self.isAuth wasnt True.')

    def mapVals(self, val, inMin, inMax, outMin, outMax):
        toRet = float(outMin + (float(outMax - outMin) * (float(val - inMin) / float(inMax - inMin))))
        # return clamp(toRet, outMin, outMax)
        return toRet

    def get(self):
        logging.info("someone hit the fixture GET endpoint")
        if self.isAuth():
            logging.info("they are authorized to hit the GET endpoint")
            logging.info(state.lastState)
        else:
            logging.info("we rejected a GET attempt due to failed authentication")
            logging.info(self)

    def process(self, entries):
        logging.info(entries)
        l = int(len(entries)/4)
        logging.info('there are %s entries to parse' % l)

        for i in reversed(range(l)):
            logging.info('i is %s' % i)
            # thisTime = entries[i*4-4]
            pX = int(self.mapVals(float(entries[i*4-3]), -180.0, 180.0, 0.0, 255))
            pY = int(self.mapVals(float(entries[i*4-2]), -180.0, 180.0, 0.0, 255))
            pZ = int(self.mapVals(float(entries[i*4-1]), -180.0, 180.0, 0.0, 255))
            logging.info('mapped x is %s' % pX)
            logging.info('mapped y is %s' % pY)
            logging.info('mapped z is %s' % pZ)
            state.lastState = [pX, pY, pZ]
            seq = (str(pX), str(pY), str(pZ))
            toSend = ','.join(seq)
            logging.info('done processing %s ' % state.lastState)
