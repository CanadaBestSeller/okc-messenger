#!/usr/bin/env python3

import logging
import socketserver
import sys

from messenger.request_handler import RequestHandler

# Logging
LOG_NAME = 'log.txt'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


def main():
    serving_host, serving_port = sys.argv[1], int(sys.argv[2])
    initialize_logger()
    consume(serving_host, serving_port)


def consume(serving_host, serving_port):
    logging.info("Serving requests @ {}:{}".format(serving_host, serving_port))
    while True:
        server = socketserver.TCPServer((serving_host, serving_port), RequestHandler)
        server.serve_forever()


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
