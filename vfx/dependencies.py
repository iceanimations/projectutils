from ..dependencies import TwoWayDependency


class PublishDependency(TwoWayDependency):
    __keyword__ = 'publish'
    __source_tag__ = 'source'
    __target_tag__ = 'target'


class TextureDependency(TwoWayDependency):
    __keyword__ = 'texture'
    __source_tag__ = 'model'
    __target_tag__ = 'images'


class CombinedDependency(TwoWayDependency):
    __keyword__ = 'combined'
    __source_tag__ = 'separate'
    __target_tag__ = 'combined'


class CacheCompatibleDependency(TwoWayDependency):
    __keyword__ = 'cache_compatible'
    __source_tag__ = 'shaded'
    __target_tag__ = 'rig'


class PointCacheDependency(TwoWayDependency):
    __keyword__ = 'pointcache'
    __source_tag__ = 'scene'
    __target_tag__ = 'cache'


class AnimCamDependency(TwoWayDependency):
    __keyword__ = 'animcam'
    __source_tag__ = 'scene'
    __target_tag__ = 'cam'


class PreviewDependency(TwoWayDependency):
    __keyword__ = 'preview'
    __source_tag__ = 'scene'
    __target_tag__ = 'preview'


class AnimDependency(TwoWayDependency):
    __keyword__ = 'anim'
    __source_tag__ = 'scene'
    __target_tag__ = 'anim'


class Rig2Cache(TwoWayDependency):
    __keyword__ = 'rig2cache'
    __source_tag__ = 'rig'
    __target_tag__ = 'cache'
