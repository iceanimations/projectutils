_server = None
_user = None


def set_server(server):
    global _server
    _server = server


def set_user(user):
    global _user
    _user = user


def get_user():
    return _user


def get_server():
    return _server


class Server(object):
    """Server Property for SObjects"""
    def __init__(self, server=None):
        self._server = server if server else _server

    def __get__(self, obj, cls=None):
        return obj._server if obj._server else _server

    def __set__(self, obj, server):
        obj._server = server if server else self._server

try:
    from auth import user as USER
    set_user(USER.get_user())
    set_server(USER.get_server())
except Exception as e:
    _user = None
    from auth import user as USER
    set_server(USER.TacticServer(setup=False))
