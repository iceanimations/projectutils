from abc import ABCMeta, abstractproperty
from . import server as _server


class SObjectMeta(ABCMeta):

    subclasses = dict()

    def __new__(mcls, name, bases, namespace):
        for _name, _member in namespace.copy().items():
            if isinstance(_member, FuncOverride):
                def _wrapper(self, *args, **kwargs):
                    return _member.func(
                            self.conn, self.search_key, *args, **kwargs)
                _wrapper.__name__ = _name
                _wrapper.__doc__ = _member.func.__doc__
                namespace[_name] = _wrapper
        cls = super(SObjectMeta, mcls).__new__(mcls, name, bases, namespace)
        _server.TacticObjectServer.register_sobject_class(cls)
        return cls


class RelatedSObject(object):
    __stype__ = ''
    __show_retired__ = False

    def __init__(self, stype, show_retired=False):
        self.__stype__ = stype
        self.__show_retired__ = show_retired

    def __get__(self, obj, cls):
        return obj.conn.eval('@SOBJECT(%s[id, %s].%s)' % (
            obj.__stype__, obj.id, self.__stype__))


class ParentSObject(RelatedSObject):
    __key__ = None

    def __init__(self, stype, key, show_retired=False):
        super(ParentSObject, self).__init__(stype, show_retired=show_retired)
        self.__key__ = key

    def __get__(self, obj, cls):
        return obj.conn.query(
                self.__stype__,
                filters=[('code', obj.get_field(self.__key__))],
                show_retired=self.__show_retired__, single=True)

    def __set__(self, obj, value):
        if isinstance(value, SObject):
            value = value.code
        obj.__data__[self.__key__] = value


class ChildSObject(RelatedSObject):

    def __get__(self, obj, cls):
        return obj.conn.eval('@SOBJECT(%s)' % self.__stype__, obj.search_key)


class SObjectField(object):
    __key__ = None
    __force__ = False

    def __init__(self, key, force=True):
        self.__key__ = key
        self.__force__ = force

    def __get__(self, obj, cls):
        ''':retval: str'''
        if self.__key__ in obj.__data__:
            return obj.__data__[self.__key__]
        elif self.__force__ and self.__key__ in obj.conn.get_column_names(
                cls.__stype__):
            self.__data__ = obj.conn.get_by_search_key(obj.search_key).__data__
        else:
            raise AttributeError('%s is not a valid key for %s object' % (
                self.__key__, obj.__stype__))


class FuncOverride(object):
    func = None

    def __init__(self, func):
        self.func = func


class SObject(object):
    __metaclass__ = SObjectMeta
    conn = _server.Connection()
    __data__ = None

    search_key = SObjectField('__search_key__')
    code = SObjectField('code', True)
    description = SObjectField('description', True)
    id = SObjectField('id', True)
    name = SObjectField('name', True)
    retire_status = SObjectField('retire_status', True)
    status = SObjectField('status', True)
    timestamp = SObjectField('timestamp', True)

    snapshots = ChildSObject('sthpw/snapshot')
    tasks = ChildSObject('sthpw/task')

    def __init__(self, data, conn=None):
        self.conn = conn
        stype, code = self.conn.split_search_key(data['__search_key__'])
        stype = stype.split('?')[0]
        self.__data__ = data
        if stype == self.__stype__:
            self.__data__ = {
                    key: value if value is not None else ''
                    for key, value in data.items()}
        else:
            raise TypeError(
                    'provided data does not refer to an %s object' %
                    self.__stype__)

    @abstractproperty
    def __stype__(self):
        pass

    def __repr__(self):
        skey = self.__data__['__search_key__']
        return self.__class__.__name__ + "({'__search_key__': '%s'})" % skey

    @property
    def data(self):
        return self.__data__

    def get_field(self, key):
        return self.__data__[key]

    def set_field(self, key, value):
        self.__data__[key] = value

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

    @classmethod
    def get_by_code(cls, code):
        return cls.conn.get_by_code(cls.__stype__, code)

    @classmethod
    def get_by_search_key(cls, search_key):
        data = cls.conn.get_by_search_key(search_key)
        _server.TacticObjectServer.wrap_sobject_class(data, cls.conn)

    @classmethod
    def get_unique_sobject(cls):
        return cls(cls.conn.get_unique_sobject(cls.__stype__))

    @classmethod
    def get_column_names(cls):
        return cls.conn.get_column_names(cls.__stype__)

    def connect_sobject(self, dest, context='default'):
        return self.conn.connect_sobjects(
                self.search_key, dest.search_key, context)
    connect_sobject.__doc__ = _server.TacticObjectServer.__doc__

    def insert_update(self, metadata={}, parent_key=None, info={},
                      use_id=False, triggers=False):
        obj = self.conn.insert_update(
                self.search_key, self.__data__, metadata=metadata,
                parent_key=None, info=info, use_id=use_id, triggers=False)
        self.__data__ = obj.__data__
        return obj
    insert_update.__doc__ = _server.TacticObjectServer.insert_update.__doc__

    def insert(self, *args, **kwargs):
        return self.conn.insert(
                self.search_key, self.__data__, *args, **kwargs)
    insert.__doc__ = _server.TacticObjectServer.insert.__doc__

    def update(self, *args, **kwargs):
        return self.conn.update(
                self.search_key, self.__data__, *args, **kwargs)
    update.__doc__ = _server.TacticObjectServer.update.__doc__

    reactivate = FuncOverride(
            _server.TacticObjectServer.reactivate_sobject)
    retire = FuncOverride(
            _server.TacticObjectServer.retire_sobject)
    update = FuncOverride(
            _server.TacticObjectServer.update)
    delete = FuncOverride(
            _server.TacticObjectServer.delete_sobject)
    simple_checkin = FuncOverride(
            _server.TacticObjectServer.simple_checkin)
    group_checkin = FuncOverride(
            _server.TacticObjectServer.group_checkin)
    directory_checkin = FuncOverride(
            _server.TacticObjectServer.directory_checkin)
    checkout = FuncOverride(
            _server.TacticObjectServer.checkout)
    get_snapshot = FuncOverride(
            _server.TacticObjectServer.get_snapshot)
    get_parent = FuncOverride(
            _server.TacticObjectServer.get_parent)
    get_all_children = FuncOverride(
            _server.TacticObjectServer.get_all_children)
    get_connected_sobject = FuncOverride(
            _server.TacticObjectServer.get_connected_sobject)
    get_connected_sobjects = FuncOverride(
            _server.TacticObjectServer.get_connected_sobjects)


class UnknownSObject(SObject):
    __stype__ = '*'

    def __new__(cls, data, conn=None):
        self = super(UnknownSObject, cls).__new__(cls, data, conn)
        self.__stype__ = cls.conn.get_stype(data)
        return self
