from ..base import SObject
# from ..sthpw import Snapshot, File


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
    asset = None
    production = None


class AssetInEpisode(ProductionAsset):
    __stype__ = 'vfx/asset_in_episode'


class AssetInSequence(ProductionAsset):
    __stype__ = 'vfx/asset_in_sequence'


class AssetInShot(ProductionAsset):
    __stype__ = 'vfx/asset_in_shot'


class Texture(SObject):
    __stype__ = 'vfx/texture'
