import arcade
from random import *

from arcade import AnimationKeyframe


def createFixedSprite(filePath, size=None, isMaxRatio=False):
    # load texture for sprite
    spr = arcade.AnimatedTimeSprite()
    spr.append_texture(arcade.load_texture(filePath))
    # set dimensions
    spr.update_animation()
    if size != None:
        if isMaxRatio:
            ratio = max(size[0] / spr.width, size[1] / spr.height)
        else:
            ratio = min(size[0]/spr.width, size[1]/spr.height)
        spr.scale = ratio
    return spr


def createAnimatedSprite(filePath, spriteBox, startIndex, endIndex, frameduration=1/60, size=None, isMaxRatio=False):
    # get sprite box (nb sprites X, nb Y, size X size Y)
    nbX, nbY, szW, szH = spriteBox
    # Instanciate sprite object
    spr = arcade.AnimatedTimeSprite()
    # Read Horizontal first, then vertical
    for y in range(nbY):
        for x in range(nbX):
            index = x + y*nbX
            # add index only if in range
            if index >= startIndex and index <= endIndex:
                tex = arcade.load_texture(filePath, x * szW, y * szH, szW, szH)
                spr.textures.append(tex)
    # set dimensions
    spr.update_animation()
    if size != None:
        if isMaxRatio:
            ratio = max(size[0]/spr.width, size[1]/spr.height)
        else:
            ratio = min(size[0]/spr.width, size[1]/spr.height)
        spr.scale = ratio
    # set frame duration
    spr.texture_change_frames = int(frameduration*60 + 0.5)

    # return sprite object
    return spr


def createParticleBurst(x0,y0,partInterval,totalDuration,partSize,partScale,partSpeed,color,startAlpha,endAlpha,imagePath=None):
    e = arcade.Emitter(
        center_xy=(x0, y0),
        emit_controller=arcade.EmitterIntervalWithTime(partInterval, totalDuration),
        particle_factory=lambda emitter: arcade.FadeParticle(
            filename_or_texture=imagePath if imagePath is not None else arcade.make_circle_texture(partSize, color),
            change_xy=arcade.rand_in_circle((0.0, 0.0), partSpeed),
            scale=partScale,
            lifetime=uniform(totalDuration/4, totalDuration),
            start_alpha=startAlpha,
            end_alpha=endAlpha,
        ),
    )
    return e



def createParticleEmitter(x0,y0,partNB,partSize,partScale,partSpeed,color,startAlpha,endAlpha):
    e = arcade.Emitter(
        center_xy        = (x0, y0),
        emit_controller  = arcade.EmitMaintainCount(partNB),
        particle_factory = lambda emitter: arcade.FadeParticle(
            filename_or_texture = arcade.make_circle_texture(partSize, color),
            change_xy           = arcade.rand_in_circle( (0.0,0.0), partSpeed),
            lifetime            = uniform(0.01,0.4),
            scale = partScale,
            start_alpha=startAlpha,
            end_alpha=endAlpha,
        ),
    )
    return e


