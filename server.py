from auth import user as USER
import types


_server = None


def set_server(server):
    global _server
    _server = server


def get_server():
    return _server


class TacticObjectServerMeta(USER.TacticServerMeta):
    '''Wraps Return Calls TacticServerMeta from wrapping the objects again'''

    @classmethod
    def _wrap(mcls, func):

        # TODO: how to wrap other attrs such as project_code

        func_name = func.__name__

        def _object_wrapper(self, *args, **kwargs):

            real_func = getattr(self.real_server, func_name)

            result = real_func(*args, **kwargs)
            if TacticObjectServer.is_sobj_dict(result):
                result = TacticObjectServer.wrap_sobject_class(
                        result, self)
            elif isinstance(result, list) and all(
                    (True if TacticObjectServer.is_sobj_dict(member)
                        else False for member in result)):
                result = [TacticObjectServer.wrap_sobject_class(mem, self)
                          for mem in result]
            return result
        _object_wrapper.__name__ = func_name
        _object_wrapper.__doc__ = func.__doc__

        return _object_wrapper


class TacticObjectServer(USER.TacticServer):
    __metaclass__ = TacticObjectServerMeta

    _sobject_classes = {}

    def __new__(cls, obj, *args, **kwargs):
        new_obj = super(TacticObjectServer, cls).__new__(cls, *args, **kwargs)
        new_obj.real_server = obj
        return new_obj

    def create_copy(self):
        return TacticObjectServer(USER.get_server_copy())

    @classmethod
    def register_sobject_class(cls, sobj_cls):
        stype = getattr(sobj_cls, '__stype__', None)
        if isinstance(stype, basestring):
            cls._sobject_classes[stype] = sobj_cls
            setattr(cls, sobj_cls.__name__, sobj_cls)

    @classmethod
    def get_sobject_class(self, stype):
        return self._sobject_classes.get(stype, None)

    @classmethod
    def get_stype(self, sobj_dict):
        stype, _ = _server.split_search_key(sobj_dict['__search_key__'])
        return stype.split('?')[0]

    @classmethod
    def wrap_sobject_class(cls, sobject, conn=None):
        stype = TacticObjectServer.get_stype(sobject)
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
        return getattr(self.real_server, name)


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

set_server(TacticObjectServer(USER.get_server()))
