from .. import base
from .. import sthpw
from .. import config


class AssetCategory(sthpw.UserRelatedSObject):
    __stype__ = 'vfx/asset_category'


class AssetType(base.SObject):
    __stype__ = 'vfx/asset_type'


class Asset(base.SObject):
    __stype__ = 'vfx/asset'

    short_code = base.SObjectField('short_code')
    asset_category = base.SObjectField('asset_category')
    pipeline_code = base.SObjectField('pipeline_code')
    snapshot = base.SObjectField('snapshot')
    images = base.SObjectField('images')
    asset_type = base.SObjectField('asset_type')

    category = base.ParentSObject('vfx/asset_category', 'asset_category')
    type = base.ParentSObject('vfx/asset_type', 'asset_type')
    pipeline = base.ParentSObject('sthpw/pipeline', 'pipeline_code')


class Texture(base.SObject):
    __stype__ = 'vfx/texture'

    category = base.SObjectField('category')
    asset_code = base.SObjectField('asset_code')
    asset_context = base.SObjectField('asset_context')
    pipeline_code = base.SObjectField('pipeline_code')
    snapshot = base.SObjectField('snapshot')

    asset = base.ParentSObject('vfx/asset', 'asset_code')
    pipeline = base.ParentSObject('sthpw/pipeline', 'pipeline_code')


class ProductionElement(base.SObject):
    '''Production Element Class'''
    sort_order = base.SObjectField('sort_order')


class Episode(ProductionElement):
    __stype__ = 'vfx/episode'


class Sequence(ProductionElement):
    __stype__ = 'vfx/sequence'

    episode_code = base.SObject('episode')
    episode = base.ParentSObject('vfx/episode', 'episode_code')


class Shot(ProductionElement):
    __stype__ = 'vfx/shot'

    tc_frame_end = base.SObjectField('tc_frame_end')
    type = base.SObjectField('type')
    description = base.SObjectField('description')
    frame_out = base.SObjectField('frame_out')
    short_code = base.SObjectField('short_code')
    scan_status = base.SObjectField('scan_status')
    frame_note = base.SObjectField('frame_note')
    tc_frame_start = base.SObjectField('tc_frame_start')
    priority = base.SObjectField('priority')
    complexity = base.SObjectField('complexity')
    pipeline_code = base.SObjectField('pipeline_code')
    sequence_code = base.SObjectField('sequence_code')
    images = base.SObjectField('images')
    frame_in = base.SObjectField('frame_in')
    sort_order = base.SObjectField('sort_order')
    parent_code = base.SObjectField('parent_code')

    pipeline = base.ParentSObject('sthpw/pipeline', 'pipeline_code')
    sequence = base.ParentSObject('sthpw/sequence', 'sequence_code')


class ProductionAsset(base.SObject):
    __asset_type__ = 'vfx/asset'
    __prod_type__ = None

    asset = base.ParentSObject('vfx/asset', 'asset_code')
    asset_code = base.SObjectField('asset_code')

    @base.abstractproperty
    def prod_elem(self):
        pass


class AssetInEpisode(ProductionAsset):
    __stype__ = 'vfx/asset_in_episode'
    __prod_type__ = 'vfx/episode'

    episode_code = base.SObjectField('episode_code')
    prod_elem = episode = base.ParentSObject(__prod_type__, 'episode_code')


class AssetInSequence(ProductionAsset):
    __stype__ = 'vfx/asset_in_sequence'
    __prod_type__ = 'vfx/sequence'

    sequence_code = base.SObjectField('sequence_code')
    prod_elem = sequence = base.ParentSObject(__prod_type__, 'sequence_code')


class AssetInShot(ProductionAsset, sthpw.UserRelatedSObject):
    __stype__ = 'vfx/asset_in_shot'
    __prod_type__ = 'vfx/shot'

    shot_code = base.SObjectField('shot_code')
    pipeline_code = base.SObjectField('pipeline_code')
    type = base.SObjectField('type')

    prod_elem = shot = base.ParentSObject(__prod_type__, 'shot_code')
    pipeline = base.ParentSObject('sthpw/pipeline', 'pipeline_code')


class Layer(base.SObject):
    __stype__ = 'vfx/layer'

    sort_order = base.SObjectField('sort_order')
    shot_code = base.SObjectField('shot_code')
    shot = base.ParentSObject('vfx/shot', 'shot_code')
    snapshot = base.SObjectField('snapshot')


class Release(base.SObject):
    __stype__ = 'vfx/release'


class ArtReference(base.SObject):
    __stype__ = 'vfx/art_reference'

    snapshot = base.SObjectField('snapshot')
    keywords = base.SObjectField('keywords')


class Camera(base.SObject):
    __stype__ = 'vfx/camera'

    shot_code = base.SObjectField('shot_code')
    shot = base.ParentSObject('vfx/shot', 'shot_code')


class Leica(sthpw.UserRelatedSObject):
    __stype__ = 'vfx/leica'

    shot_code = base.SObjectField('shot_code')
    shot = base.ParentSObject('vfx/shot', 'shot_code')


class NodeData(base.SObject):
    __stype__ = 'vfx/node_data'


class Plate(base.SObject):
    __stype__ = 'vfx/plate'

    episode_code = base.SObjectField('episode_code')
    shot_code = base.SObjectField('shot_code')
    type = base.SObjectField('type')

    episode = base.SObjectField('episode')
    shot = base.ParentSObject('vfx/shot', 'shot_code')


class Render(base.UserRelatedSObject):
    __stype__ = 'vfx/render'

    _file_range = base.SObjectField('_file_range')
    _version = base.SObjectField('_version')
    _snapshot = base.SObjectField('_snapshot')
    _session = base.SObjectField('_session')
    search_type = base.SObjectField('search_type')
    search_id = base.SObjectField('search_id')
    _images = base.SObjectField('_images')
    login = base.SObjectField('login')
    _snapshot_code = base.SObjectField('_snapshot_code')

    @property
    def parent_search_key(self):
        return self.conn.build_search_key(
                self.__stype__, self.id,
                self.project_code if self.project_code else None, 'id')

    @property
    def parent_sobject(self):
        return self.conn.get_by_search_key(self.parent_search_key)


class Review(base.UserRelatedSObject):
    __stype__ = 'vfx/review'

    type = base.SObjectField('type')
    date = base.SObjectField('date')


class Schedule(base.UserRelatedSObject):
    __stype__ = 'vfx/schedule'

    shot_code = base.SObjectField('shot_code')
    pipeline_code = base.SObjectField('pipeline_code')

    pipeline = base.ParentSObject('sthpw/pipeline', 'pipeline_code')


class Script(base.SObject):
    __stype__ = 'vfx/script'

    title = base.SObjectField('title')
    sequence_code = base.SObjectField('sequence_code')
    stage = base.SObjectField('stage')
    author = base.SObjectField('author')

    sequence = base.ParentSObject('vfx/sequence', sequence_code)


class ShotTexture(base.UserRelatedSObject):
    __stype__ = 'vfx/shot_texture'

    snapshot = base.SObjectField('snapshot')
    search_id = base.SObjectField('search_id')
    search_type = base.SObjectField('search_type')
    asset_context = base.SObjectField('asset_context')

    @property
    def parent_search_key(self):
        return self.conn.build_search_key(
                self.__stype__, self.id,
                self.project_code if self.project_code else None, 'id')

    @property
    def parent_sobject(self):
        return self.conn.get_by_search_key(self.parent_search_key)


class Storyboard(base.SObject):
    __stype__ = 'vfx/storyboard'

    shot_code = base.SObjectField('shot_code')
    shot = base.ParentSObject('vfx/shot', 'shot_code')


class Submission(base.UserRelatedSObject):
    __stype__ = 'vfx/submission'

    review_code = base.SObjectField('review_code')
    artist = base.SObjectField('artist')
    version = base.SObjectField('version')
    search_id = base.SObjectField('search_id')
    search_type = base.SObjectField('search_type')
    sort_order = base.SObjectField('sort_order')
    snapshot_code = base.SObjectField('snapshot_code')
    context = base.SObjectField('context')
    parent_code = base.SObjectField('parent_code')

    review = base.ParentSObject('sthpw/review', 'review_code')
    artist_user = base.ParentSObject('sthpw/login', 'artist')
    parent = base.ParentSObject('sthpw/submission', 'parent_code')
    snapshot = base.ParentSObject('vfx/snapshot', 'snapshot_code')

    @property
    def parent_search_key(self):
        return self.conn.build_search_key(
                self.__stype__, self.id,
                self.project_code if self.project_code else None, 'id')

    @property
    def parent_sobject(self):
        return self.conn.get_by_search_key(self.parent_search_key)
