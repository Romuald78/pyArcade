
import math



def getSpriteCircle(sprite, factor, offsetX=0, offsetY=00):
    fX = sprite.center_x + offsetX
    fY = sprite.center_y + offsetY
    fR = sprite.width * factor / 2
    cir2 = (fX,fY,fR)
    return cir2

def getSpriteBox(sprite, factor, offsetX=0, offsetY=0):
    fX = sprite.center_x
    fY = sprite.center_y + offsetY
    fW = sprite.width  * factor
    fH = sprite.height * factor
    box2 = (fX, fY, fW, fH)
    return box2

def getDistance(pt1, pt2):
    x1, y1 = pt1
    x2, y2 = pt2
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def isCollidingCircle(cir1, cir2):
    x1c, y1c, r1 = cir1
    x2c, y2c, r2 = cir2
    d12 = getDistance((x1c,y1c),(x2c,y2c))
    return d12 < r1+r2

def isCollidingBox( box1, box2 ):
    x1c, y1c, w1, h1 = box1
    x2c, y2c, w2, h2 = box2
    x1 = x1c - w1 / 2
    y1 = y1c - h1 / 2
    x2 = x2c - w2 / 2
    y2 = y2c - h2 / 2
    isColliding = (x1 < x2+w2 and x1+w1 > x2 and y1 < y2+h2 and y1+h1 > y2)
    return isColliding
