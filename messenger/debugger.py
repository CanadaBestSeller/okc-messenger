#!/usr/bin/env python3

import logging

from messenger.communication import Request, Sender


class Debugger(object):
    """
    Consume links from given file
    Sends message call to outbound_port which can be picked up by Consumer
    """

    def __init__(self, input_file, outbound_host, outbound_port):
        self.input_file = input_file
        self.outbound_host = outbound_host
        self.outbound_port = outbound_port
        logging.info('{0} initialized'.format(self))

        open(self.input_file, 'w').close()  # clear input_file
        logging.info('{0} input file ({1}) cleared'.format(self, input_file))

        self._sender = Sender(self.outbound_host, self.outbound_port)

    def __repr__(self):
        return '<OKC-messenger Debugger. Destination: {0}:{1}>'.format(self.outbound_host, self.outbound_port)

    def consume(self):
        if Debugger.has_input_in(self.input_file):
            popped_line = Debugger.pop_first_line_from_file(self.input_file)
            logging.info("Debugger is processing popped line:\n'{0}'".format(popped_line))
            self._process_debugger_line(popped_line)
        else:
            logging.info("Debugger queue is empty.")

    def _process_debugger_line(self, line):
        sanitized_line = line.strip()
        if len(sanitized_line) == 0:
            logging.warn("Popped line is empty. Skipping.")
            return
        if Debugger.link_is_not_valid(line):
            logging.warn("Popped line is not a valid link. Skipping.")
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
        return Request(match_id, handle)
