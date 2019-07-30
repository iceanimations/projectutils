import abc


class TwoWayDependency(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def __source_tag__(self):
        pass

    @abc.abstractproperty
    def __target_tag__(self):
        pass

    @abc.abstractproperty
    def __keyword__(self):
        pass

    def __init__(self, direction='forward', single=False):
        self._snapshot = None
        self._single = single
        self._direction = str(direction)
        self._context = None
        self._version = -1
        self._versionless = False

    def __repr__(self):
        return '%s: %s for %r' % (
                self.__class__.__name__, self.tag,
                self._context if self._context else self._snapshot)

    def __get__(self, obj, cls):
        new_obj = self.copy()
        new_obj._context = obj
        return new_obj

    def set_version(self, version):
        self._version = int(version)

    def set_versionless(self, versionless):
        self._versionless = bool(versionless)

    def set_snapshot(self, snapshot):
        self._snapshot = snapshot.copypa
        self._version = snapshot.version

    def copy(self):
        new_obj = self.__class__()
        new_obj._single = self._single
        new_obj._direction = self._direction
        new_obj._snapshot = self._snapshot
        new_obj._context = self._context
        new_obj._version = self._version
        new_obj._versionless = self._versionless
        return new_obj

    @property
    def source_tag(self):
        return '_'.join([self.__keyword__, self.__source_tag__])

    @property
    def target_tag(self):
        return '_'.join([self.__keyword__, self.__target_tag__])

    @property
    def snapshot(self):
        if self._snapshot is None:
            self._snapshot = self._context.get_snapshot(
                    version=self._version, versionless=self._versionless)
        return self._snapshot

    @property
    def tag(self):
        return (self.target_tag if self._direction == 'forward' else
                self.source_tag)

    def get(self, version=-1, versionless=False):
        if self._version != version:
            self._snapshot = None
            self._version = version
        if self._versionless != versionless:
            self._snapshot = None
            self._versionless = versionless
        if self.snapshot:
            deps = self.snapshot.get_dependencies(self.snapshot, tag=self.tag)
            if self._single:
                return deps[0] if deps else {}
            else:
                return deps
        else:
            return {}

    def add(self, snapshot):
        snapshot = snapshot.copy(self.snapshot.conn)
        if self._direction == 'forward':
            self.snapshot.add_dependency_by_code(
                snapshot, type='ref', tag=self.target_tag)
            snapshot.add_dependency_by_code(
                self.snapshot, type='ref', tag=self.source_tag)
        else:
            self.snapshot.add_dependency_by_code(
                snapshot, type='ref', tag=self.source_tag)
            snapshot.add_dependency_by_code(
                self.snapshot, type='ref', tag=self.target_tag)
        return self.snapshot, snapshot

    def remove(self, snapshot=None):
        snapshot = snapshot.copy(self.snapshot.conn)
        if self.direction == 'forward':
            self.snapshot.remove_dependency(
                snapshot, type='ref', tag=self.target_tag)
            snapshot.remove_dependency(
                self.snapshot, type='ref', tag=self.source_tag)
        else:
            self.snapshot.remove_dependency(
                snapshot, type='ref', tag=self.source_tag)
            snapshot.remove_dependency(
                self.snapshot, type='ref', tag=self.target_tag)
        return self.snapshot, snapshot


class DefaultDependency(TwoWayDependency):
    __keyword__ = 'default'
    __source_tag__ = 'source'
    __target_tag__ = 'target'
