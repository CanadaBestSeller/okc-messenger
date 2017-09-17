class QueueEntry(dict):

    def __init__(self, match_id, match_handle, message):
        dict.__init__(self, match_id=match_id)
        dict.__init__(self, match_handle=match_handle)
        dict.__init__(self, message=message)

    def __init__(self, match_id, match_handle):
        dict.__init__(self, match_id=match_id)
        dict.__init__(self, match_handle=match_handle)
        dict.__init__(self, message='')
