#!/usr/bin/env python3

import logging
import sys
import time

from messenger.communication import Request, Sender

# Controls
INPUT_FILE = 'add-links-here-to-debug.txt'
CYCLE_IN_SECONDS = 2

# Logging
LOG_NAME = 'log.txt'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


def main():
    debugging_host, debugging_port = sys.argv[1], sys.argv[2]
    initialize_logger()
    debugger = Debugger(INPUT_FILE, debugging_host, debugging_port)  # Attach to inbound to simulate real input
    logging.info('\n'
                 '\n---'
                 '\nInitialized debugging for {}:{}. To test, add links to "{}"'
                 '\n---'
                 '\n'.format(debugger.destination_host, debugger.destination_port, debugger.input_file))
    while True:
        debugger.consume()
        time.sleep(CYCLE_IN_SECONDS)


class Debugger(object):
    """
    Consume links from given file
    Sends message call to destination_port which can be picked up by Consumer
    """

    def __init__(self, input_file, destination_host, destination_port):
        self.input_file = input_file
        self.destination_host = destination_host
        self.destination_port = destination_port
        logging.info('{0} initialized'.format(self))

        open(self.input_file, 'w').close()  # clear input_file
        logging.info('{0} input file ({1}) cleared'.format(self, input_file))

        self._sender = Sender('OKC Messenger Debugger', self.destination_host, self.destination_port)

    def __repr__(self):
        return '<OKC-messenger Debugger. Destination: {0}:{1}>'.format(self.destination_host, self.destination_port)

    def consume(self):
        if Debugger.has_input_in(self.input_file):
            popped_line = Debugger.pop_first_line_from_file(self.input_file)
            logging.info("Debugger is processing popped line:\n'{0}'".format(popped_line))
            self._process_debugger_line(popped_line)

    def close(self):
        pass

    def _process_debugger_line(self, line):
        sanitized_line = line.strip()
        if len(sanitized_line) == 0:
            logging.warning("Popped line is empty. Skipping.")
            return
        if Debugger.link_is_not_valid(line):
            logging.warning("Popped line is not a valid link. Skipping.")
            return

        handle = Debugger.link_to_handle(sanitized_line)
        message_request = Debugger.generate_message_request(handle)
        self._sender.send(message_request)

    @staticmethod
    def has_input_in(input_file): return len(open(input_file).readlines()) > 0

    @staticmethod
    def pop_first_line_from_file(input_file):
        lines = open(input_file).readlines()  # grab all the lines
        open(input_file, 'w').writelines(lines[1:])  # delete first line (pop queue)
        return lines[0]

    @staticmethod
    def link_is_not_valid(link):
        from urllib.parse import urlparse
        return len(urlparse(link).scheme) == 0

    @staticmethod
    def link_to_handle(line):
        from urllib.parse import urlparse
        return urlparse(line).path.split('/')[2]

    @staticmethod
    def generate_message_request(handle):
        import hashlib
        hash_generator = hashlib.md5()
        hash_generator.update(handle.encode('utf-8'))
        match_id = 'debug-' + hash_generator.hexdigest()[:8].upper()
        return Request(match_id=match_id,
                       match_handle=handle,
                       platform='okc',
                       request_type='send-message')


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
