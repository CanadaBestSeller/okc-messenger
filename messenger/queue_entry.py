#!/usr/bin/env python3


class QueueEntry(dict):

    def __init__(self, match_id, match_handle, message=None):
        dict.__init__(self, match_id=match_id)
        dict.__init__(self, match_handle=match_handle)
        dict.__init__(self, message=message or '')
