#!/usr/bin/python

import time
import logging

from queue_entry import QueueEntry


def consume(inbound_port, outbound_port):
    while True:
        logging.info("Finished consumption.\n\n---------- Consuming from DEBUGGER ----------")
        consume_from_debugger(inbound_port, outbound_port)
        time.sleep(1)

        logging.info("Finished consumption.\n\n---------- Consuming from QUEUE ----------")
        consume_from_queue()
        time.sleep(1)


def consume_from_debugger(inbound_port, outbound_port):
    debugger_lines = open(DEBUGGER_QUEUE_NAME).readlines() # grab all the lines
    if len(debugger_lines) > 0:
        # delete first line (pop queue)
        open(DEBUGGER_QUEUE_NAME, 'w').writelines(debugger_lines[1:])
        popped_line = debugger_lines[0]
        logging.info("Debugger is processing popped line:\n'{0}'".format(popped_line))
        process_debugger_line(popped_line, inbound_port)
    else:
        logging.info("Debugger queue is empty.")


def process_debugger_line(line, destination):
    sanitized_line = line.strip()
    if len(sanitized_line) == 0:
        logging.warn("Popped line is empty. Skipping.")
        return
    if linkIs_not_valid(line):
        logging.warn("Popped line is not a valid link. Skipping.")
        return

    handle = link_to_handle(sanitized_line)
    queue_entry = generate_queue_entry(handle)
    send_to_port(queue_entry, destination)


def send_to_port(queue_entry, destination):
    import json
    serialized_queue_entry = json.dumps(queue_entry)
    logging.info("NOT IMPLEMENTED")
    logging.info("Sending message to port {1}:\n{0}".format(serialized_queue_entry, destination))


def linkIs_not_valid(link):
    from urllib.parse import urlparse
    return len(urlparse(link).scheme) == 0


def link_to_handle(line):
    from urllib.parse import urlparse
    return urlparse(line).path.split('/')[2]


def generate_queue_entry(handle):
    import hashlib
    hasher = hashlib.md5()
    hasher.update(handle.encode('utf-8'))
    match_id = 'manual-' + hasher.hexdigest()[:8].upper()
    return QueueEntry(match_id, handle)


def consume_from_queue():
    return


def initialize_consumer(inbound_port, outbound_port):
    logging.info("Initializing OKC Message Consumer...")
    logging.info("INBOUND port @ {0} for receiving messages.".format(inbound_port))
    logging.info("OUTBOUND port @ {0} for sending notifications.".format(outbound_port))
    initialize_debugger()
    initialize_queue()


def initialize_debugger():
    reset_debugger_queue()
    logging.info("Initializing Debugger... DONE")


def initialize_queue():
    logging.info("Initializing Queue... DONE")


def reset_debugger_queue():
    open(DEBUGGER_QUEUE_NAME, 'w').close()


