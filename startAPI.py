#!/usr/bin/env python
# fixture_server to receive sensor packets

import datetime
import logging
import os
from pymongo import MongoClient
import tornado
import tornado.ioloop
import tornado.web
import tornado.options
import tornado.template


from handlers.FixtureHandler import FixtureHandler



if __name__ == '__main__':

    tornado.options.define('debug', default=True, type=bool, help=(
        "Turn on autoreload"
    ))
    tornado.options.logging = 'debug'
    tornado.options.parse_command_line()

    # client = MongoClient(tz_aware=True)
    # db = client.listening_table
    this_dir = os.path.dirname(__file__)
    static_path = os.path.join(this_dir, 'static')
    application = tornado.web.Application([
            (r'/fixture', FixtureHandler),
        ], db=db)

    static_path=static_path
    debug=tornado.options.options.debug

    logging.info('Listening on http://localhost:80')
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()