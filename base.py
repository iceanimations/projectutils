from abc import ABCMeta, abstractproperty
from .server import Server


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

    def __init__(self, data, server=None):
        self.__data__ = data
        self.server = server

    @abstractproperty
    def __stype__(self):
        pass

    @classmethod
    def search_type(cls):
        return cls.__stype__

    @classmethod
    def query(cls, *args, **kwargs):
        cls.server.query(cls.__stype__, *args, **kwargs)
    query.__doc__ = server.query.__doc__

    def update(self, *args, **kwargs):
        self.server.update(self.search_key())

    def insert(self):
        pass

    def search_key(self):
        return self.__data__['__search_key__']

    @classmethod
    def get_unique_sobject(cls):
        return cls(cls.server.get_unique_sobject(cls.search_type()))
    get_unique_sobject.__doc__ = server.__doc__

    @class
