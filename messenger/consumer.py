#!/usr/bin/env python3

import logging


class Consumer(object):
    """
    Consume message calls from inbound port.
    Sends notifications to outbound port when reply has been received.
    """

    def __init__(self, inbound_port, outbound_port):
        self.inbound_port = inbound_port
        self.outbound_port = outbound_port
        logging.info("INBOUND port @ {0} for receiving messages.".format(self.inbound_port))
        logging.info("OUTBOUND port @ {0} for sending notifications.".format(self.outbound_port))

    def consume(self):
        logging.info("Consuming stuff...")
