### ====================================================================================================
### IMPORTS
### ====================================================================================================
import arcade
from Utils import *
from random import *
import time
var = Variables()



### ====================================================================================================
### INITIALISATION OF YOUR VARIABLES
### ====================================================================================================
def setup():
    #-------------------------------------------------------------------
    # ROBOT SPRITE
    var.robot = createSprite(f":resources:images/animated_characters/robot/robot_idle.png",(200,200))
    # robot position
    var.robot.center_x = 100
    var.robot.center_y = 100
    #-------------------------------------------------------------------

    # BACKGROUND
    arcade.set_background_color(arcade.color.BLUE)
    var.bg = createSprite(f":resources:images/backgrounds/abstract_1.jpg",(SCREEN_WIDTH,SCREEN_HEIGHT),True)
    var.bg.center_x = SCREEN_WIDTH / 2
    var.bg.center_y = SCREEN_HEIGHT / 2
    # robot position
    var.robot.center_x = 100
    var.robot.center_y = 100
    # MOVEMENT
    var.moveLeft  = False
    var.moveRight = False
    # GEM LIST
    var.gems = []
    # LIFE
    var.life = 5
    var.stars = []
    for i in range(var.life):
        star = createSprite(f":resources:images/items/star.png",(100,100))
        star.center_y = SCREEN_HEIGHT - 50;
        star.center_x = 50 + 75 * i
        var.stars.append(star)
    # TIMER
    var.time = 0
    # SCORE
    var.score = 0
    # DASH
    var.dashCD = 0
    var.dash   = False
    # EMIT
    var.emit = createParticleEmitter(var.robot.center_x,var.robot.center_y,100,50,0.1,2.5,(255,32,32,192),100,25)
    var.explodeStar = None
    var.getGem = None



### ====================================================================================================
### UPDATE OF YOUR GAME DATA
### ====================================================================================================
def update(deltaTime):
    # -------------------------------------------------------------------
    pass
    #-------------------------------------------------------------------

    # DASH INCREASE
    var.dashCD += deltaTime
    # TIMER INCREASE
    var.time += deltaTime
    # process game only if life is greater than zero
    if var.life > 0:
        # ROBOT MOVEMENT
        if var.moveLeft:
            var.robot.center_x -= 10*deltaTime*60;
        if var.moveRight:
            var.robot.center_x += 10*deltaTime*60;
        var.robot.center_x = max(0,min(SCREEN_WIDTH,var.robot.center_x))
        var.robot.center_y = max(0,min(SCREEN_WIDTH,var.robot.center_y))
        # ROBOT DASH
        if var.dash and var.dashCD >= 3:
            if var.moveLeft and not var.moveRight:
                var.robot.center_x -= 200;
                var.dash = False
                var.dashCD = 0
            if not var.moveLeft and var.moveRight:
                var.robot.center_x += 200;
                var.dash = False
                var.dashCD = 0
        if var.dash and var.dashCD < 3:
            var.dash = False
        # GEM GENERATION
        if var.time >= 1:
            var.time -= 1
            gem = createSprite(f":resources:images/items/gemYellow.png",(75,75));
            gem.center_x = randint(0,SCREEN_WIDTH)
            gem.center_y = SCREEN_HEIGHT+100
            var.gems.append( gem)
    # GEM MOVEMENT
    for g in var.gems:
        # MOVE GEM
        g.center_y -= 5*deltaTime*60
        # MISS GEM
        if g.center_y < 0:
            var.gems.remove(g)
            var.life -= 1
            y0 = SCREEN_HEIGHT - 50;
            x0 = 50 + 75 * var.life
            var.explodeStar = createParticleBurst(x0, y0, 0.002, 0.10, 25, 0.25, 4.5, (255, 255, 32, 200),
                                                  uniform(0.25, 0.5), 100, 0)
        # PICK UP GEM
        elif g.center_y < 100:
            if abs( var.robot.center_x - g.center_x) < 50:
                var.gems.remove(g)
                var.score += 1
                y0 = g.center_y
                x0 = g.center_x
                var.explodeStar = createParticleBurst(x0, y0, 0.002, 0.15, 25, 0.25, 4.5, (255, 255, 32, 200),
                                                      uniform(0.25, 0.5), 100, 0)
    # DASH EMIT
    if var.emit:
        var.emit.center_x = var.robot.center_x+2
        var.emit.center_y = var.robot.center_y+27
        var.emit.update()
    # EXPLODE STAR EMIT
    if var.explodeStar:
        var.explodeStar.update()
    # GET GEM EMIT
    if var.getGem:
        var.getGem.update()



### ====================================================================================================
### DRAW YOUR IMAGES ON THE SCREEN
### ====================================================================================================
def draw():
    # BACKGROUND
    var.bg.draw()

    #-------------------------------------------------------------------
    var.robot.draw()
    #-------------------------------------------------------------------

    # DASH EMIT
    if var.dashCD >= 3:
        var.emit.draw()
    # STARS
    for i in range(var.life):
        var.stars[i].draw()
    # EXPLODE STAR
    if var.explodeStar:
        var.explodeStar.draw()
    # GET GEM
    if var.getGem:
        var.getGem.draw()
    # SCORE TEXT
    arcade.draw_text("SCORE = "+str(var.score), SCREEN_WIDTH-25, SCREEN_HEIGHT-45, arcade.color.ORANGE, 30, anchor_x="right", anchor_y="top", bold=True    )
    # GEMS
    for g in var.gems:
        g.draw()



### ====================================================================================================
### FUNCTION CALLED WHEN YOU PRESS A KEY ON THE KEYBOARD
### ====================================================================================================
def onKeyEvent(key,isPressed):
    #-------------------------------------------------------------------
    if key == arcade.key.SPACE:
        if isPressed :
            print("SPACE KEY has been pressed !")
        else:
            print("SPACE KEY has been released !")
    #-------------------------------------------------------------------

    if key == arcade.key.LEFT:
        var.moveLeft = isPressed
    if key == arcade.key.RIGHT:
        var.moveRight = isPressed
    if key == arcade.key.ENTER and isPressed:
        var.life   = 5
        var.gems   = []
        var.score  = 0
        var.dash   = False
        var.dashCD = 0
        var.time = 0
    if key == arcade.key.D and isPressed:
        var.dash = True



### ====================================================================================================
### FUNCTION CALLED WHEN YOU PRESS A BUTTON ON A GAMEPAD CONTROLLER
### ====================================================================================================
def onButtonEvent(gamepadNum,buttonNum,isPressed):
    #-------------------------------------------------------------------
    pass
    #-------------------------------------------------------------------

    if isPressed:
        var.dash = True



### ====================================================================================================
### FUNCTION CALLED WHEN YOU MOVE AN AXIS ON A GAMEPAD CONTROLLER
### ====================================================================================================
def onAxisEvent(gamepadNum,axisName,analogValue):
    #-------------------------------------------------------------------
    pass
    #-------------------------------------------------------------------

    if axisName == "x":
        if analogValue < -0.5:
            var.moveLeft = True
            var.moveRight = False
        elif analogValue > 0.5:
            var.moveRight = True
            var.moveLeft = False
        else:
            var.moveLeft= False
            var.moveRight = False


