#!/usr/bin/env python3

import logging
import os
import sys
import time

# This is a root-level Python file, and as such, should not have relative imports
from messenger.debugger import Debugger
from messenger.consumer import Consumer

# Consumer controls
CONSUMPTION_CYCLE_DELAY = 2
QUEUE_FILE_NAME = 'queue-messages.txt'
DEBUGGER_INPUT_FILE = 'add-links-here-to-debug.txt'

# Logging
LOG_NAME = 'log.txt'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Credentials (username & password)
USERNAME = os.environ.get('OKC_USERNAME')
PASSWORD = os.environ.get('OKC_PASSWORD')


def main():
    inbound_port, outbound_port = sys.argv[1], sys.argv[2]
    initialize_logger()
    consume(inbound_port, outbound_port)


def consume(inbound_port, outbound_port):
    debugger = Debugger(DEBUGGER_INPUT_FILE, outbound_port)
    consumer = Consumer(inbound_port, outbound_port)
    while True:
        logging.info("Finished.\n\n\n---------- Consuming from DEBUGGER ----------")
        debugger.consume()
        time.sleep(CONSUMPTION_CYCLE_DELAY)

        logging.info("Finished.\n\n\n---------- Consuming from CONSUMER ----------")
        consumer.consume()
        time.sleep(CONSUMPTION_CYCLE_DELAY)


def initialize_logger():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    log_formatter = logging.Formatter(LOG_FORMAT)

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(log_formatter)

    file_handler = logging.FileHandler(LOG_NAME)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(log_formatter)

    root_logger.addHandler(stdout_handler)
    root_logger.addHandler(file_handler)

    logging.info("Loggers successfully initialized.")

if __name__ == '__main__':
    main()
