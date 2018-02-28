from .. import base
from .. import sthpw


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

    pipeline_code = base.SObjectField('pipeline_code')
    process = base.SObjectField('process')
    color = base.SObjectField('color')
    sort_order = base.SObjectField('sort_order')
    timestamp = base.SObjectField('timestamp')
    s_status = base.SObjectField('s_status')
    checkin_mode = base.SObjectField('checkin_mode')
    subcontext_options = base.SObjectField('subcontext_options')
    checkin_validate_script_path = base.SObjectField(
            'checkin_validate_script_path')
    checkin_options_view = base.SObjectField('checkin_options_view')
    sandbox_create_script_path = base.SObjectField(
            'sandbox_create_script_path')
    context_options = base.SObjectField('context_options')
    description = base.SObjectField('description')
    repo_type = base.SObjectField('repo_type')
    transfer_mode = base.SObjectField('transfer_mode')
    workflow = base.SObjectField('workflow')
    subpipeline_code = base.SObjectField('subpipeline_code')

    pipeline = base.ParentSObject('sthpw/pipeline', 'pipeline_code')
    subpipeline = base.ParentSObject('sthpw/pipeline', 'subpipeline_code')


class Translation(sthpw.UserRelatedSObject):
    __stype__ = 'config/process'

    en = base.SObjectField('en')
    fr = base.SObjectField('fr')
    ja = base.SObjectField('ja')
    es = base.SObjectField('es')


class WidgetConfig(sthpw.UserRelatedSObject):
    __stype__ = 'config/widget_config'

    view = base.SObjectField('view')
    category = base.SObjectField('category')
    search_type = base.SObjectField('search_type')
    config = base.SObjectField('config')
    widget_type = base.SObjectField('widget_type')
    title = base.SObjectField('title')


class ClientTrigger(base.SObject):
    __stype__ = 'config/client_trigger'

    event = base.SObjectField('event')
    callback = base.SObjectField('callback')


class ServerTrigger(base.SObject):
    __stype__ = 'config/trigger'

    class_name = base.SObjectField('class_name')
    script_path = base.SObjectField('script_path')
    title = base.SObjectField('title')
    description = base.SObjectField('description')
    event = base.SObjectField('event')
    mode = base.SObjectField('mode')
    process = base.SObjectField('process')
    listen_process = base.SObjectField('listen_process')
    trigger_type = base.SObjectField('trigger_type')
    data = base.SObjectField('data')
    search_type = base.SObjectField('search_type')


class ProjectSetting(base.SObject):
    __stype__ = 'config/prod_setting'

    key = base.SObjectField('key')
    value = base.SObjectField('value')
    description = base.SObjectField('description')
    type = base.SObjectField('type')
    search_type = base.SObjectField('search_type')
    category = base.SObjectField('category')


class CustomURL(base.SObject):
    __stype__ = 'config/url'

    url = base.SObjectField('url')
    widget = base.SObjectField('widget')
