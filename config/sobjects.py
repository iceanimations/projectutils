from .. import base


class Naming(base.SObject):
    __stype__ = 'config/naming'

    base_dir_alias = base.SObjectField('base_dir_alias')
    context = base.SObjectField('context')
    latest_versionless = base.SObjectField('latest_versionless')
    class_name = base.SObjectField('class_name')
    sandbox_dir_naming = base.SObjectField('sandbox_dir_naming')
    current_versionless = base.SObjectField('current_versionless')
    checkin_type = base.SObjectField('checkin_type')
    dir_naming = base.SObjectField('dir_naming')
    search_type = base.SObjectField('search_type')
    manual_version = base.SObjectField('manual_version')
    file_naming = base.SObjectField('file_naming')
    snapshot_type = base.SObjectField('snapshot_type')
    script_path = base.SObjectField('script_path')
    ingest_rule_code = base.SObjectField('ingest_rule_code')
    sandbox_dir_alias = base.SObjectField('sandbox_dir_alias')
    condition = base.SObjectField('condition')


class Process(base.SObject):
    __stype__ = 'config/process'


class Translation(base.SObject):
    __stype__ = 'config/process'


class WidgetConfig(base.SObject):
    __stype__ = 'config/widget_config'


class ClientTrigger(base.SObject):
    __stype__ = 'config/client_trigger'


class ServerTrigger(base.SObject):
    __stype__ = 'config/trigger'


class ProjectSetting(base.SObject):
    __stype__ = 'config/prod_setting'


class CustomURL(base.SObject):
    __stype__ = 'config/url'
