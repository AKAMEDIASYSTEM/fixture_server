#!/usr/bin/env python
# fixture - remote presence
# 2014 AKA MEDIA SYSTEM
# 2022 resurrected

import datetime
import logging
import os
import tornado
import tornado.ioloop
import tornado.web
import tornado.options
import tornado.template
import groups
import state


from handlers.FixtureHandler import FixtureHandler
from handlers.FixtureGiver import FixtureGiver

if __name__ == '__main__':
    for g in groups.grouplist:
        state.userStates[g.id] = [0.0,0.0,0.0]
    logging.info(states.userStates)
    tornado.options.define('debug', default=True, type=bool, help=(
        "Turn on autoreload"
    ))
    tornado.options.logging = 'debug'
    tornado.options.parse_command_line()
    lastState = [0.0,0.0,0.0]
    this_dir = os.path.dirname(__file__)
    static_path = os.path.join(this_dir, 'static')
    application = tornado.web.Application([
            (r'/fixture', FixtureHandler),
            (r'/fixget', FixtureGiver)
        ], lastState=lastState)
        # ])

    static_path=static_path
    debug=tornado.options.options.debug

    logging.info('Listening on http://localhost:8888')
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()