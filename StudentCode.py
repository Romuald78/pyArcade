### ====================================================================================================
### IMPORTS
### ====================================================================================================
# -------------------------------------------------------------------
from utils import *
from random import *
import math
# -------------------------------------------------------------------
# -------------------------------------------------------------------



### ====================================================================================================
### PARAMETERS
### ====================================================================================================
# -------------------------------------------------------------------
SCREEN_WIDTH  = int(960*1.5)
SCREEN_HEIGHT = int(540*1.5)
var  = {}
# -------------------------------------------------------------------



### ====================================================================================================
### YOUR OWN FUNCTIONS HERE
### ====================================================================================================
# -------------------------------------------------------------------
def saturateParallaxOffset(of7):
    while of7 > 1:
        of7 -= 2
    while of7 < -1:
        of7 += 2
    return of7

def moveParallax():
    of7  = var["offset"]
    step = var["prlxStep"]
    prlx = var["parallax"]
    for i in range(len(prlx)):
        bg1 = prlx[i][0]
        bg2 = prlx[i][1]
        j = len(prlx) -i ##### -1
        newOf7 = saturateParallaxOffset( of7 * (step**j) )
        bg1.center_x = int( SCREEN_WIDTH  * (0.5+newOf7) )
        bg1.center_y = SCREEN_HEIGHT / 2
        bg2.center_y = SCREEN_HEIGHT / 2
        if newOf7 >= 0:
            bg2.center_x = bg1.center_x - SCREEN_WIDTH
        else:
            bg2.center_x = bg1.center_x + SCREEN_WIDTH

def drawParallax():
    prlx = var["parallax"]
    for i in range(len(prlx)):
        bg1 = prlx[i][0]
        bg2 = prlx[i][1]
        bg1.draw()
        bg2.draw()

def loadParallax():
    prlx = []
    for i in range(1,7):
        bg1 = createFixedSprite(f"./images/winter0{i}.png", (SCREEN_WIDTH,SCREEN_HEIGHT))
        bg2 = createFixedSprite(f"./images/winter0{i}.png", (SCREEN_WIDTH,SCREEN_HEIGHT))
        prlx.append( (bg1,bg2) )
    # return new object
    return prlx

def setParallaxFromPlayer():
    x = var["charX"]
    of7 = (x-SCREEN_WIDTH/2)/(SCREEN_WIDTH/2)
    of7 = -of7
    var["offset"] = of7

def placeCharacterSprite():
    x = var["charX"]
    y = var["charY"]
    var["spriteWALK" ].center_x = x
    var["spriteWALK" ].center_y = y
    var["spriteSLIDE"].center_x = x
    var["spriteSLIDE"].center_y = y

def moveCharacter(delta):
    # set speed according to slide mode or not
    speed = var["speedSlide"] if var["slide"] else var["speedWalk"]
    # check if we have to move the sprites
    if var["moveL"] != var["moveR"] or var["slide"]:
        # left move
        if var["viewL"] == True:
            var["charX"] -= speed * 60 * delta
            var["spriteWALK"].update_animation(delta)
            var["spriteWALK"].width  = var["charWidth"] * -1
            var["spriteSLIDE"].width = var["charWidth"] * -1
        # right move
        else:
            var["charX"] += speed * 60 * delta
            var["spriteWALK"].update_animation(delta)
            var["spriteWALK"].width  = var["charWidth"]
            var["spriteSLIDE"].width = var["charWidth"]
    else:
        # no move : select default frame for animation
        var["spriteWALK"].set_texture(0)
        if var["viewL"] == True:
            var["spriteWALK"].width = var["charWidth"] * -1

    # set the sprite position
    placeCharacterSprite()

def checkScreenBorders():
    var["charX"] = max(0           +80, var["charX"])
    var["charX"] = min(SCREEN_WIDTH-80, var["charX"])

def drawCharacter():
    if var["slide"]:
        var["spriteSLIDE"].draw()
    else:
        var["spriteWALK"].draw()

def addNewFish():
    x     = randint(0,SCREEN_WIDTH)
    speed = 2+random()*4
    n     = randint(0,5)
    # set init time to make the fish appear a little bit higher on the screen (behind the penguin)
    hMax  = random()*700
    time  = speed*0.05
    y = SCREEN_HEIGHT
    tex = createAnimatedSprite("./images/fishes_224x128.png", (6, 1, 224, 128), (128, 128))
    tex.set_texture(n)
    tex.center_x = x
    tex.center_y = y
    var["fishes"].append( [tex, x, speed, time, hMax] )

def moveFishes(delta):
    for f in var["fishes"]:
        # fish X is related to character offset
        f[0].center_x = f[1] - var["charX"] + (SCREEN_WIDTH/2)
        # fish falling (throw in the air and fall back : sine wave according to speed and time)
        # speed is the number of seconds to make the up and down path
        totalTime = f[2]
        time      = f[3]
        y = math.sin(math.pi*time/totalTime)
        scal = 0.25 + 0.5*(time/totalTime)
        f[0].center_y = 100 + y*700
        f[0].scale = scal
        # fish turn
        turn = (time/totalTime)*(360+180) - 90
        f[0].angle = turn
        # increase time for next frame
        f[3] += delta


def checkFishDestroy():
    for f in var["fishes"]:
        totalTime = f[2]
        time      = f[3]
        # fish destroy if they touched the ground
        if time >= totalTime:
            var["fishes"].remove(f)

def drawFishes(isFront):
    for f in var["fishes"]:
        totalTime = f[2]
        time = f[3]
        #if the fishes are on the last hal of their path, draw them according to the boolean flag
        if (time >= totalTime/2) == (isFront):
            f[0].draw()


# -------------------------------------------------------------------




### ====================================================================================================
### INITIALISATION OF YOUR VARIABLES
### ====================================================================================================
def setup():
    #-------------------------------------------------------------------
    # parallax winter
    var["parallax"] = loadParallax()
    var["offset"]   = 0
    var["prlxStep"] = 0.8

    # character SPRITE
    var["spriteWALK"] = createAnimatedSprite("./images/penguin_walk.png", (4,1,128,128), (200, 200))
    var["charWidth" ] = var["spriteWALK"].width
    # SLIDE
    var["spriteSLIDE"] = createAnimatedSprite("./images/penguin_slide.png", (1,1,128,128), (200, 200))

    # character position
    var["charX"] = SCREEN_WIDTH//2
    var["charY"] = 250
    # character horizontal movement
    var["moveL"] = False
    var["moveR"] = False
    var["viewL"] = False
    var["slide"] = False
    var["speedWalk"]  = 6
    var["speedSlide"] = 12

    # fishes
    var["fishes"] = []
    var["time"]   = 0
    #-------------------------------------------------------------------



### ====================================================================================================
### UPDATE OF YOUR GAME DATA
### ====================================================================================================
def update(deltaTime):
    # -------------------------------------------------------------------
    # add fish every 500ms
    var["time"] += deltaTime
    while var["time"] > 1:
        var["time"] -= 1
        addNewFish()

    moveCharacter(deltaTime)
    checkScreenBorders()
    setParallaxFromPlayer()
    moveParallax()
    moveFishes(deltaTime)
    checkFishDestroy()
    #-------------------------------------------------------------------



### ====================================================================================================
### DRAW YOUR IMAGES ON THE SCREEN
### ====================================================================================================
def draw():
    #-------------------------------------------------------------------
    drawParallax()
    drawFishes(False)
    drawCharacter()
    drawFishes(True)
    #-------------------------------------------------------------------



### ====================================================================================================
### FUNCTION CALLED WHEN YOU PRESS A KEY ON THE KEYBOARD
### ====================================================================================================
def onKeyEvent(key,isPressed):
    #-------------------------------------------------------------------
    # process walking booleans
    if key == arcade.key.LEFT:
        var["moveL"] = isPressed
    if key == arcade.key.RIGHT:
        var["moveR"] = isPressed
    # process sliding
    if key == arcade.key.SPACE:
        var["slide"] = isPressed
    # process view only if not sliding
    if var["slide"] == False:
        if var["moveR"] != var["moveL"]:
            var["viewL"] = var["moveL"]
    #-------------------------------------------------------------------



### ====================================================================================================
### FUNCTION CALLED WHEN YOU PRESS A BUTTON ON A GAMEPAD CONTROLLER
### ====================================================================================================
def onButtonEvent(gamepadNum,buttonNum,isPressed):
    #-------------------------------------------------------------------
    pass
    #-------------------------------------------------------------------



### ====================================================================================================
### FUNCTION CALLED WHEN YOU MOVE AN AXIS ON A GAMEPAD CONTROLLER
### ====================================================================================================
def onAxisEvent(gamepadNum,axisName,analogValue):
    #-------------------------------------------------------------------
    pass
    #-------------------------------------------------------------------


