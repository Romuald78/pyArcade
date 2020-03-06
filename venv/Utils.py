import arcade
from random import *
class Variables:
    pass

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540

def createSprite(filePath,size=None,isMaxRatio=False):
    spr = arcade.AnimatedTimeSprite()
    spr.textures = []
    spr.textures.append(arcade.load_texture(filePath))
    spr.update_animation()
    if size != None:
        if isMaxRatio:
            ratio = max(size[0] / spr.width, size[1] / spr.height)
        else:
            ratio = min(size[0]/spr.width, size[1]/spr.height)
        spr.scale = ratio

    return spr

def createParticleBurst(x0,y0,partInterval,totalDuration,partSize,partScale,partSpeed,color,lifeTime,startAlpha,endAlpha):
    e = arcade.Emitter(
        center_xy=(x0, y0),
        emit_controller=arcade.EmitterIntervalWithTime(partInterval, totalDuration),
        particle_factory=lambda emitter: arcade.FadeParticle(
            filename_or_texture=arcade.make_circle_texture(partSize, color),
            change_xy=arcade.rand_in_circle((0.0, 0.0), partSpeed),
            scale=partScale,
            lifetime=lifeTime,
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


