#!/usr/bin/env python3

import logging
import json
import socket

from datetime import datetime

MAX_TCP_CONNECTIONS = 5
MAX_BYTES_RECEIVABLE = 64*64


class Request(dict):
    """
    Easy de/serialization because we're inheriting from dictionary. Works nicely with Python's json module:
    serialized_request = json.dumps(Request('a', 'b'))
    deserialized_request = Request(**(json.loads(serialized_request))
    """
    def __init__(self, match_id, match_handle, platform=None, request_type=None, data=None, metadata=None, request_id=None):
        dict.__init__(self, match_id=match_id)
        dict.__init__(self, match_handle=match_handle)
        dict.__init__(self, platform=platform or '')
        dict.__init__(self, request_type=request_type or '')
        dict.__init__(self, data=data or '')
        dict.__init__(self, metadata=metadata or '')
        dict.__init__(self, request_id=request_id or str(datetime.utcnow()))


class Sender(object):
    def __init__(self, identifier, destination_host, destination_port):
        self.identifier = identifier
        self.destination_host = destination_host
        self.destination_port = destination_port
        logging.info("Initialized {}".format(self.__repr__()))

    def send(self, message_request):
<<<<<<< HEAD
        self._socket = socket.socket()
=======
>>>>>>> eeb7478f87ee913d4394ff926fa670e9c916b003
        self._socket.connect((self.destination_host, int(self.destination_port)))
        self._socket.send(json.dumps(message_request).encode())
        logging.info("Sent to {}".format(self.destination_host, self.destination_port))

        received = self._socket.recv(1024)
        logging.info("Received: {}".format(received))

        self._socket.close()

    def __repr__(self):
        return '<{0} Sender @ {1}:{2}>'.format(self.identifier, self.destination_host, self.destination_port)


class Receiver(object):
    def __init__(self, identifier, inbound_host, inbound_port, default_timeout):
        self.identifier = identifier
        self.inbound_host = inbound_host
        self.inbound_port = inbound_port
        self.default_timeout = default_timeout

        s = socket.socket()
        # s.bind((inbound_host, inbound_port))
        s.settimeout(default_timeout)
        s.listen(MAX_TCP_CONNECTIONS)
        self._socket = s

    def receive(self, timeout=None):
        self._socket.settimeout(timeout or self.default_timeout)
        try:
            connection, address = self._socket.accept()
            buffer = connection.recv(MAX_BYTES_RECEIVABLE)
            if len(buffer) > 0:
                print(buffer)
        except socket.timeout:
            return None

    def __repr__(self):
        return '<{0} Receiver @ {1}:{2}>'.format(self.identifier, self.inbound_host, self.inbound_port)

