### ====================================================================================================
### IMPORTS
### ====================================================================================================
# -------------------------------------------------------------------
from utils import *
from collisions import *
from random import *
import math
import time
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

def drawParallax(start=0,end=None):
    prlx = var["parallax"]
    if end==None:
        end = len(prlx)
    for p in prlx[start:end]:
        bg1 = p[0]
        bg2 = p[1]
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
        dx = 0
        if var["viewL"] == True:
            dx = -speed * 60 * delta
            var["spriteWALK"].update_animation(delta)
            var["spriteWALK"].width  = var["charWidth"] * -1
            var["spriteSLIDE"].width = var["charWidth"] * -1
        # right move
        else:
            dx = speed * 60 * delta
            var["spriteWALK"].update_animation(delta)
            var["spriteWALK"].width  = var["charWidth"]
            var["spriteSLIDE"].width = var["charWidth"]
        # move player and check position
        var["charX"] += dx
        checkScreenBorders()
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

def generateNewFishes(delta):
    var["time"] += delta
    while var["time"] > 1:
        var["time"] -= 1
        addNewFish()

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
        f[0].center_y = 75 + y*725
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
            addNewSplashEffect( (f[1], f[0].center_y) )
            reduceLife()

def getCharBox():
    # get position of character
    pX = var["charX"]
    pY = var["charY"] + var["boxYOF7"  ]
    # get box size for character
    pW = var["charWidth"] * var["boxFactor"]
    pH = var["charHeight"] * var["boxFactor"]
    # construct box for character
    box1 = (pX, pY, pW, pH)
    return box1


def getCharCircle():
    # get position of character
    pX = var["charX"]
    pY = var["charY"] + var["boxYOF7"]
    # get circle size for character
    pR = var["charWidth"] * var["boxFactor"] / 2
    cir1 = (pX,pY,pR)
    return cir1

def checkFishCollisions():
    #box1 = getCharBox()
    cir1 = getCharCircle()
    # Now loop for all fishes and get their collision box
    for f in var["fishes"]:
        # if fish is going down
        totalTime = f[2]
        time      = f[3]
        if time > totalTime / 2:
            cir2 = getSpriteCircle(f[0],1.0)
            if isCollidingCircle(cir1,cir2):
                var["fishes"].remove(f)
                addNewWinEffect((cir2[0],cir1[1]))
                var["score"] += 1

def drawFishes(isFront):
    for f in var["fishes"]:
        totalTime = f[2]
        time = f[3]
        #if the fishes are on the last hal of their path, draw them according to the boolean flag
        if (time >= totalTime/2) == (isFront):
            f[0].draw()

def addNewWinEffect(pos):
    win = createParticleBurst(pos[0], pos[1], 0.025, 0.25, 100, 1, 3.0, (255,255,0,128), 100, 80, "./images/star.png")
    var["wins"].append(win)
    var["bloupWAV"].play()


def updateWinEffect(delta):
    for w in var["wins"]:
        w.update()
        if w.can_reap():
            var["wins"].remove(w)

def drawWinEffect():
    for w in var["wins"]:
        w.draw()

def addNewSplashEffect(pos):
    splash = createAnimatedSprite("./images/splash_192x96.png", (8, 1, 192, 96), (192, 96))
    splash.center_y = pos[1] + randint(0,15)
    splash.color = (255,255,255,128)
    var["splash"].append( [pos,splash] )
    var["splashWAV"].play()

def updateSplash(delta):
    for e in var["splash"]:
        if e[1].cur_texture_index == len(e[1].textures)-1:
            var["splash"].remove(e)
        else:
            e[1].update_animation(delta)

def moveSplash():
    for e in var["splash"]:
        # emitter X is related to character offset
        e[1].center_x = e[0][0] - var["charX"] + (SCREEN_WIDTH / 2)

def drawSplash():
    for e in var["splash"]:
        e[1].draw()

def drawDebug():
    cir1 = getCharCircle()
    #arcade.draw_circle_outline(cir1[0],cir1[1],cir1[2], arcade.color.YELLOW)
    for f in var["fishes"]:
        cir2 = getSpriteCircle(f[0], var["boxFactor"])
    #    arcade.draw_circle_outline(cir2[0],cir2[1],cir2[2], arcade.color.YELLOW)

def createHUD():
    var["lifebar"] = createFixedSprite("images/bar.png")
    var["lifebar"].center_x = 21*32/2 + 32
    var["lifebar"].center_y = SCREEN_HEIGHT - 32 - 32
    var["life"] = 0.5
    var["lifePoints"] = []
    for i in range(20):
        pt = createFixedSprite("images/barElt.png")
        pt.center_x = 32 + 32 + (i*32)
        pt.center_y = var["lifebar"].center_y
        red = 255*min(1, (20-i)/10)
        grn = 255*min(1,     i /10)
        pt.color = (red,grn,0,128)
        var["lifePoints"].append(pt)
    var["lifeMax"] = 20
    var["life"]    = 20
    var["score"]   = 0

def drawHUD():
    iMax = int( (0.5 + 20 * var["life"]) / var["lifeMax"] )
    for i in range(iMax):
        var["lifePoints"][i].draw()
    var["lifebar"].draw()
    arcade.draw_text("Score = "+str(var["score"]), SCREEN_WIDTH-400, SCREEN_HEIGHT-96-16, (0,0,0,192), 64 )

def reduceLife():
    var["life"] -= 1

def endGame():
    if var["life"] <= 0 and var["startFlag"] == True:
        var["startFlag"] = False

def createClouds():
    var["clouds"] = []
    for i in range(7):
        tex = createAnimatedSprite("./images/clouds_384x128.png", (7, 1, 384, 128), (384, 128))
        tex.set_texture(i)
        tex.center_y = randint(SCREEN_HEIGHT-192,SCREEN_HEIGHT-32)
        x            = randint(-SCREEN_WIDTH,SCREEN_WIDTH)
        speed = randint(1,4)
        var["clouds"].append([speed,x,tex])

def moveClouds(delta):
    of7  = var["offset"]
    step = var["prlxStep"]
    j    = 6
    newOf7 = saturateParallaxOffset(of7 * (step ** j))

    for c in var["clouds"]:
        c[1] += c[0] * delta*60
        if c[1] > SCREEN_WIDTH:
            c[1] -= 2*SCREEN_WIDTH
            c[2].center_y = randint(SCREEN_HEIGHT - 192, SCREEN_HEIGHT - 32)
            c[0] = randint(1, 4)
        c[2].center_x = int(SCREEN_WIDTH * (0.5 + newOf7)) + c[1]

def drawClouds():
    for c in var["clouds"]:
        c[2].draw()



def loadSounds():
    var["bloupWAV"] = arcade.load_sound("sounds/bloup.wav")
    var["splashWAV"]= arcade.load_sound("sounds/splash.wav")


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
    var["spriteWALK"].texture_change_frames = 2
    var["charWidth" ] = var["spriteWALK"].width
    var["charHeight"] = var["spriteWALK"].height

    # hit box
    var["boxFactor"] = 0.6
    var["boxYOF7"  ] = -25

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

    # splashes and wins
    var["splash"] = []
    var["wins"]   = []

    # start boolean
    var["startFlag"] = False

    createHUD()
    createClouds()

    loadSounds()
    #-------------------------------------------------------------------



### ====================================================================================================
### UPDATE OF YOUR GAME DATA
### ====================================================================================================
def update(deltaTime):
    # -------------------------------------------------------------------
    if var["startFlag"] and var["life"] > 0:
        generateNewFishes(deltaTime)

    moveCharacter(deltaTime)

    setParallaxFromPlayer()
    moveParallax()

    moveFishes(deltaTime)
    moveSplash()
    moveClouds(deltaTime)

    if var["life"] > 0:
        checkFishCollisions()

    checkFishDestroy()

    updateSplash(deltaTime)
    updateWinEffect(deltaTime)

    endGame()
    #-------------------------------------------------------------------




### ====================================================================================================
### DRAW YOUR IMAGES ON THE SCREEN
### ====================================================================================================
def draw():
    #-------------------------------------------------------------------
    drawParallax(0,1)
    drawClouds()
    drawParallax(1,-1)
    drawFishes(False)
    drawCharacter()
    drawFishes(True)
    drawSplash()
    drawWinEffect()
    drawParallax(-1)
    drawDebug()
    drawHUD()

    if var["startFlag"]==False:
        # the game has not started
        milliseconds = int(round(time.time() * 1000))
        arcade.draw_rectangle_filled(SCREEN_WIDTH//2,SCREEN_HEIGHT//2,SCREEN_WIDTH,SCREEN_HEIGHT,(0,0,0,128))

        msg  = "Gamepad Commands : \n"
        xRef = 16
        yRef = 150
        arcade.draw_text(msg, 16, yRef, (255,255,255,192), font_size=32, align="left")

        msg  = "- Move Left : ANALOG STICK \n"
        msg += "- Move Right : ANALOG STICK \n"
        msg += "- Slide : ANY BUTTON   \n"
        msg += "- Start new game : "
        if milliseconds % 2000 < 1000:
            msg += "START BUTTON "
        msg += "\n"
        yRef -= 56
        arcade.draw_text(msg, xRef+16, yRef, (255,255,255,192), font_size=16, align="left")

        msg  = "Keyboard Commands : \n"
        yRef -= 56
        arcade.draw_text(msg, xRef, yRef, (255, 255, 255, 192), font_size=32, align="left")

        msg  = "- Move Left : LEFT ARROW  \n"
        msg += "- Move Right : RIGHT ARROW \n"
        msg += "- Slide : SPACE KEY   \n"
        msg += "- Start new game : "
        if milliseconds % 2000 < 1000:
            msg += "ENTER KEY   "
        msg += "\n"
        yRef -= 56
        arcade.draw_text(msg, xRef+16, yRef, (255,255,255,192), font_size=16, align="left")

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
    # if ENTER is released, game starts
    if key == arcade.key.ENTER and not isPressed:
        if len(var["fishes"]) == 0 and var["startFlag"] == False:
            var["life"]      = 20
            var["startFlag"] = True
            var["score"]     = 0

    #-------------------------------------------------------------------



### ====================================================================================================
### FUNCTION CALLED WHEN YOU PRESS A BUTTON ON A GAMEPAD CONTROLLER
### ====================================================================================================
def onButtonEvent(gamepadNum,buttonNum,isPressed):
    #-------------------------------------------------------------------
    # if ENTER is released, game starts
    if buttonNum == 7:
        if not isPressed:
            if len(var["fishes"]) == 0 and var["startFlag"] == False:
                var["life"] = 20
                var["startFlag"] = True
                var["score"] = 0
    else:
        # process sliding
        var["slide"] = isPressed
    #-------------------------------------------------------------------



### ====================================================================================================
### FUNCTION CALLED WHEN YOU MOVE AN AXIS ON A GAMEPAD CONTROLLER
### ====================================================================================================
def onAxisEvent(gamepadNum,axisName,analogValue):
    #-------------------------------------------------------------------
    if axisName == "x":
        var["moveL"] = analogValue < -0.5
        var["moveR"] = analogValue >  0.5

    # process view only if not sliding
    if var["slide"] == False:
        if var["moveR"] != var["moveL"]:
            var["viewL"] = var["moveL"]
    #-------------------------------------------------------------------


