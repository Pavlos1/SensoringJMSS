#!/usr/bin/env python
# coding: utf-8
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
import werkzeug.serving

import app

@werkzeug.serving.run_with_reloader
def runServer():
    http_server = WSGIServer(('',app.app.port), app.my_app, handler_class=WebSocketHandler)
    http_server.serve_forever()
