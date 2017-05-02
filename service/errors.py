# -*- coding: utf-8 -*-

class ForbiddenError(Exception):
    """
    :class: ForbiddenError

    403 禁止访问
    """
    def __init__(self):
        self.status_code = 403

    def __repr__(self):
        return "{'msg': 'forbidden'}"


class NotfoundError(Exception):
    """
    :class: NotfoundError

    404 not found
    """
    def __init__(self):
        self.status_code = 404

    def __repr__(self):
        return "{'msg': 'notfound'}"
