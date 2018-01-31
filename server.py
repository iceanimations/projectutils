from auth import user as USER
import types


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


class ProjectServer(USER.TacticServer):

    _sobject_classes = {}

    def __init__(self, A, *args, **kwargs):
        self.server = A.server

    def create_copy(self):
        return ProjectServer(USER.get_server_copy())

    @classmethod
    def register_sobject_class(cls, sobj_cls):
        stype = getattr(sobj_cls, '__stype__', None)
        if isinstance(stype, basestring):
            cls._sobject_classes[stype] = sobj_cls

    @classmethod
    def get_sobject_class(self, stype):
        return self._sobject_classes.get(stype, None)

    @classmethod
    def get_stype(self, sobj_dict):
        stype, _ = _server.split_search_key(sobj_dict['__search_key__'])
        return stype.split('?')[0]

    @classmethod
    def wrap_sobject_class(cls, sobject, conn=None):
        stype = ProjectServer.get_stype(sobject)
        sobject_class = cls.get_sobject_class(stype)
        if sobject_class is None:
            sobject_class = cls.get_sobject_class('*')
        return sobject_class(sobject, conn=conn)

    @classmethod
    def get_stypes(cls, namespace=None):
        ''':type namespace: str or None'''
        if namespace is None:
            return cls._sobject_classes.keys()
        else:
            namespace = namespace.rstrip('/')
            return [stype for stype in cls._sobject_classes.keys() if
                    stype.startswith(namespace+'/')]

    @classmethod
    def get_sobject_classes(cls, namespace=None):
        if namespace is None:
            return cls._sobject_classes.values()
        else:
            namespace = namespace.rstrip('/')
            return [_class for stype, _class in cls._sobject_classes.items() if
                    stype.startswith(namespace + '/')]

    @staticmethod
    def is_sobj_dict(d):
        return isinstance(d, dict) and '__search_key__' in d

    def __getattr__(self, name):
        attr = super(ProjectServer, self).__getattr__(name)
        if isinstance(attr, types.FunctionType):
            def _another_wrapper(*args, **kwargs):
                result = attr(*args, **kwargs)
                if ProjectServer.is_sobj_dict(result):
                    result = ProjectServer.wrap_sobject_class(result, self)
                elif isinstance(result, list) and all(
                        (True if ProjectServer.is_sobj_dict(member)
                            else False for member in result)):
                    result = [ProjectServer.wrap_sobject_class(mem, self)
                              for mem in result]
                return result
            return _another_wrapper
        return attr


class Connection(object):

    def __init__(self, server=None):
        self._conn = server

    def __get__(self, obj, cls=None):
        return getattr(obj, '_conn', None) or self._conn or _server

    def __set__(self, obj, value):
        if value is _server:
            value = None
        if obj is None:
            self._conn = value
        else:
            obj._conn = value

try:
    from auth import user as USER
    set_user(USER.get_user())
    set_server(ProjectServer(USER.get_server()))
except Exception as e:
    _user = None
    from auth import user as USER
    set_server(ProjectServer(USER.TacticServer(setup=False)))
