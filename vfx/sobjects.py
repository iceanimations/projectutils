from ..base import SObject
from .. import sthpw


class Asset(SObject):
    __stype__ = 'vfx/asset'


class ProductionElement(SObject):
    '''Production Element Class'''


class Episode(ProductionElement):
    __stype__ = 'vfx/episode'


class Sequence(ProductionElement):
    __stype__ = 'vfx/sequence'


class Shot(ProductionElement):
    __stype__ = 'vfx/shot'


class ProductionAsset(SObject):
    __asset_type__ = 'vfx/asset'
    __prod_type__ = None


class AssetInEpisode(ProductionAsset):
    __stype__ = 'vfx/asset_in_episode'
    __prod_type__ = 'vfx/episode'


class AssetInSequence(ProductionAsset):
    __stype__ = 'vfx/asset_in_sequence'
    __prod_type__ = 'vfx/sequence'


class AssetInShot(ProductionAsset):
    __stype__ = 'vfx/asset_in_shot'
    __prod_type__ = 'vfx/shot'


class Texture(SObject):
    __stype__ = 'vfx/texture'
    __parent_type__ = 'vfx/asset'
