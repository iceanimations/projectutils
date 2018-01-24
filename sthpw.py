from .base import SObject, _Project


__all__ = ['Snapshot', 'File', 'Task', 'Project', 'Login', 'LoginGroup',
           'LoginInGroup']


class Snapshot(SObject):
    __stype__ = 'sthpw/snapshot'


class File(SObject):
    __stype__ = 'sthpw/file'


class Task(SObject):
    __stype__ = 'sthpw/task'


class Project(SObject):
    __stype__ = 'sthpw/project'


class Login(SObject):
    __stype__ = 'sthpw/login'


class LoginGroup(SObject):
    __stype__ = 'sthpw/login_group'


class LoginInGroup(SObject):
    __stype__ = 'sthpw/login_in_group'
