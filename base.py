from abc import ABCMeta, abstractproperty
from . import server as _server


class SObjectMeta(ABCMeta):

    subclasses = dict()

    def __new__(mcls, name, bases, namespace):
        cls = super(SObjectMeta, mcls).__new__(mcls, name, bases, namespace)
        _server.ProjectServer.register_sobject_class(cls)
        return cls


class RelatedSObject(object):
    __stype__ = ''
    __show_retired__ = False

    def __init__(self, stype, show_retired=False):
        self.__stype__ = stype
        self.__show_retired__ = show_retired

    def __get__(self, obj, cls):
        return obj.conn.eval('@SOBJECT(%s[code, %s].%s)' % (
            obj.search_type, obj.code, self.__stype__))


class ParentSObject(RelatedSObject):
    __key__ = None

    def __init__(self, stype, key, show_retired=False):
        super(ParentSObject, self).__init__(stype, show_retired=show_retired)
        self.__key__ = key

    def __get__(self, obj, cls):
        return obj.conn.get_parent(
                self.__stype__, obj.search_key, self.__show_retired__)

    def __set__(self, obj, value):
        if isinstance(value, SObject):
            value = value.code
        obj.__data__[self.__key__] = value


class ChildSObject(RelatedSObject):

    def __get__(self, obj, cls):
        return obj.conn.get_all_children(obj.search_key, self.__stype__)


class SObjectField(object):
    __key__ = None
    __force__ = False

    def __init__(self, key, force=False):
        self.__key__ = key
        self.__force__ = force

    def __get__(self, obj, cls):
        if self.__key__ in obj.__data__:
            return obj.__data__[self.__key__]
        elif self.__force__ and self.__key__ in obj.conn.get_column_names(
                cls.__stype__):
            self.__data__ = obj.conn.get_by_search_key(obj.search_key).__data__
        else:
            raise AttributeError('%s is not a valid key for %s object' % (
                self.__key__, obj.__stype__))


class SObject(object):
    __metaclass__ = SObjectMeta
    conn = _server.Connection()
    __data__ = None

    search_key = SObjectField('__search_key__')
    code = SObjectField('code', True)
    description = SObjectField('description')
    id = SObjectField('id', True)
    name = SObjectField('name', True)
    retire_status = SObjectField('retire_status')
    status = SObjectField('status')
    timestamp = SObjectField('timestamp')

    snapshots = ChildSObject('sthpw/snapshot')
    tasks = ChildSObject('sthpw/task')

    def __init__(self, data, conn=None):
        self.conn = conn
        stype, code = self.conn.split_search_key(data['__search_key__'])
        stype = stype.split('?')[0]
        if stype == self.search_type:
            self.__data__ = data
        else:
            raise TypeError(
                    'provided data does not refer to an %s object' %
                    self.search_type)

    def __stype__(self):
        pass

    def __repr__(self):
        skey = self.__data__['__search_key__']
        return self.__class__.__name__ + "({'__search_key__': '%s'})" % skey

    @property
    def search_type(cls):
        return cls.__stype__

    def delete(self, include_dependencies=False):
        self.conn.delete_sobject(
                self.search_type(), include_dependencies=include_dependencies)

    @classmethod
    def query(cls, filters=[], columns=[], order_bys=[], show_retired=False,
              limit=None, offset=None, single=False):
        result = cls.conn.query(
                cls.__stype__, filters=filters, columns=columns,
                order_bys=order_bys, show_retired=show_retired, limit=limit,
                offset=offset, single=single)
        if single:
            if not result:
                return None
            else:
                return cls(result.__data__, conn=cls.conn)
        return [cls(res.__data__, conn=cls.conn) for res in result]

    @classmethod
    def fast_query(cls, filters=[], limit=None):
        return cls.conn.fast_query(cls.__stype__, filters=filters, limit=None)

    def get_all_children(self, child_type):
        return self.conn.update(self.search_key, child_type)

    def update(self, args, **kwargs):
        return self.conn.update(self.search_key, include_dependencies=False)

    def insert(self, metadata={}, parent_key=None, info={}, use_id=False,
               triggers=True):
        return self.conn.insert(
                self.search_type, self.__data__, metadata=metadata,
                parent_key=parent_key, info=info, use_id=use_id,
                triggers=triggers)

    @classmethod
    def get_by_code(cls, code):
        data = cls.server.get_by_code(cls.search_type, code)
        if data:
            return cls(data, server=cls.server)

    @classmethod
    def get_by_search_key(cls, search_key):
        data = cls.conn.get_by_search_key(search_key)
        _server.ProjectServer.wrap_sobject_class(data, cls.conn)

    @classmethod
    def get_unique_sobject(cls):
        return cls(cls.server.get_unique_sobject(cls.search_type()))

    def insert_update(self, metadata={}, parent_key=None, info={},
                      use_id=False, triggers=False):
        data = self.conn.insert_update(
                self.search_key, self.__data__, metadata=metadata,
                parent_key=None, info=info, use_id=use_id, triggers=False)
        self.__data__ = data

    def retire(self):
        return self.conn.retire_sobject(self.search_key)

    def reactivate(self):
        return self.conn.reactivate_object(self.search_key)

    def get_field(self, key):
        return self.__data__[key]

    def set_field(self, key, value):
        self.__data__[key] = value


class UnknownSObject(SObject):
    __stype__ = '*'

    def __init__(self, data, server=None):
        self.__stype__ = _server.ProjectServer.get_stype(data)
        super(UnknownSObject, self).__init__(data, server)
