from abc import ABCMeta, abstractproperty
from .server import Server
import functools


class SObjectMeta(ABCMeta):

    subclasses = dict()

    def __new__(mcls, name, bases, namespace):
        cls = super(ABCMeta, mcls).__new__(mcls, name, bases, namespace)
        return cls


class RelatedSObject(object):
    __stype__ = ''
    __key__ = None

    def __init__(self, stype, key):
        self.__stype__ = stype
        self.__key__ = key

    def __get__(self, obj, cls):
        pass

    def __set__(self, obj, server):
        pass


class ParentSObject(RelatedSObject):
    pass


class ChildSObject(RelatedSObject):
    pass


class SObjectField(object):
    __key__ = None

    def __init__(self, key):
        self.__key__ = key

    def __get__(self, obj, cls):
        return obj.__data__[self.__key__]


class SObject(object):
    __metaclass__ = SObjectMeta
    server = Server()
    __data__ = None
    search_key = SObjectField('__search_key__')

    def __init__(self, data, server=None):
        self.__data__ = data
        self.server = server

    def __stype__(self):
        pass

    @property
    def search_type(cls):
        return cls.__stype__

    def delete(self, include_dependencies=False):
        self.server.delete_sobject(
                self.search_type(), include_dependencies=include_dependencies)

    @classmethod
    def query(cls, filters=[], columns=[], order_bys=[], show_retired=False,
              limit=None, offset=None, single=True):
        result = cls.server.query(
                cls.__stype__, filters=filters, column=columns,
                order_bys=order_bys, show_retired=show_retired, limit=limit,
                offset=offset, single=single)
        if single:
            if not result:
                return None
            else:
                return cls(result, server=cls.server)
        return [cls(res, server=cls.server) for res in result]
    query.__doc__ = server.query.__doc__

    @classmethod
    def fast_query(cls, filters=[], limit=None):
        return [cls(res, server=cls.server) for res in cls.server.fast_query()]

    def get_all_children(cls, child_type):
        pass

    def update(self, args, **kwargs):
        self.server.update(self.search_key, include_dependencies=False)

    def insert(self):
        pass

    def search_key(self):
        return self.__data__['__search_key__']

    @classmethod
    def get_unique_sobject(cls):
        return cls(cls.server.get_unique_sobject(cls.search_type()))
    get_unique_sobject.__doc__ = server.__doc__

