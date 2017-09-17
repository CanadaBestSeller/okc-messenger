#!/usr/bin/python

import sys
import logging

from messenger import consumer

LOG_NAME = 'log.txt'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
QUEUE_FILE_NAME = 'queue-messages.txt'
DEBUGGER_QUEUE_NAME = 'add-https-links-here.txt'

def main():
    inbound_port, outbound_port = sys.argv[1], sys.argv[2]
    initialize_logger()
    initialize_consumer(inbound_port, outbound_port)

    consume(inbound_port, outbound_port)


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
