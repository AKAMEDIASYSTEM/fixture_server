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

class FixtureGiver(BaseHandler):

    """Accept a file (CSV) with accelerometer samples in it"""
    def __init__(self, *args, **kwargs):
        BaseHandler.__init__(self,  *args, **kwargs)

    def mapVals(self, val, inMin, inMax, outMin, outMax):
        toRet = float(outMin + (float(outMax - outMin) * (float(val - inMin) / float(inMax - inMin))))
        # return clamp(toRet, outMin, outMax)
        return toRet

    def get(self):
        logging.info("hit the fixtureGIVER GET endpoint")
        theUser = self.isAuth()
        if theUser:
            logging.info("they are authorized to hit the GET endpoint")
            logging.info(state.userStates[theUser])
            responseString = str(state.userStates[theUser])
            self.write(responseString[1:-1])
        else:
            logging.info("we rejected a GET attempt due to failed authentication")
            logging.info(self.token)

