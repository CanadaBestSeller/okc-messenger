#!/usr/bin/env python3

import logging
import os
import sys
import time

# This is a root-level Python file, and as such, should not have relative imports
from messenger.debugger import Debugger
from messenger.consumer import Consumer

# Creative Controls
FIRST_MESSAGE = "You seem fun and silly, with a good head on your shoulders :) " \
                "I wouldn't mind exploring the possibility of enhancing your life and exposing you to my awesomeness"

# Consumer Controls
QUEUE_FILE_NAME = 'queue-messages.txt'
DEBUGGER_INPUT_FILE = 'add-links-here-to-debug.txt'
HOST = 'localhost'
DEFAULT_TIMEOUT_IN_SECONDS = 3
CONSUMPTION_CYCLE_DELAY_IN_SECONDS = 2

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
    debugger = Debugger(DEBUGGER_INPUT_FILE, HOST, outbound_port)
    consumer = Consumer(HOST, inbound_port, outbound_port, DEFAULT_TIMEOUT_IN_SECONDS, USERNAME, PASSWORD)
    while True:
        try:
            logging.info("Finished.\n\n\n---------- Consuming from CONSUMER ----------")
            consumer.consume()
            time.sleep(CONSUMPTION_CYCLE_DELAY_IN_SECONDS)

            logging.info("Finished.\n\n\n---------- Consuming from DEBUGGER ----------")
            debugger.consume()
            time.sleep(CONSUMPTION_CYCLE_DELAY_IN_SECONDS)
        except KeyboardInterrupt:
            consumer.close()
            logging.info("Finished.\n\n\nProgram ended.")
            break


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
