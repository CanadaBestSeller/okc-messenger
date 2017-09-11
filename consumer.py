#!/usr/bin/python

import time
import sys
import logging

from queue_entry import *

# Constants
LOG_NAME = 'consumer.log'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
QUEUE_FILE_NAME = 'queue-messages.txt'
DEBUGGER_QUEUE_NAME = 'add-https-links-here.txt'

def main():
    inbound_port, outbound_port = sys.argv[1], sys.argv[2] 
    initialize(inbound_port, outbound_port)
    consume(inbound_port, outbound_port)

def initialize(inbound_port, outbound_port):
    initializeLogger()
    initializeConsumer(inbound_port, outbound_port)

def consume(inbound_port, outbound_port):
    while True:
        logging.info("Finished consumption.\n\n---------- Consuming from DEBUGGER ----------")
        consumeFromDebugger(inbound_port, outbound_port)
        time.sleep(1)

        logging.info("Finished consumption.\n\n---------- Consuming from QUEUE ----------")
        consumeFromQueue()
        time.sleep(1)

def consumeFromDebugger(inbound_port, outbound_port):
    debugger_lines = open(DEBUGGER_QUEUE_NAME).readlines() # grab all the lines
    if len(debugger_lines) > 0:
        # delete first line (pop queue)
        open(DEBUGGER_QUEUE_NAME, 'w').writelines(debugger_lines[1:])
        popped_line = debugger_lines[0]
        logging.info("Debugger is processing popped line:\n'{0}'".format(popped_line))
        processDebuggerLine(popped_line, inbound_port)
    else:
        logging.info("Debugger queue is empty.")
        
def processDebuggerLine(line, destination):
    sanitized_line = line.strip()
    if len(sanitized_line) == 0:
        logging.warn("Popped line is empty. Skipping.")
        return
    if linkIsNotValid(line):
        logging.warn("Popped line is not a valid link. Skipping.")
        return

    handle = linkToHandle(sanitized_line)
    queue_entry = generateQueueEntry(handle)
    sendToPort(queue_entry, destination)

def sendToPort(queue_entry, destination):
    import json
    serialized_queue_entry = json.dumps(queue_entry)
    logging.info("NOT IMPLEMENTED")
    logging.info("Sending message to port {1}:\n{0}".format(serialized_queue_entry, destination))

def linkIsNotValid(link):
    from urllib.parse import urlparse
    return len(urlparse(link).scheme) == 0

def linkToHandle(line):
    from urllib.parse import urlparse
    return urlparse(line).path.split('/')[2]

def generateQueueEntry(handle):
    import hashlib
    hasher = hashlib.md5()
    hasher.update(handle.encode('utf-8'))
    match_id = 'manual-' + hasher.hexdigest()[:8].upper()
    return QueueEntry(match_id, handle)

def consumeFromQueue():
    return

def initializeConsumer(inbound_port, outbound_port):
    logging.info("Initializing OKC Message Consumer...")
    logging.info("INBOUND port @ {0} for receiving messages.".format(inbound_port))
    logging.info("OUTBOUND port @ {0} for sending notifications.".format(outbound_port))
    initializeDebugger()
    initializeQueue()

def initializeDebugger():
    resetDebuggerQueue()
    logging.info("Initializing Debugger... DONE")

def initializeQueue():
    logging.info("Initializing Queue... DONE")

def resetDebuggerQueue():
    open(DEBUGGER_QUEUE_NAME, 'w').close()

def initializeLogger():
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

if __name__ == '__main__': main()
