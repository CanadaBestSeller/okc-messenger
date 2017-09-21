#!/usr/bin/env python3

import logging
import socketserver

from messenger.communication import Receiver
from messenger.okc_message_sender import OkcMessageSender
from messenger.session import Session


class Consumer(socketserver.BaseRequestHandler):
    """
    Consume message calls from inbound port.
    Sends notifications to outbound port when reply has been received.
    """

    def __init__(self, host, serving_port, username, password):
        self.host = host
        self.inbound_port = serving_port
        self.username = username
        self.password = password

        logging.info("Consuming messages @ {}.".format(self.host, self.inbound_port))

    def handle(self):
        data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        self.process(data)

    def process(self, data):
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())

    def send_message(self):
        current_session = Session(self.username, self.password)
        sender = OkcMessageSender(current_session)

    def close(self):
        # Close shit up
        pass
