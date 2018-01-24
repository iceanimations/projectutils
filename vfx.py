from .base import SObject
from .sthpw import Snapshot, File


class Asset(SObject):
    __stype__ = 'vfx/asset'


class ProductionElement(SObject):
    pass


class Episode(ProductionElement):
    __stype__ = 'vfx/episode'


class Sequence(ProductionElement):
    __stype__ = 'vfx/sequence'


class Shot(ProductionElement):
    __stype__ = 'vfx/sequence'


class ProductionAsset(SObject):
    pass


class AssetInEpisode(ProductionAsset):
    __stype__ = 'vfx/asset_in_episode'


class AssetInSequence(ProductionAsset):
    __stype__ = 'vfx/asset_in_sequence'


class AssetInShot(ProductionAsset):
    __stype__ = 'vfx/asset_in_shot'


class Texture(SObject):
    __stype__ = 'vfx/texture'


class Preview(File):
    pass


class Cache(object):
    pass
