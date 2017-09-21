#!/usr/bin/env python3

import json
import logging
import os
import socketserver

from messenger.communication import Request
from messenger.okc_message_sender import OkcMessageSender
from messenger.session import Session

# Creative Controls
FIRST_MESSAGE = "You seem fun and silly, with a good head on your shoulders :) " \
                "I wouldn't mind exploring the possibility of enhancing your life by exposing you to my awesomeness"

# Credentials (username & password)
USERNAME = os.environ.get('OKC_USERNAME')
PASSWORD = os.environ.get('OKC_PASSWORD')


class RequestHandler(socketserver.BaseRequestHandler):
    """
    Handles requests from inbound port.
    Sends notifications back when request has been served.
    """

    # Contract
    def handle(self):
        self.data = self.request.recv(1024).strip()
        json_data = json.loads(self.data.decode())
        logging.info('Received request from {}:\n{}'.format(self.client_address[0], json.dumps(json_data, indent=4)))
        request = Request(**json_data)
        RequestHandler.process(request)

    # Contract
    def setup(self): pass

    # Contract
    def finish(self): pass

    def close(self): pass

    @staticmethod
    def process(request):
        if request['request_type'] == 'send-message':
            RequestHandler.send_message(request)

    @staticmethod
    def send_message(request):
        logging.info("{} : {}".format(USERNAME, PASSWORD))
        current_session = Session.login(USERNAME, PASSWORD)

        message = request['data'] or FIRST_MESSAGE
        logging.info("Sending message to {}".format(request['match_handle']))
        logging.info("Message:\n{}".format(message))

        sender = OkcMessageSender(current_session)
        sender.send(username=request['match_handle'], message=message)
