### ====================================================================================================
### IMPORTS
### ====================================================================================================
import arcade
from utils import *
from random import *



class Process:

    ### ====================================================================================================
    ### PARAMETERS
    ### ====================================================================================================
    SCREEN_WIDTH  = int(960*1.75)
    SCREEN_HEIGHT = int(540*1.75)

    # create new candy
    def createCandy(self):
        nbImg = 8
        x = randint(0,Process.SCREEN_WIDTH)
        y = Process.SCREEN_HEIGHT+50
        params = {"filePath"  : "images/items/shuriken.png",
                  "spriteBox" :(4,2,175,175),
                  "startIndex":0,
                  "endIndex"  :nbImg-1,
                  "size"      :(self.CANDY_W, self.CANDY_W)
                 }
        candy = createAnimatedSprite(params)
        candy.center_x = x
        candy.center_y = y
        img = randint(0,nbImg-1)
        candy.set_texture(img)
        spd = random()*(self.MAX_CANDY_SPEED-self.MIN_CANDY_SPEED) + self.MIN_CANDY_SPEED
        self.candies.append((candy,spd,x))

    def drawCandies(self):
        for c in self.candies:
            c[0].draw()

    def updateCandies(self,dt):
        for c in self.candies:
            # get girl sprite
            spr = self.girl["anims"][self.girl["state"]]
            # get candy sprite
            cnd = c[0]
            # move candy down
            cnd.center_y -= c[1]*dt*60
            # turn candy
            cnd.angle += 10
            # change x position according to parallax
            refX = self.parallax["offset"]
            cnd.center_x = refX + c[2]
            # if candy too low : destroy
            if cnd.center_y < self.girl["position"][1]-spr.height/2:
                self.candies.remove(c)
                self.createSkullBurst(cnd.center_x, cnd.center_y, c[2])

            # if candy colligind with girl
            if (cnd.center_x - spr.center_x)**2 + (cnd.center_y - spr.center_y)**2 < self.COLLIDE_DIST**2:
                self.candies.remove(c)
                self.createGhostBurst(cnd.center_x, cnd.center_y, c[2])

    # create Ghost Burst
    def createGhostBurst(self,currentX,currentY, realX):
        # create burst
        paramB = {"x0": currentX,
                  "y0": currentY,
                  "partInterval": 0.020,
                  "totalDuration": 0.3,
                  "partSize": 50,
                  "partScale": 0.15,
                  "partSpeed": 10.0,
                  "color": (0, 0, 0),
                  "startAlpha": 100,
                  "endAlpha": 25,
                  "imagePath": "images/items/ghost.png"
                  }
        newBurst = createParticleBurst(paramB)
        self.bursts.append((newBurst, realX))

    # create Ghost Burst
    def createSkullBurst(self,currentX,currentY, realX):
        # create burst
        paramB = {"x0": currentX,
                  "y0": currentY,
                  "partInterval": 0.03,
                  "totalDuration": 0.25,
                  "partSize": 50,
                  "partScale": 0.15,
                  "partSpeed": 10.0,
                  "color": (0, 0, 0),
                  "startAlpha": 100,
                  "endAlpha": 25,
                  "imagePath": "images/items/skull.png"
                  }
        newBurst = createParticleBurst(paramB)
        self.bursts.append((newBurst, realX))


    # Draw parallax
    def drawParallax(self, excludes):
        refX = self.parallax["offset"]
        for i in range(len(self.parallax["sprites"])):
            if i not in excludes:
                layers = self.parallax["sprites"][i]
                layers[0].center_x = int(refX*(i/2+1)*0.33+Process.SCREEN_WIDTH/2)
                if layers[0].center_x >= Process.SCREEN_WIDTH/2:
                    layers[1].center_x = layers[0].center_x - Process.SCREEN_WIDTH
                else:
                    layers[1].center_x = layers[0].center_x + Process.SCREEN_WIDTH
                layers[0].draw()
                layers[1].draw()

    # compute offset from girl position
    def updateParallaxOffset(self):
        self.parallax["offset"] = Process.SCREEN_WIDTH/2 - self.girl["position"][0]


    # update movement state according to controls
    def updateState(self):
        if list(self.girl["move"].values()).count(True) == 1:
            self.girl["state"] = "run"
        else:
            self.girl["state"] = "idle"

    # update Position
    def updatePosition(self,dt):
        # move if needed and set direction
        if list(self.girl["move"].values()).count(True) == 1:
            if self.girl["move"]["left"]:
                self.girl["position"][0] -= self.SPEED*dt*60
                self.girl["lastDir"] = "left"
            else:
                self.girl["position"][0] += self.SPEED*dt*60
                self.girl["lastDir"] = "right"
        # saturate position
        self.girl["position"][0] = max(self.CHAR_W/2, self.girl["position"][0])
        self.girl["position"][0] = min(Process.SCREEN_WIDTH-self.CHAR_W/2, self.girl["position"][0])

    # update animation
    def updateGirlAnim(self,dt):
        # get current sprite
        sprite = self.girl["anims"][self.girl["state"]]
        # update animation
        sprite.update_animation(dt)
        # check direction
        if self.girl["lastDir"] == "left":
            sprite.width=-self.CHAR_W
        else:
            sprite.width=self.CHAR_W

    # select sprite according to state
    def drawGirl(self):
        x, y = self.girl["position"]
        sprite = self.girl["anims"][self.girl["state"]]
        sprite.center_x = x
        sprite.center_y = y
        sprite.draw()


    ### ====================================================================================================
    ### CONSTRUCTOR
    ### ====================================================================================================
    def __init__(self):
        pass
        self.SPEED  = 8
        self.CHAR_W = 250
        self.CANDY_W = 100
        self.MAX_CANDY_SPEED = 5
        self.MIN_CANDY_SPEED = 2.5
        self.COLLIDE_DIST = (self.CHAR_W + self.CANDY_W)*0.33
        self.NB_PARALLAX = 6

    ### ====================================================================================================
    ### INIT
    ### ====================================================================================================
    def setup(self):
        # character animation : prepare configuration
        paramRun = {"filePath"     : "images/characters/ninja.png",
                    "spriteBox"    : (7, 1, 120, 120),
                    "startIndex"   : 1,
                    "endIndex"     : 6,
                    "frameDuration": 1/20,
                    "size"         : (self.CHAR_W,self.CHAR_W),
                    "isMaxRatio"   : True
                   }
        paramIdle = {"filePath"     : "images/characters/ninja.png",
                     "spriteBox"    : (7, 1, 120, 120),
                     "startIndex"   : 0,
                     "endIndex"     : 0,
                     "frameDuration": 1/20,
                     "size"         : (self.CHAR_W,self.CHAR_W),
                     "isMaxRatio"   : True
                    }
        # character animation : create sprite objects
        runAnim  = createAnimatedSprite(paramRun )
        idleAnim = createAnimatedSprite(paramIdle)

        allAnims = {"idle" : idleAnim, "run":runAnim}
        # init state
        state = "idle"
        # movements
        move = {"left":False, "right":False}
        # character position
        position = [Process.SCREEN_WIDTH/2,162*1.75]
        # create girl dictionary
        self.girl = {"state"   : state,
                     "move"    : move,
                     "lastDir" : "right",
                     "position": position,
                     "anims"   : allAnims}

        # create parallax
        sprList = []
        for i in range(self.NB_PARALLAX ,0,-1):
            paramBG = {"filePath": f"images/parallax/night/night{i}.png",
                       "size"    : (Process.SCREEN_WIDTH, Process.SCREEN_HEIGHT)
                      }
            sprList.append([createFixedSprite(paramBG),
                            createFixedSprite(paramBG)])
            sprList[-1][0].center_y = Process.SCREEN_HEIGHT/2
            sprList[-1][1].center_y = Process.SCREEN_HEIGHT/2
        self.parallax = {"offset":0,
                         "sprites":sprList}

        # candy list
        self.candies = []

        # Particle effect following character
        paramPE = { "x0"          : 2000,
                    "y0"          : 2000,
                    "partNB"      : 200,
                    "partSize"    : 128,
                    "partScale"   : 0.3,
                    "partSpeed"   : 7.0,
                    "maxLifeTime" : 0.7,
                    "color"       : (255,128,0),
                    "startAlpha"  : 100,
                    "endAlpha"    : 0,
                    "textureFile" : "images/items/star.png"
        }
        self.charEmitter = createParticleEmitter(paramPE)

        # Particle bursts
        self.bursts = []


    # update all emitters
    def updateEmitters(self):
        # update all bursts
        for b in self.bursts:
            # update burst emitter
            emit = b[0]
            x    = self.parallax["offset"] + b[1]
            emit.center_x = x
            emit.update()
            # remove if needed
            if emit.can_reap():
                self.bursts.remove(b)

        # update character emitter
        if self.girl["state"] == "run":
            delta = int(self.CHAR_W/6)
            self.charEmitter.center_x = self.girl["position"][0]
            self.charEmitter.center_y = self.girl["position"][1] + randint(-delta,delta)
        else:
            self.charEmitter.center_x = 10000
            self.charEmitter.center_y = 10000
        self.charEmitter.update()

    # draw all emitters (bursts + char)
    def drawBursts(self):
        # draw bursts
        for b in self.bursts:
            b[0].draw()

    def drawCharEmitter(self):
        self.charEmitter.draw()



    ### ====================================================================================================
    ### UPDATE
    ### ====================================================================================================
    def update(self,deltaTime):
        self.updateState()
        self.updatePosition(deltaTime)
        self.updateParallaxOffset()
        self.updateGirlAnim(deltaTime)
        self.updateCandies(deltaTime)

        # update all emitters
        self.updateEmitters()


    ### ====================================================================================================
    ### RENDERING
    ### ====================================================================================================
    def draw(self):
        self.drawParallax([self.NB_PARALLAX -1])

        self.drawCharEmitter()
        self.drawGirl()

        self.drawCandies()

        self.drawBursts()

        self.drawParallax(list(range(self.NB_PARALLAX -1)))




    ### ====================================================================================================
    ### KEYBOARD EVENTS
    ### key is from : arcade.key.xxx
    ### ====================================================================================================
    def onKeyEvent(self,key,isPressed):
        if key == arcade.key.LEFT:
            self.girl["move"]["left"]  = isPressed
        if key == arcade.key.RIGHT:
            self.girl["move"]["right"] = isPressed

        if key==arcade.key.SPACE and isPressed:
            self.createCandy()


    ### ====================================================================================================
    ### GAMEPAD BUTTON EVENTS
    ### buttonName can be "A", "B", "X", "Y", "LB", "RB", "VIEW", "MENU", "LSTICK", "RSTICK"
    ### ====================================================================================================
    def onButtonEvent(self, gamepadNum,buttonName,isPressed):
        # print(f"GamePad={gamepadNum} - ButtonNum={buttonName} - isPressed={isPressed}")
        pass


    ### ====================================================================================================
    ### GAMEPAD AXIS EVENTS
    ### axisName can be "X", "Y", "RX", "RY", "Z"
    ### ====================================================================================================
    def onAxisEvent(self, gamepadNum,axisName,analogValue):
        #print(f"GamePad={gamepadNum} - AxisName={axisName} - Value={analogValue}")
        pass
        if axisName == "X":
            self.girl["move"]["left"]  = analogValue <= -0.5
            self.girl["move"]["right"] = analogValue >=  0.5

