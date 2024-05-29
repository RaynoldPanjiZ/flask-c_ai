# from PyQt5.QtWebKit import QWebView
import sys, os

from threading import Thread
from multiprocessing import Process, Queue, Value
import time

from webapp.routes3 import app
from gevent import pywsgi

from flask_cors import CORS
import logging

PORT = 5000


## flask thread  https://codereview.stackexchange.com/a/114307
class FlaskThread(object):
    def __init__(self, application):
        self.application = application
        # logging.basicConfig(level=logging.INFO)
        # self.application.debug = True

    def start(self):
        http_server = pywsgi.WSGIServer(('0.0.0.0', PORT), self.application)
        http_server.serve_forever()
        # self.application.run(host='0.0.0.0', port=PORT)
        print('server run')



def qtApp(app):
    # Initialize the app
    # app.config.from_object(AppConfiguration)
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    # api = Api(app)

    webapp = FlaskThread(app)
    webapp.start()



if __name__ == '__main__':
    sys.exit(qtApp(app))
