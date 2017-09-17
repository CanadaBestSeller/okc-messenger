#!/usr/bin/env python3

import logging

from .queue_entry import QueueEntry


class Debugger(object):
    """
    Consume links from given file
    Sends message call to outbound_port which can be picked up by Consumer
    """

    def __init__(self, input_file, outbound_port):
        self.input_file = input_file
        self.outbound_port = outbound_port
        open(self.input_file, 'w').close()  # clear input_file

    def consume(self):
        if Debugger.has_input_in(self.input_file):
            popped_line = Debugger.pop_first_line_from_file(self.input_file)
            logging.info("Debugger is processing popped line:\n'{0}'".format(popped_line))
            Debugger.process_debugger_line(popped_line, self.outbound_port)
        else:
            logging.info("Debugger queue is empty.")

    @staticmethod
    def has_input_in(input_file): return len(open(input_file).readlines()) > 0

    @staticmethod
    def pop_first_line_from_file(input_file):
        lines = open(input_file).readlines()  # grab all the lines
        open(input_file, 'w').writelines(lines[1:])  # delete first line (pop queue)
        return lines[0]

    @staticmethod
    def get_lines_from_input_file(input_file): return

    @staticmethod
    def process_debugger_line(line, destination):
        sanitized_line = line.strip()
        if len(sanitized_line) == 0:
            logging.warn("Popped line is empty. Skipping.")
            return
        if Debugger.link_is_not_valid(line):
            logging.warn("Popped line is not a valid link. Skipping.")
            return

        handle = Debugger.link_to_handle(sanitized_line)
        queue_entry = Debugger.generate_queue_entry(handle)
        Debugger.send_to_port(queue_entry, destination)

    @staticmethod
    def link_is_not_valid(link):
        from urllib.parse import urlparse
        return len(urlparse(link).scheme) == 0

    @staticmethod
    def link_to_handle(line):
        from urllib.parse import urlparse
        return urlparse(line).path.split('/')[2]

    @staticmethod
    def generate_queue_entry(handle):
        import hashlib
        hash_generator = hashlib.md5()
        hash_generator.update(handle.encode('utf-8'))
        match_id = 'debug-' + hash_generator.hexdigest()[:8].upper()
        return QueueEntry(match_id, handle)

    @staticmethod
    def send_to_port(queue_entry, destination):
        import json
        serialized_queue_entry = json.dumps(queue_entry)
        logging.info("NOT IMPLEMENTED")
        logging.info("Sending message to port {1}:\n{0}".format(serialized_queue_entry, destination))
