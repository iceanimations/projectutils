from .. import base
from . import dependencies


class AssetModel(base.Context):
    __stype__ = 'vfx/asset'
    __context__ = 'model'

    publish_target = dependencies.PublishDependency()


class AssetRig(base.Context):
    __stype__ = 'vfx/asset'
    __context__ = 'rig'

    publish_target = dependencies.PublishDependency()


class AssetShaded(base.Context):
    __stype__ = 'vfx/asset'
    __context__ = 'shaded'

    publish_target = dependencies.PublishDependency()
    texture = dependencies.TextureDependency(single=True)


class AssetTexture(base.Context):
    __stype__ = 'vfx/texture'
    __context__ = 'texture'

    publish_target = dependencies.PublishDependency()
    shaded_model = dependencies.TextureDependency(
            direction='backward', single=True)


class AssetInEpisodeModel(base.Context):
    __stype__ = 'vfx/asset_in_episode'
    __context__ = 'model'

    publish_source = dependencies.PublishDependency(
            direction='backward', single=True)


class AssetInEpisodeShaded(base.Context):
    __stype__ = 'vfx/asset_in_episode'
    __context__ = 'shaded'

    publish_source = dependencies.PublishDependency(
            direction='backward', single=True)
    texture = dependencies.TextureDependency(single=True)
    combined = dependencies.CombinedDependency(single=True)


class AssetInEpisodeShadedCombined(base.Context):
    __stype__ = 'vfx/asset_in_episode'
    __context__ = 'shaded/combined'

    separate = dependencies.CombinedDependency(
            direction='backward', single=True)


class AssetInEpisodeTexture(base.Context):
    __stype__ = 'vfx/asset_in_episode'
    __context__ = 'texture'

    publish_source = dependencies.PublishDependency(
            direction='backward', single=True)
    shaded_model = dependencies.TextureDependency(
            direction='backward', single=True)


class AssetInEpisodeRig(base.Context):
    __stype__ = 'vfx/asset_in_episode'
    __context__ = 'rig'

    publish_source = dependencies.PublishDependency(
            direction='backward', single=True)
    combined = dependencies.CombinedDependency(single=True)


class AssetInEpisodeCombinedRig(base.Context):
    __stype__ = 'vfx/asset_in_episode'
    __context__ = 'rig/combined'

    separate = dependencies.CombinedDependency(
            direction='backward', single=True)


class SequenceAnimationMSE(base.Context):
    __stype__ = 'vfx/sequence'
    __context__ = 'animation/mse'

    cam = dependencies.AnimCamDependency()
    cache = dependencies.PointCacheDependency()
    preview = dependencies.PreviewDependency()


class ShotAnimation(base.Context):
    __stype__ = 'vfx/shot'
    __context__ = 'animation'


class ShotCache(base.Context):
    __stype__ = 'vfx/shot'
    __context__ = 'animation/cache'

    scene = dependencies.PointCacheDependency(
            direction='backward', single=True)


class ShotPreview(base.Context):
    __stype__ = 'vfx/shot'
    __context__ = 'animation/preview'

    scene = dependencies.PreviewDependency(
            direction='backward', single=True)


class ShotCam(base.Context):
    __stype__ = 'vfx/shot'
    __context__ = 'animation/cam'

    scene = dependencies.AnimCamDependency(
            direction='backward', single=True)


class ShotAnimatic(base.Context):
    __stype__ = 'vfx/shot'
    __context__ = 'animatic'
