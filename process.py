### ====================================================================================================
### IMPORTS
### ====================================================================================================
import arcade
from utils import *
from random import *
import time
import pickle



class Process:

    ### ====================================================================================================
    ### PARAMETERS
    ### ====================================================================================================
    SCREEN_WIDTH  = int(960*1.75)
    SCREEN_HEIGHT = int(540*1.75)

    ### ====================================================================================================
    ### SCORE
    ### ====================================================================================================
    def initScore(self):
        self.score = 0

    def increaseScore(self):
        self.score += 1

    def drawScore(self):
        paramTxt = {"x": self.SCREEN_WIDTH - 5,
                    "y": self.SCREEN_HEIGHT - 5,
                    "alignH": "right",
                    "alignV": "top",
                    "message": "SCORE = " + str(self.score),
                    "size": 50,
                    "color": (160, 160, 160, 192),
                    }
        drawText(paramTxt)

    ### ====================================================================================================
    ### LIFE
    ### ====================================================================================================
    def initLife(self):
        self.life = self.LIFE_INIT

    def decreaseLife(self):
        self.life = max(0, self.life-1)

    def drawLife(self):
        # draw life border
        self.lifeBorder.draw()
        # draw life bars
        for i in range(self.life):
            self.lifeBars[i].draw()

    def checkEndOfLife(self):
        if self.life <= 0 and self.isRunning():
            self.stopGame()

    ### ====================================================================================================
    ### CHARACTERS
    ### ====================================================================================================
    def createCharacter(self):
        self.charSprites = []
        # Create RUN anims
        params = {
            "filePath"      : f"images/characters/ninja.png",
            "spriteBox"     : (7,1,120,120),
            "startIndex"    : 1,
            "endIndex"      : 6,
            "frameDuration" : 1/15,
            "size"          : (self.CHAR_W, self.CHAR_H),
            "flipH"         : True
        }
        self.charSprites.append( createAnimatedSprite(params) )
        params["flipH"] = False
        self.charSprites.append(createAnimatedSprite(params))
        # Create IDLE anims
        params = {
            "filePath"      : f"images/characters/ninja.png",
            "spriteBox"     : (7, 1, 120, 120),
            "startIndex"    : 0,
            "endIndex"      : 0,
            "frameDuration" : 1/15,
            "size"          : (self.CHAR_W, self.CHAR_H),
            "flipH"         : True
        }
        self.charSprites.append(createAnimatedSprite(params))
        params["flipH"] = False
        self.charSprites.append(createAnimatedSprite(params))
        # select default RIGHT IDLE
        self.characterSprite = self.charSprites[0]
        # Create position variables
        self.charX = self.SCREEN_WIDTH//2
        self.charY = self.SCREEN_HEIGHT//4+10
        # Create move variables
        self.moves = {"left":False, "right":False}
        self.sliding = False
        # direction variable
        self.charDirection = "right"

    def updateCharacter(self, deltaTime):
        # update character direction (if not sliding)
        if not self.sliding:
            if self.moves["left"] != self.moves["right"]:
                if self.moves["left"]:
                    self.charDirection = "left"
                elif self.moves["right"]:
                    self.charDirection = "right"

        # move char according to left/right or slide
        if (self.moves["left"] != self.moves["right"]) or self.sliding:
            deltaMove = self.SPEED*60*deltaTime
            if self.sliding:
                deltaMove *= 2
            if self.charDirection == "left":
                self.charX -= deltaMove
            else:
                self.charX += deltaMove

        # X range limitation
        self.charX = max(self.CHAR_W//3, self.charX)
        self.charX = min(self.SCREEN_WIDTH-self.CHAR_W//3, self.charX)


        # select animation
        idx = 0
        if self.charDirection == "right":
            idx += 1
        if (self.moves["left"] == self.moves["right"]) and not self.sliding:
            idx += 2
        self.characterSprite = self.charSprites[idx]

        # update sprite animation frame
        self.characterSprite.update_animation()

        # update sprite position
        self.characterSprite.center_x = self.charX
        self.characterSprite.center_y = self.charY

    def drawCharacter(self):
        self.characterSprite.draw()
        if self.DEBUG:
            arcade.draw_rectangle_outline(self.characterSprite.center_x,
                                          self.characterSprite.center_y,
                                          self.characterSprite.width*self.BOX_CHAR_RATIO,
                                          self.characterSprite.height*self.BOX_CHAR_RATIO,
                                          (255, 0, 255, 255))

    def moveCharacter(self,direction,isON):
        self.moves[direction] = isON

    ### ====================================================================================================
    ### BACKGROUNDS / PARALLAX
    ### ====================================================================================================
    def createBackGround(self):
        # Create sprite object
        self.backgrounds = []
        for i in range(6,0,-1):
            params = {
                "filePath": f"images/parallax/night/night{i}.png",
                "size"    : (self.SCREEN_WIDTH     , self.SCREEN_HEIGHT     ),
                "position": (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2)
            }
            bg0 = createFixedSprite(params)
            bg1 = createFixedSprite(params)
            self.backgrounds.append( (bg0, bg1) )

    def getParallaxDelta(self):
        # Get [-1,+1] dx value
        dx  = (self.charX - self.SCREEN_WIDTH // 2)
        dx /= (self.SCREEN_WIDTH // 2)
        dx  = -dx * self.BACKGROUND_SPEED * (self.SCREEN_WIDTH//2)
        return dx

    def updateBackgrounds(self):
        # get Parallax ratio (front layer)
        dx = self.getParallaxDelta()
        # move backgrounds according to offset dx
        for i in range(len(self.backgrounds)):
            bgs = self.backgrounds[i]
            bg0 = bgs[0]
            bg1 = bgs[1]
            bg0.center_x = dx*(i+1) + (self.SCREEN_WIDTH//2)
            if dx <= 0:
                bg1.center_x = bg0.center_x + self.SCREEN_WIDTH
            else:
                bg1.center_x = bg0.center_x - self.SCREEN_WIDTH

    def drawBackGround(self, exclude=()):
        for i in range(len(self.backgrounds)):
            if i not in exclude:
                bgs = self.backgrounds[i]
                bg0 = bgs[0]
                bg1 = bgs[1]
                bg0.draw()
                bg1.draw()


    ### ====================================================================================================
    ### ITEMS
    ### ====================================================================================================
    def initItemList(self):
        self.items = []
        self.itemGenTimer = 0
        # init pseudo random
        self.prng = Random(123456789)

    def generateItem(self, deltaTime):
        # increase timer
        self.itemGenTimer += deltaTime
        # check value
        if self.itemGenTimer > self.ITEM_INTERVAL:
            # reduce counter
            self.itemGenTimer -= self.ITEM_INTERVAL
            # Generate one item
            x   = self.prng.randint(0,self.SCREEN_WIDTH)
            y   = self.SCREEN_HEIGHT
            spd = self.prng.random()*(self.ITEM_MAX_SPEED-self.ITEM_MIN_SPEED) + self.ITEM_MIN_SPEED
            idx = self.prng.randint(0,5)
            rot = self.prng.randint(5,15)
            params = {
                "filePath"      : f"images/items/shuriken.png",
                "spriteBox"     : (4, 2, 175, 175),
                "startIndex"    : 0,
                "endIndex"      : 7,
                "frameDuration" : 1 / 15,
                "size"          : (self.ITEM_SIZE, self.ITEM_SIZE),
                "position"      : (x,y),
                "filterColor"   : (255,255,255,220)
            }
            sprite = createAnimatedSprite(params)
            sprite.set_texture(idx)
            self.items.append((sprite,x,spd,rot))

    def updateItems(self,deltaTime):
        for itm in self.items:
            # retrieve information
            sprite = itm[0]
            xRef   = itm[1]
            speed  = itm[2]
            rot    = itm[3]
            # make the item go down
            sprite.center_y -= speed*60*deltaTime
            # update X position according to xRef and parallax ratio
            dx = self.getParallaxDelta()
            sprite.center_x = xRef +  dx * (len(self.backgrounds))
            # make the item turn
            sprite.angle += rot
            if sprite.center_y < self.ITEM_MIN_Y:
                # item has been missed, remove from list and decrese life
                self.playMissSound()
                self.decreaseLife()
                self.items.remove(itm)
                self.createMissBurst(xRef,sprite.center_y)

    def drawItems(self):
        for itm in self.items:
            sprite = itm[0]
            sprite.draw()
            if self.DEBUG:
                arcade.draw_rectangle_outline(sprite.center_x,
                                              sprite.center_y,
                                              sprite.width*self.BOX_ITEM_RATIO,
                                              sprite.height*self.BOX_ITEM_RATIO,
                                              (255,0,255,255))

    ### ====================================================================================================
    ### COLLISIONS (box)
    ### ====================================================================================================
    def isColliding(self, box1, box2):
        if (box1["x2"] < box2["x1"]) or (box1["x1"] > box2["x2"]) or (box1["y2"] < box2["y1"]) or (box1["y1"] > box2["y2"]):
            return False
        else:
            return True

    def checkItemCharCollision(self):
        for itm in self.items:
            sprite = itm[0]
            box1 = {"x1":self.characterSprite.center_x - self.characterSprite.width *self.BOX_CHAR_RATIO //2,
                    "y1":self.characterSprite.center_y - self.characterSprite.height*self.BOX_CHAR_RATIO //2,
                    "x2":self.characterSprite.center_x + self.characterSprite.width *self.BOX_CHAR_RATIO //2,
                    "y2":self.characterSprite.center_y + self.characterSprite.height*self.BOX_CHAR_RATIO //2
                   }
            box2 = {"x1":sprite.center_x - sprite.width *self.BOX_ITEM_RATIO //2,
                    "y1":sprite.center_y - sprite.height*self.BOX_ITEM_RATIO //2,
                    "x2":sprite.center_x + sprite.width *self.BOX_ITEM_RATIO //2,
                    "y2":sprite.center_y + sprite.height*self.BOX_ITEM_RATIO //2
                   }
            if self.isColliding(box1, box2):
                # item is colliding with character : add score and remove item
                self.playTakeSound()
                self.increaseScore()
                self.items.remove(itm)
                self.createTakeBurst(itm[1],sprite.center_y)


    ### ====================================================================================================
    ### GAME STATE
    ### ====================================================================================================
    def initEndGame(self):
        self.rewindGame()

    def isReadyToStart(self):
        return self.state == "ready"

    def isRunning(self):
        return self.state == "running"

    def isFinished(self):
        return self.state == "finished"

    def startGame(self):
        self.state = "running"

    def stopGame(self):
        self.state = "finished"
        self.saveNewScore(self.score)

    def rewindGame(self):
        self.score = 0
        self.life  = self.LIFE_INIT
        self.state = "ready"

    ### ====================================================================================================
    ### HUD
    ### ====================================================================================================
    def initHUD(self):
        self.welcomeTxtParam = {
            "x"      : self.SCREEN_WIDTH//2,
            "y"      : self.SCREEN_HEIGHT//2,
            "alignH" : "center",
            "alignV" : "center",
            "message": "Press ENTER key\nor START button",
            "size"   : 100,
            "color"  : (255, 255, 255, 200),
        }
        self.endTxtParam = {
            "x"      : self.SCREEN_WIDTH//2,
            "y"      : self.SCREEN_HEIGHT//2,
            "alignH" : "center",
            "alignV" : "center",
            "message": "Game OVER",
            "size"   : 60,
            "color"  : (255, 255, 255, 200),
        }
        borderParam = {
            "filePath": f"images/interface/bar.png",
            "size": (672, 64),
            "position": (672//2 + 5, self.SCREEN_HEIGHT - 64//2 - 5),
            "filterColor": (255,255,255,180)
        }
        self.lifeBorder = createFixedSprite(borderParam)
        self.lifeBars = []
        for i in range(self.LIFE_INIT):
            red   = int(min(255, 255*(2-i/10)))
            green = int(min(255, 255*(  i/10)))
            blue  = 32
            eltParam = {
                "filePath": f"images/interface/barElt.png",
                "size": (30, 40),
                "position": (22 + i*32 + 15, self.SCREEN_HEIGHT - 64//2 - 5),
                "filterColor": (red,green,blue,180)
            }
            self.lifeBars.append( createFixedSprite(eltParam) )

    def displayStartMessage(self):
        t = int(time.time()*1000)%1000
        if t < 500:
            drawText(self.welcomeTxtParam)

    def displayEndMessage(self):
        msg = "  Game OVER\n"
        msg += f"Your score is {self.score}\n\n"
        msg += "- HIGH SCORES -\n"
        for hs in self.highScores[:5]:
            msg += f"         {hs}\n"
        self.endTxtParam["message"] = msg
        drawText(self.endTxtParam)

    def drawHUD(self):
        # draw score and life
        self.drawScore()
        self.drawLife()
        # draw message according to game state
        if self.isReadyToStart():
            self.displayStartMessage()
        elif self.isFinished():
            self.displayEndMessage()

    ### ====================================================================================================
    ### HIGH SCORES
    ### ====================================================================================================
    def initHighScores(self):
        # open the text file (or create it if it does not exist)
        self.highScores = [0,1,2,3,4,5,6,7,8]
        try:
            with open('highscores.dat', 'rb') as handle:
                self.highScores = pickle.load(handle)
        except:
            pass
        print(self.highScores)

    def saveNewScore(self,newScore):
        # Add score
        self.highScores.append(newScore)
        #sort all the values in it
        self.highScores = sorted(self.highScores, reverse=True)
        #only keep the 10 greatest values
        if len(self.highScores)>10:
            self.highScores = self.highScores[:10]
        # save structure into file
        with open('highscores.dat', 'wb') as handle:
            pickle.dump(self.highScores,handle)
        print(self.highScores)

    ### ====================================================================================================
    ### SOUNDS
    ### ====================================================================================================
    def createSounds(self):
        self.sndTake = createSound("sounds/bling.wav")
        self.sndMiss = createSound("sounds/crash.wav")

    def playTakeSound(self):
        self.sndTake.play()

    def playMissSound(self):
            self.sndMiss.play()

    ### ====================================================================================================
    ### PARTICLE EFFECTS
    ### ====================================================================================================
    def initParticleEffects(self):
        # burst structures
        self.takeBurst = []
        self.missBurst = []
        # char particle
        paramPE = { "x0"          : 2000,
                    "y0"          : 2000,
                    "partNB"      : 200,
                    "partSize"    : 128,
                    "partScale"   : 1.5,
                    "partSpeed"   : 0.0,
                    "maxLifeTime" : 0.25,
                    "color"       : (255,128,0),
                    "startAlpha"  : 15,
                    "endAlpha"    : 0,
                    "spriteBox"   : (7,1,120,120),
                    "spriteSelect": (6,0),
                    "textureFile" : "images/characters/ninja.png"
        }
        self.charEmitterRight= createParticleEmitter(paramPE)
        paramPE["flipH"] = True
        self.charEmitterLeft = createParticleEmitter(paramPE)

    def createTakeBurst(self, x, y):
        # create burst
        paramB = {"x0": x,
                  "y0": y,
                  "partInterval": 0.03,
                  "totalDuration": 0.25,
                  "partSize": 50,
                  "partScale": 1.0,
                  "partSpeed": 10.0,
                  "color": (0, 0, 0),
                  "startAlpha": 100,
                  "endAlpha": 25,
                  "imagePath": "images/items/star.png"
                  }
        newBurst = createParticleBurst(paramB)
        self.takeBurst.append((newBurst,x))

    def createMissBurst(self, x, y):
        # create burst
        paramB = {"x0": x,
                  "y0": y,
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
        self.missBurst.append((newBurst,x))

    def updateAllBursts(self):
        for b in self.takeBurst:
            b[0].center_x = self.getParallaxDelta()*len(self.backgrounds) + b[1]
            b[0].update()
            if b[0].can_reap():
                self.takeBurst.remove(b)
        # miss bursts must move like the parallax
        for b in self.missBurst:
            b[0].center_x = self.getParallaxDelta()*len(self.backgrounds) + b[1]
            b[0].update()
            if b[0].can_reap():
                self.missBurst.remove(b)

    def updateCharEmitter(self):
        self.charEmitterLeft.center_x  = 10000
        self.charEmitterLeft.center_y  = 10000
        self.charEmitterRight.center_x = 10000
        self.charEmitterRight.center_y = 10000
        if (self.moves["left"] != self.moves["right"]) or self.sliding:
            if self.charDirection == "left":
                self.charEmitterLeft.center_x = self.charX
                self.charEmitterLeft.center_y = self.charY
            else:
                self.charEmitterRight.center_x = self.charX
                self.charEmitterRight.center_y = self.charY
        self.charEmitterLeft.update()
        self.charEmitterRight.update()

    def drawAllBursts(self):
        for b in self.takeBurst:
            b[0].draw()
        for b in self.missBurst:
            b[0].draw()

    def drawCharEmitter(self):
        self.charEmitterLeft.draw()
        self.charEmitterRight.draw()


    ### ====================================================================================================
    ### CLOUDS
    ### ====================================================================================================
    def initClouds(self):
        self.clouds = []
        self.cloudTimer = 0

    def generateCloud(self):
        # create random speed
        speed = random() * (self.CLOUD_SPEED_MAX - self.CLOUD_SPEED_MIN) + self.CLOUD_SPEED_MIN
        # create position (random Y)
        x = -(self.SCREEN_WIDTH+384)//2
        y = self.SCREEN_HEIGHT - random()*self.CLOUD_RANGE_HEIGHT
        # Create random sprite for cloud
        alpha = int(random()*128 + 32)
        params = {
            "filePath": f"images/items/clouds.png",
            "spriteBox"     : (7,1,384,128),
            "startIndex"    : 0,
            "endIndex"      : 6,
            "frameDuration" : 1/15,
            "size"          : (200, 100),
            "filterColor"   : (255,255,255,alpha)
        }
        sprite = createAnimatedSprite(params)
        sprite.center_y = y
        # Add cloud into list
        self.clouds.append( [sprite,x,speed] )

    def updateClouds(self,deltaTime):
        # generate new clouds
        self.cloudTimer += deltaTime
        if self.cloudTimer >= self.CLOUD_INTERVAL:
            self.cloudTimer -= self.CLOUD_INTERVAL
            self.generateCloud()

        # make clouds go forward
        for i in range(len(self.clouds)):
            cld = self.clouds[i]
            # Get parameters
            sprite = cld[0]
            refX   = cld[1]
            speed  = cld[2]
            # Update refX and store
            refX  += speed*60*deltaTime
            self.clouds[i][1] = refX
            # update sprite position according to refX and parallax offset
            sprite.center_x = self.getParallaxDelta()*2.5 + refX
        # Destroy clouds if out of area
        for cld in self.clouds:
            if cld[1]> self.SCREEN_WIDTH * 1.5 :
                self.clouds.remove(cld)

    def drawClouds(self):
        for cld in self.clouds:
            cld[0].draw()



    ### ====================================================================================================
    ### CONSTRUCTOR
    ### ====================================================================================================
    def __init__(self):
        # Character constants
        self.DEBUG              = True
        self.CHAR_W             = 170
        self.CHAR_H             = 170
        self.SPEED              = 15
        self.ITEM_MIN_SPEED     = 2
        self.ITEM_MAX_SPEED     = 7
        self.ITEM_SIZE          = 100
        self.ITEM_MIN_Y         = 100
        self.ITEM_INTERVAL      = 1.0
        self.BOX_CHAR_RATIO     = 0.75
        self.BOX_ITEM_RATIO     = 0.75
        self.LIFE_INIT          = 20
        self.BACKGROUND_SPEED   = 0.15
        self.CLOUD_RANGE_HEIGHT = 400
        self.CLOUD_SPEED_MIN    = 0.1
        self.CLOUD_SPEED_MAX    = 4
        self.CLOUD_INTERVAL     = 1


    ### ====================================================================================================
    ### INIT
    ### ====================================================================================================
    def setup(self):
        self.initEndGame()
        self.createCharacter()
        self.createBackGround()
        self.initItemList()
        self.initScore()
        self.initLife()
        self.initHUD()
        self.initHighScores()
        self.createSounds()
        self.initParticleEffects()
        self.initClouds()

        # params = {
        #     "filePath"      : f"images/characters/ninja.png",
        #     "spriteBox"     : (7,1,120,120),
        #     "startIndex"    : 1,
        #     "endIndex"      : 6,
        #     "frameDuration" : 1/15,
        #     "size"          : (self.CHAR_W, self.CHAR_H),
        #     "flipH"         : False
        # }
        # self.TEST = createAnimatedSprite(params)
        # self.TEST.center_x = 200
        # self.TEST.center_y = 200
        # self.TEST.repeat_count_x = 1


    ### ====================================================================================================
    ### UPDATE
    ### ====================================================================================================
    def update(self,deltaTime):
        # always update backgrounds
        self.updateBackgrounds()
        # check end of game
        self.checkEndOfLife()
        # generate only in running state
        if self.isRunning():
            self.generateItem(deltaTime)
        # always update character and items and bursts
        self.updateCharacter(deltaTime)
        self.updateItems(deltaTime)
        self.updateAllBursts()
        self.updateCharEmitter()
        # only check for collisions with character if game is running
        if self.isRunning():
            self.checkItemCharCollision()
        # update clouds
        self.updateClouds(deltaTime)


        # self.TEST.update_animation()

    ### ====================================================================================================
    ### RENDERING
    ### ====================================================================================================
    def draw(self):
        self.drawBackGround((2,3,4,5))
        self.drawClouds()
        self.drawBackGround((0,1,5))

        self.drawCharEmitter()
        self.drawCharacter()

        self.drawItems()
        self.drawAllBursts()

        self.drawBackGround((0,1,2,3,4))
        self.drawHUD()


        # self.TEST.draw()


    ### ====================================================================================================
    ### KEYBOARD EVENTS
    ### key is taken from : arcade.key.xxx
    ### ====================================================================================================
    def onKeyEvent(self,key,isPressed):
        ###print(f"key={key} - isPressed={isPressed}")
        # move character with LEFT and RIGHT arrows
        if key==arcade.key.LEFT:
            self.moveCharacter("left",isPressed)
        elif key==arcade.key.RIGHT:
            self.moveCharacter("right",isPressed)
        # START when ready / REWIND when finished
        if key== arcade.key.ENTER and not isPressed:
            if self.isReadyToStart():
                self.startGame()
            if self.isFinished():
                self.rewindGame()
        # MOVE character fast when holding SPACE
        if key == arcade.key.SPACE:
            self.sliding = isPressed



    ### ====================================================================================================
    ### GAMEPAD BUTTON EVENTS
    ### buttonName can be "A", "B", "X", "Y", "LB", "RB", "VIEW", "MENU", "LSTICK", "RSTICK"
    ### ====================================================================================================
    def onButtonEvent(self, gamepadNum,buttonName,isPressed):
        ###print(f"GamePad={gamepadNum} - ButtonNum={buttonName} - isPressed={isPressed}")
        # START when ready / REWIND when finished
        if buttonName == "MENU" and not isPressed:
            if self.isReadyToStart():
                self.startGame()
            if self.isFinished():
                self.rewindGame()
        # slide when pressing any button
        if buttonName != "MENU":
            self.sliding = isPressed



    ### ====================================================================================================
    ### GAMEPAD AXIS EVENTS
    ### axisName can be "X", "Y", "RX", "RY", "Z"
    ### ====================================================================================================
    def onAxisEvent(self, gamepadNum,axisName,analogValue):
        ###print(f"GamePad={gamepadNum} - AxisName={axisName} - Value={analogValue}")
        # Move character with X axis
        if axisName == "X":
            if analogValue < -0.5:
                self.moveCharacter("left", True)
            elif analogValue > 0.5:
                self.moveCharacter("right", True)
            else:
                self.moveCharacter("left" , False)
                self.moveCharacter("right", False)



    ### ====================================================================================================
    ### MOUSE MOTION EVENTS
    ### ====================================================================================================
    def mouseMotionEvent(self,x,y,dx,dy):
        print(f"MOUSE MOTION : x={x}/y={y} dx={dx}/dy={dy}")



    ### ====================================================================================================
    ### MOUSE BUTTON EVENTS
    ### ====================================================================================================
    def mouseButtonEvent(self,x,y,buttonNum,isPressed):
        print(f"MOUSE BUTTON : x={x}/y={y} buttonNum={buttonNum} isPressed={isPressed}")




