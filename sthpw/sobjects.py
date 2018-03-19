from .. import base
from .. import server as _server

import os
import xml.etree.ElementTree as etree


class ProjectRelatedSObject(base.SObject):
    project = base.ParentSObject('sthpw/project', 'project_code')
    project_code = base.SObjectField('project_code')


class UserRelatedSObject(base.SObject):
    user = base.ParentSObject('sthpw/login', 'login')
    login = base.SObjectField('login', True)


class NonProjectSObject(base.SObject):

    @property
    def parent_search_key(self):
        return self.conn.build_search_key(
                self.__stype__, self.code,
                self.project_code if self.project_code else None)

    @property
    def parent_sobject(self):
        return self.conn.get_by_search_key(self.parent_search_key)


class Snapshot(NonProjectSObject, UserRelatedSObject, ProjectRelatedSObject):
    __stype__ = 'sthpw/snapshot'

    context = base.SObjectField('context', True)
    snapshot_type = base.SObjectField('snapshot_type', True)
    is_synced = base.SObjectField('is_synced', True)
    process = base.SObjectField('process', True)
    lock_date = base.SObjectField('lock_data', True)
    is_latest = base.SObjectField('is_latest', True)
    revision = base.SObjectField('revision', True)
    level_id = base.SObjectField('level_id', True)
    lock_login = base.SObjectField('lock_login', True)
    label = base.SObjectField('label', True)
    version = base.SObjectField('version', True)
    level_type = base.SObjectField('level_type', True)
    search_id = base.SObjectField('search_id', True)
    metadata = base.SObjectField('metadata', True)
    status = base.SObjectField('status', True)
    repo = base.SObjectField('repo', True)
    is_current = base.SObjectField('is_current', True)
    search_code = base.SObjectField('search_code', True)
    snapshot_type = base.SObjectField('snapshot_type', True)
    server = base.SObjectField('server', True)
    search_type = base.SObjectField('search_type', True)
    snapshot = base.SObjectField('snapshot', True)
    context = base.SObjectField('context', True)
    column_name = base.SObjectField('column_name', True)

    paths = base.PathField('__paths__')
    paths_dict = base.PathField('__paths_dict__')

    parent_cached = base.CachedObjectField('__parent__')
    files_cached = base.CachedObjectField('__files__')

    lock_user = base.ParentSObject('sthpw/login', 'lock_login')
    files = base.ChildSObject('sthpw/file')

    def get_all_paths(self, *args, **kwargs):
        conn = self.conn
        paths = conn.get_all_paths_from_snapshot(
                self.code, *args, **kwargs)
        return [conn.translatePath(v) for v in paths]
    get_all_paths.__doc__ = \
        _server.TacticObjectServer.get_all_paths_from_snapshot.__doc__

    def query(cls, **kwargs):
        return cls.conn.query_snapshots(
                include_paths=True, include_paths_dict=True,
                include_parent=True, include_files=True, **kwargs)
    query.__doc__ = _server.TacticObjectServer.query_snapshots.__doc__
    query = classmethod(query)

    def get_preallocated_path(self, *args, **kwargs):
        path = self.conn.get_preallocated_path(self.code, *args, **kwargs)
        return self.conn.translatePath(path)
    get_preallocated_path.__doc__ = \
        _server.TacticObjectServer.get_preallocated_path.__doc__

    def set_current(self):
        self.conn.set_current_snapshot(self.code)
    set_current.__doc__ = \
        _server.TacticObjectServer.set_current_snapshot.__doc__

    def copy_to(self, snapshot_to, mode='copy', exclude_types=None):
        if not isinstance(snapshot_to, Snapshot):
            raise ValueError('%r is not a Snapshot instance')
        if exclude_types is None:
            exclude_types = []
        server = self.conn
        snapshot_to = snapshot_to.copy(server)

        dirs = []
        groups = []
        files = []
        ftypes = []

        base_dir = server.base_dir

        for fileEntry in self.files:
            file_path = os.path.join(
                    base_dir, fileEntry.relative_dir, fileEntry.file_name
                    ).replace('/', '\\')
            file_type = fileEntry.type

            if file_type in exclude_types:
                continue

            if fileEntry['base_type'] == 'file':
                files.append(file_path)
                ftypes.append(file_type)
            elif fileEntry['base_type'] == 'directory':
                dirs.append((file_path, file_type))
            elif fileEntry['base_type'] == 'sequence':
                groups.append((file_path, fileEntry['file_range'], file_type))

        server.add_file(
                snapshot_to.code, files, file_type=ftypes, mode=mode,
                create_icon=False)
        for directory in dirs:
            server.add_directory(
                    snapshot_to.code, directory[0], file_type=directory[1],
                    mode=mode)
        for group in groups:
            server.add_group(snapshot_to.code, group[1], group[0], mode=mode)

        return snapshot_to

    def add_dependency(self, file_path, **kwargs):
        return self.conn.add_dependency(file_path, **kwargs)
    add_dependency.__doc__ = _server.TacticObjectServer.add_dependency.__doc__

    def add_dependency_by_code(self, snapshot, **kwargs):
        code = snapshot
        if isinstance(snapshot, Snapshot):
            snapshot = snapshot.copy(self.conn)
            code = snapshot.code
        return self.conn.add_dependency_by_code(
                self.code, code, **kwargs)
    add_dependency_by_code.__doc__ = \
        _server.TacticObjectServer.add_dependency_by_code.__doc__

    def get_dependencies(self, *args, **kwargs):
        return self.conn.get_dependencies(self.code, *args, **kwargs)
    get_dependencies.__doc__ = \
        _server.TacticObjectServer.get_dependencies.__doc__

    def get_all_dependencies(self, *args, **kwargs):
        return self.conn.get_all_dependencies(self.code, *args, **kwargs)
    get_all_dependencies.__doc__ = \
        _server.TacticObjectServer.get_all_dependencies.__doc__

    def remove_dependency(self, snapshot=None, type='ref', tag='main'):
        elem = etree.fromstring(self.snapshot)
        xpath = "%s[@tag='%s']" % (type, tag)
        if snapshot is not None:
            snapshot = snapshot.copy(self.conn)
            xpath = "%s[@snapshot_code='%s']" % snapshot.code
        for child in elem.findall(xpath):
            elem.remove(child)
        self.snapshot = etree.dump(elem)
        return self.snapshot.update()

    def add_file(self, file_path, **kwargs):
        return self.conn.add_file(self.code, file_path, **kwargs)
    add_file.__doc__ = _server.TacticObjectServer.add_file.__doc__

    def add_group(self, *args, **kwargs):
        return self.conn.add_group(self.code, *args, **kwargs)
    add_group.__doc__ = _server.TacticObjectServer.add_group.__doc__

    def add_directory(self, *args, **kwargs):
        return self.conn.add_directory(self.code, *args, **kwargs)
    add_directory.__doc__ = _server.TacticObjectServer.add_directory.__doc__

    def get_context(self):
        return base.Context(
                self.context, self.parent_cached or self.get_parent())


class File(NonProjectSObject, ProjectRelatedSObject):
    __stype__ = 'sthpw/file'

    snapshot = base.ParentSObject('sthpw/snapshot', 'snapshot_code')

    repo_type = base.SObjectField('repo_type')
    file_name = base.SObjectField('file_name')
    snapshot_code = base.SObjectField('snapshot_code')
    base_type = base.SObjectField('base_type')
    st_size = base.SObjectField('st_size')
    type = base.SObjectField('type')
    search_id = base.SObjectField('search_id')
    metadata = base.SObjectField('metadata')
    base_dir_alias = base.SObjectField('base_dir_alias')
    timestamp = base.SObjectField('timestamp')
    file_range = base.SObjectField('file_range')
    search_code = base.SObjectField('search_code')
    checkin_dir = base.SObjectField('checkin_dir')
    md5 = base.SObjectField('md5')
    relative_dir = base.SObjectField('relative_dir')
    source_path = base.PathField('source_path')
    search_type = base.SObjectField('search_type')
    metadata_search = base.SObjectField('metadata_search')

    @property
    def parent_snapshot(self):
        return self.conn.Snapshot.query(
                filters=[('code', self.snapshot_code)], single=True)

    def get_path(self):
        path = os.path.join(
                self.conn.base_dir, self.relative_dir, self.file_name)
        return self.conn.translatePath(path)


class Milestone(ProjectRelatedSObject):
    __stype__ = 'sthpw/milestone'

    due_date = base.SObjectField('due_date', True)


class Task(NonProjectSObject, ProjectRelatedSObject, UserRelatedSObject):
    __stype__ = 'sthpw/task'

    bid_cost = base.SObjectField('bid_cost')
    process = base.SObjectField('process')
    bid_end_date = base.SObjectField('bid_end_date')
    client_version = base.SObjectField('client_version')
    completion = base.SObjectField('completion')
    search_type = base.SObjectField('search_type')
    actual_start_date = base.SObjectField('actual_start_date')
    parent_id = base.SObjectField('parent_id')
    discussion = base.SObjectField('discussion')
    actual_end_date = base.SObjectField('actual_end_date')
    overlap = base.SObjectField('overlap')
    priority = base.SObjectField('priority')
    color = base.SObjectField('color')
    pipeline_code = base.SObjectField('pipeline_code')
    search_id = base.SObjectField('search_id')
    status = base.SObjectField('status')
    milestone_code = base.SObjectField('milestone_code')
    bid_quantity = base.SObjectField('bid_quantity')
    timestamp = base.SObjectField('timestamp')
    efficiency = base.SObjectField('efficiency')
    search_code = base.SObjectField('search_code')
    data_ = base.SObjectField('data_')
    actual_quantity = base.SObjectField('actual_quantity')
    depend_id = base.SObjectField('depend_id')
    bid_duration = base.SObjectField('bid_duration')
    sort_order = base.SObjectField('sort_order')
    bid_start_date = base.SObjectField('bid_start_date')
    context = base.SObjectField('context')
    velocity = base.SObjectField('velocity')
    actual_duration = base.SObjectField('actual_duration')
    supervisor = base.SObjectField('supervisor')
    assigned = base.SObjectField('assigned')

    supervisor_user = base.ParentSObject('sthpw/login', 'supervisor')
    assigned_user = base.ParentSObject('sthpw/login', 'assigned')
    milestone = base.ParentSObject('sthpw/milestone', 'milestone_code')


class WorkHour(NonProjectSObject, ProjectRelatedSObject, UserRelatedSObject):
    __stype__ = 'sthpw/work_hour'

    description = base.SObjectField('description')
    category = base.SObjectField('category')
    day = base.SObjectField('day')
    start_time = base.SObjectField('start_time')
    end_time = base.SObjectField('end_time')
    straight_time = base.SObjectField('straight_time')
    over_time = base.SObjectField('over_time')
    search_type = base.SObjectField('search_type')
    search_id = base.SObjectField('search_id')
    task_code = base.SObjectField('task_code')
    overtime = base.SObjectField('overtime')
    status = base.SObjectField('status')
    process = base.SObjectField('process')
    search_code = base.SObjectField('search_code')


class Project(base.SObject):
    __stype__ = 'sthpw/project'

    db_resource = base.SObjectField('db_resource')
    sobject_mapping_cls = base.SObjectField('sobject_mapping_cls')
    category = base.SObjectField('category')
    palette = base.SObjectField('palette')
    title = base.SObjectField('title')
    dir_naming_cls = base.SObjectField('dir_naming_cls')
    type = base.SObjectField('type')
    code_naming_cls = base.SObjectField('code_naming_cls')
    file_naming_cls = base.SObjectField('file_naming_cls')
    reg_hours = base.SObjectField('reg_hours')
    last_db_update = base.SObjectField('last_db_update')
    pipeline = base.SObjectField('pipeline')
    database = base.SObjectField('database')
    last_version_update = base.SObjectField('last_version_update')
    is_template = base.SObjectField('is_template')
    snapshot = base.SObjectField('snapshot')
    node_naming_cls = base.SObjectField('node_naming_cls')
    initials = base.SObjectField('initials')

    project_files = base.ChildSObject('sthpw/file')
    project_groups = base.ChildSObject('sthpw/login_group')
    project_milestones = base.ChildSObject('sthpw/milestone')
    project_tasks = base.ChildSObject('sthpw/task')
    project_work_hours = base.ChildSObject('sthpw/work_hour')
    project_status_logs = base.ChildSObject('sthpw/status_log')
    project_connection = base.ChildSObject('sthpw/connection')
    project_triggers = base.ChildSObject('sthpw/trigger')
    project_notifications = base.ChildSObject('sthpw/notification')
    project_translations = base.ChildSObject('sthpw/translation')
    project_schemas = base.ChildSObject('sthpw/schema')
    project_pipelines = base.ChildSObject('sthpw/pipeline')

    @property
    def project_snapshots(self):
        return self.conn.Snapshot.query(filters=[('project_code', 'code')])

    @property
    def project_files(self):
        return self.conn.File.query(filters=[('project_code', 'code')])

    @property
    def checkins(self):
        return self.conn.Snapshot.query(filters=[('project_code', self.code)])

    def set(self):
        return self.conn.set_project(self.code)

    @classmethod
    def get_current(cls):
        return cls.get_by_code(cls.conn.project_code)

    @classmethod
    def get_all(cls):
        projects = cls.query()
        map(projects.pop,
            [ind for ind in reversed(range(len(projects)))
                if (projects[ind].code in ['admin', 'sthpw'] or
                    projects[ind].is_template or
                    projects[ind].category == 'Sample Projects') and
                not projects[ind]['code'] == 'vfx'])
        return projects


class Login(base.SObject):
    __stype__ = 'sthpw/login'

    login_in_groups = base.ChildSObject('sthpw/login_in_group')

    phone_number = base.SObjectField('phone_number')
    upn = base.SObjectField('upn')
    first_name = base.SObjectField('first_name')
    last_name = base.SObjectField('last_name')
    display_name = base.SObjectField('display_name')
    login_groups = base.SObjectField('login_groups')
    namespace = base.SObjectField('namespace')
    email = base.SObjectField('email')
    license_type = base.SObjectField('license_type')
    snapshot = base.SObjectField('snapshot')
    hourly_wage = base.SObjectField('hourly_wage')
    department = base.SObjectField('department')
    login = base.SObjectField('login')
    password = base.SObjectField('password')
    login_attempt = base.SObjectField('login_attempt')
    location = base.SObjectField('location')

    snapshots = base.ChildSObject('sthpw/snapshot')
    assigned_tasks = base.RelatedSObject('sthpw/task', key='assigned')
    supervisor_tasks = base.RelatedSObject('sthpw/task', key='supervisor')

    @classmethod
    def get_me(cls):
        return cls.get_by_code(cls.conn.login)

    @property
    def checkins(self):
        return self.conn.Snapshot.query(filters=[('login', self.code)])

    @property
    def groups(self):
        return self.conn.eval(
                '@SOBJECT(sthpw/login_in_group.sthpw/login_group)',
                self.search_key)

    @property
    def projects(self):
        project_codes = [group.project_code
                         for group in self.groups
                         if group.project_code]
        filters = [('code', code) for code in project_codes] + ['or']
        return self.conn.Project.query(filters=filters)


class LoginGroup(ProjectRelatedSObject):
    __stype__ = 'sthpw/login_group'

    login_in_groups = base.ChildSObject('sthpw/login_group')

    access_level = base.SObjectField('access_level')
    access_rules = base.SObjectField('access_rules')
    is_default = base.SObjectField('is_default')
    redirect_url = base.SObjectField('redirect_url')
    sub_groups = base.SObjectField('sub_groups')
    namespace = base.SObjectField('namespace')
    start_link = base.SObjectField('start_link')
    login_group = base.SObjectField('login_group')

    @property
    def logins(self):
        return self.conn.eval(
                '@SOBJECT(sthpw/login_in_group.sthpw/login)',
                self.search_key)


class LoginInGroup(UserRelatedSObject):
    __stype__ = 'sthpw/login_in_group'

    login_group = base.ParentSObject('sthpw/login_group', 'login_group')


class StatusLog(NonProjectSObject, ProjectRelatedSObject, UserRelatedSObject):
    __stype__ = 'sthpw/status_log'

    search_type = base.SObjectField('search_type')
    search_id = base.SObjectField('search_id')
    status = base.SObjectField('status')
    to_status = base.SObjectField('to_status')
    from_status = base.SObjectField('from_status')
    search_code = base.SObjectField('search_code')


class Connection(ProjectRelatedSObject):
    __stype__ = 'sthpw/connection'

    context = base.SObjectField('context')
    src_search_type = base.SObjectField('src_search_type')
    src_search_id = base.SObjectField('src_search_id')
    dst_search_type = base.SObjectField('dst_search_type')
    dst_search_id = base.SObjectField('dst_search_id')
    login = base.SObjectField('login')

    @property
    def src_sobject(self):
        skey = self.conn.build_search_key(
                self.src_search_type, self.src_search_id,
                project_code=self.project_code if self.project_code else None,
                column='id')
        return self.conn.get_by_search_key(skey)

    @property
    def dst_sobject(self):
        skey = self.conn.build_search_key(
                self.dst_search_type, self.dst_search_id,
                project_code=self.project_code if self.project_code else None,
                column='id')
        return self.conn.get_by_search_key(skey)


class GlobalServerTrigger(ProjectRelatedSObject):
    __stype__ = 'sthpw/trigger'

    class_name = base.SObjectField('class_name')
    script_path = base.SObjectField('script_path')
    description = base.SObjectField('description')
    event = base.SObjectField('event')
    mode = base.SObjectField('mode')
    project_code = base.SObjectField('project_code')
    s_status = base.SObjectField('s_status')
    process = base.SObjectField('process')


class Notification(ProjectRelatedSObject, UserRelatedSObject,
                   NonProjectSObject):
    __stype__ = 'sthpw/notification'

    event = base.SObjectField('event')
    description = base.SObjectField('description')
    search_type = base.SObjectField('search_type')
    project_code = base.SObjectField('project_code')
    rules = base.SObjectField('rules')
    subject = base.SObjectField('subject')
    message = base.SObjectField('message')
    email_handler_cls = base.SObjectField('email_handler_cls')
    mail_to = base.SObjectField('mail_to')
    mail_cc = base.SObjectField('mail_cc')
    mail_bcc = base.SObjectField('mail_bcc')
    title = base.SObjectField('title')
    process = base.SObjectField('process')
    listen_event = base.SObjectField('listen_event')
    data = base.SObjectField('data')


class DbResource(base.SObject):
    __stype__ = 'sthpw/db_resource'

    host = base.SObjectField('host')
    port = base.SObjectField('port')
    vendor = base.SObjectField('vendor')
    login = base.SObjectField('login')
    password = base.SObjectField('password')


class WidgetSetting(ProjectRelatedSObject, UserRelatedSObject):
    __stype__ = 'sthpw/wdg_settings'

    key = base.SObjectField('key')
    data = base.SObjectField('data')


class DebugLog(UserRelatedSObject):
    __stype__ = 'sthpw/debug_log'

    category = base.SObjectField('category')
    level = base.SObjectField('level')
    message = base.SObjectField('message')


class ExceptionLog(UserRelatedSObject):
    __stype__ = 'sthpw/exception_log'

    class_ = base.SObjectField('class')
    message = base.SObjectField('message')
    stack_trace = base.SObjectField('stack_trace')


class GlobalTranslation(UserRelatedSObject):
    __stype__ = 'sthpw/translation'

    en = base.SObjectField('en')
    fr = base.SObjectField('fr')
    ja = base.SObjectField('ja')
    es = base.SObjectField('es')


class Schema(ProjectRelatedSObject):
    __stype__ = 'sthpw/schema'

    schema = base.SObjectField('schema')


class Pipeline(ProjectRelatedSObject):
    __stype__ = 'sthpw/pipeline'

    pipeline = base.SObjectField('pipeline')
    search_type = base.SObjectField('search_type')
    description = base.SObjectField('description')
    color = base.SObjectField('color')
    autocreate_tasks = base.SObjectField('autocreate_tasks')
    parent_process = base.SObjectField('parent_process')
