from .. import base


class ProjectRelatedSObject(base.SObject):
    project = base.ParentSObject('sthpw/project', 'project_code')


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
        self.conn.get_by_search_key(self.parent_search_key)


class Snapshot(NonProjectSObject, UserRelatedSObject, ProjectRelatedSObject):
    __stype__ = 'sthpw/snapshot'

    context = base.SObjectField('context', True)
    snapshot_type = base.SObjectField('snapshot_type', True)
    is_synced = base.SObjectField('is_synced', True)
    process = base.SObjectField('process', True)
    project_code = base.SObjectField('project_code', True)
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

    lock_user = base.ParentSObject('sthpw/login', 'lock_login')
    files = base.ChildSObject('sthpw/file')


class File(NonProjectSObject, ProjectRelatedSObject):
    __stype__ = 'sthpw/file'

    snapshot = base.ParentSObject('sthpw/snapshot', 'snapshot_code')

    repo_type = base.SObjectField('repo_type')
    file_name = base.SObjectField('file_name')
    snapshot_code = base.SObjectField('snapshot_code')
    project_code = base.SObjectField('project_code')
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
    source_path = base.SObjectField('source_path')
    search_type = base.SObjectField('search_type')
    metadata_search = base.SObjectField('metadata_search')

    @property
    def snapshot(self):
        return self.conn.get_parent(self.search_key)


class Milestone(ProjectRelatedSObject):
    __stype__ = 'sthpw/milestone'

    project_code = base.SObjectField('project_code', True)
    due_date = base.SObjectField('due_date', True)


class Task(NonProjectSObject, ProjectRelatedSObject, UserRelatedSObject):
    __stype__ = 'sthpw/task'

    bid_cost = base.SObjectField('bid_cost')
    process = base.SObjectField('process')
    bid_end_date = base.SObjectField('bid_end_date')
    client_version = base.SObjectField('client_version')
    project_code = base.SObjectField('project_code')
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

    project_code = base.SObjectField('project_code')
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

    def set(self):
        self.conn.set_project(self.code)

    def get_groups(self):
        pass

    @classmethod
    def get_current(cls):
        return cls.get_by_code(cls.conn.project_code)


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
    project_code = base.SObjectField('project_code')
    location = base.SObjectField('location')

    @classmethod
    def get_me(cls):
        return cls.get_by_code(cls.conn.login)

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
    project_code = base.SObjectField('project_code')
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
    project_code = base.SObjectField('project_code')
    search_code = base.SObjectField('search_code')


class Connection(ProjectRelatedSObject):
    __stype__ = 'sthpw/connection'

    context = base.SObjectField('context')
    project_code = base.SObjectField('project_code')
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


class Notification(
        ProjectRelatedSObject, UserRelatedSObject, NonProjectSObject):
    __stype__ = 'sthpw/notification'


class DbResource(base.SObject):
    __stype__ = 'sthpw/db_resource'


class WidgetSetting(base.SObject):
    __stype__ = 'sthpw/wdg_settings'


class DebugLog(base.SObject):
    __stype__ = 'sthpw/debug_log'


class ExceptionLog(base.SObject):
    __stype__ = 'sthpw/exception_log'


class GlobalTranslation(UserRelatedSObject):
    __stype__ = 'sthpw/translation'


class Schema(ProjectRelatedSObject):
    __stype__ = 'sthpw/schema'

    schema = base.SObjectField('schema')


class Pipeline(ProjectRelatedSObject):
    pipeline = base.SObjectField('pipeline')
    search_type = base.SObjectField('search_type')
    project_code = base.SObjectField('project_code')
    description = base.SObjectField('description')
    color = base.SObjectField('color')
    autocreate_tasks = base.SObjectField('autocreate_tasks')
    parent_process = base.SObjectField('parent_process')
