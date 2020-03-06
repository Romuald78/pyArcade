import arcade

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

