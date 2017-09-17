#!/usr/bin/env python3

import logging
from messenger.communication import Receiver
from messenger.okc_message_sender import OkcMessageSender
from messenger.session import Session


class Consumer(object):
    """
    Consume message calls from inbound port.
    Sends notifications to outbound port when reply has been received.
    """

    def __init__(self, host, inbound_port, outbound_port, default_timeout, username, password):
        self.host = host
        self.inbound_port = inbound_port
        self.outbound_port = outbound_port
        self.default_timeout = default_timeout
        self.username = username
        self.password = password

        self._receiver = Receiver('OKC Messenger Consumer', host, inbound_port, default_timeout)

        logging.info("INBOUND port @ {0} for receiving messages.".format(self.inbound_port))
        logging.info("OUTBOUND port @ {0} for sending notifications.".format(self.outbound_port))

    def consume(self, timeout=None):
        self._receiver.receive(timeout or self.default_timeout)
        logging.info("Consuming stuff...")

    def send_message(self):
        current_session = Session(self.username, self.password)
        sender = OkcMessageSender(current_session)

    def close(self):
        # Close shit up
        pass
