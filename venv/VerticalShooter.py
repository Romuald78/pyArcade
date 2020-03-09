### ====================================================================================================
### IMPORTS
### ====================================================================================================
import arcade
from Utils import *
from random import *
import time
import math

SCREEN_WIDTH  = 960
SCREEN_HEIGHT = 960
var = Variables()



### ====================================================================================================
### INITIALISATION OF YOUR VARIABLES
### ====================================================================================================
def setup():
    # -------------------------------------------------------------------
    # BACKGROUND
    arcade.set_background_color(arcade.color.BLACK)
    var.bg1 = createSprite(f":resources:images/backgrounds/stars.png", (SCREEN_WIDTH, SCREEN_HEIGHT), True)
    var.bg1.center_x = SCREEN_WIDTH / 2
    var.bg1.center_y = (SCREEN_HEIGHT/2) + (var.bg1.height/2)
    var.bg2 = createSprite(f":resources:images/backgrounds/stars.png", (SCREEN_WIDTH, SCREEN_HEIGHT), True)
    var.bg2.center_x = SCREEN_WIDTH / 2
    var.bg2.center_y = var.bg1.center_y - var.bg1.height
    # Ship + Movement
    var.ship = createSprite(f":resources:images/space_shooter/playerShip1_green.png",(50,50),True)
    var.move = [0,0,0,0]
    var.ship.center_x = SCREEN_WIDTH/2
    var.ship.center_y = 50
    # Laser beams
    var.nbLasers = 5;
    var.lasers = []
    # Enemies
    var.enemies = []
    var.enemyTimer = 0
    var.enemyFireStep = 1.0
    # life
    var.life = 5
    var.lifeShips = []
    for i in range(var.life):
        ls = createSprite(f":resources:images/space_shooter/playerLife1_orange.png",(30,30),True)
        ls.center_y = SCREEN_HEIGHT - 30
        ls.center_x = 30 + 50*i
        var.lifeShips.append(ls)
    # turret direction
    var.turretX = 0
    var.turretY = 0
    var.turretMissiles = []
    var.turretFiring = False
    var.turretTimeStep = 0
    # emitters
    var.emits = []
    # score
    var.score = 0
    # -------------------------------------------------------------------



### ====================================================================================================
### UPDATE OF YOUR GAME DATA
### ====================================================================================================
def update(deltaTime):
    # -------------------------------------------------------------------
    # update animation
    var.ship.update()

    # each frame we increase the enemy fire rate
    var.enemyFireStep += 0.001


    if var.life > 0:
        # update movement
        var.ship.center_x += (-var.move[0]+var.move[1])*deltaTime*60*5
        var.ship.center_y += (var.move[2]-var.move[3])*deltaTime*60*5
        # Saturate position
        if var.ship.center_x < 0:
            var.ship.center_x = 0
        if var.ship.center_x >= SCREEN_WIDTH:
            var.ship.center_x = SCREEN_WIDTH
        if var.ship.center_y < 0:
            var.ship.center_y = 0
        if var.ship.center_y >= SCREEN_HEIGHT:
            var.ship.center_y = SCREEN_HEIGHT

    # move lasers
    for lz in var.lasers:
        lz.center_y += deltaTime*60*10;
        if lz.center_y >= SCREEN_HEIGHT:
            var.lasers.remove(lz)

    if var.life > 0:
        # Create and missiles
        var.turretTimeStep += deltaTime
        if var.turretFiring:
            # if the direction is correct
            if abs(var.turretX) > 0.5 or abs(var.turretY) > 0.5:
                # if firing, reduce timer and create missile
                if var.turretTimeStep >= 0.2:
                    var.turretTimeStep = 0
                    missile = createSprite(f":resources:images/pinball/pool_cue_ball.png", (5, 5), True)
                    missile.center_x = var.ship.center_x
                    missile.center_y = var.ship.center_y
                    var.turretMissiles.append( (missile,var.turretX, var.turretY, "ship") )

    # update missile positions
    for m in var.turretMissiles:
        m[0].center_x += m[1]*deltaTime*60*6.5
        m[0].center_y += m[2]*deltaTime*60*6.5
        # destroy missiles when out of area
        if m[0].center_x < 0 or m[0].center_x >= SCREEN_WIDTH or m[0].center_y < 0 or m[0].center_y >= SCREEN_HEIGHT:
            var.turretMissiles.remove(m)

    if var.life > 0:
        # increase enemy timer and check for enemy creation
        var.enemyTimer += deltaTime
        if var.enemyTimer >= 1:
            var.enemyTimer -= 1
            enemy = createSprite(f":resources:images/enemies/saw.png", (50, 50), False)
            #set random position
            enemy.center_x = randint(0,SCREEN_WIDTH)
            enemy.center_y = SCREEN_WIDTH + 50
            var.enemies.append(enemy)

    # update position for all enemies
    for e in var.enemies:
        e.center_y -= deltaTime*60*3
        # check for destroy
        if e.center_y < 0:
            var.enemies.remove(e)

    # enemies fire randomly toward the ship direction
    for e in var.enemies:
        isFire = randint(0,10000)/100
        if isFire <= var.enemyFireStep:
            missile = createSprite(f":resources:images/pinball/pool_cue_ball.png", (5, 5), True)
            missile.center_x = e.center_x
            missile.center_y = e.center_y
            dx = var.ship.center_x-e.center_x
            dy = var.ship.center_y-e.center_y
            nrm = math.sqrt(dx*dx+dy*dy)
            var.turretMissiles.append((missile, dx/nrm, dy/nrm, "enemy"))

    # update BG
    var.bg1.center_y -= 2
    if var.bg1.center_y <= SCREEN_HEIGHT/2:
        var.bg1.center_y += SCREEN_HEIGHT
    var.bg2.center_y = var.bg1.center_y - var.bg1.height

    # CHeck collisions between lasers and enemies
    for l in var.lasers:
        for e in var.enemies:
            if abs(l.center_x-e.center_x) < 20 and abs(l.center_y-e.center_y) < 20:
                var.lasers.remove(l)
                var.enemies.remove(e)
                emitter = createParticleBurst(e.center_x, e.center_y, 0.02, 0.25, 100, 0.25, 5.0, (255, 0, 0, 255), 90, 25)
                var.emits.append(emitter)
                var.score += 1

    # CHeck collisions between missiles and enemies
    for t in var.turretMissiles:
        for e in var.enemies:
            if abs(t[0].center_x-e.center_x) < 20 and abs(t[0].center_y-e.center_y) < 20:
                if t[3] != "enemy":
                    var.turretMissiles.remove(t)
                    var.enemies.remove(e)
                    emitter = createParticleBurst(e.center_x,e.center_y,0.02, 0.25, 100, 0.25, 5.0, (255, 0, 0, 255), 90, 25)
                    var.emits.append(emitter)
                    var.score += 1

    # CHeck collisions between missiles and ship
    for t in var.turretMissiles:
        if abs(var.ship.center_x-t[0].center_x) < 30 and abs(var.ship.center_y-t[0].center_y) < 25:
            if t[3] != "ship":
                var.turretMissiles.remove(t)
                var.life -= 1
                emit = createParticleBurst(var.ship.center_x, var.ship.center_y, 0.025, 0.15, 100, 0.5, 3.0, (255, 128, 128, 255), 100, 25)
                var.emits.append(emit)

    # check collisions between ship and enemies
    for e in var.enemies:
        if abs(var.ship.center_x-e.center_x) < 50 and abs(var.ship.center_y-e.center_y) < 40:
            var.enemies.remove(e)
            var.life -= 1
            x0 = 30 + 50 * var.life
            y0 = SCREEN_HEIGHT - 30
            emit = createParticleBurst(x0, y0, 0.025, 0.3, 75, 0.5, 3.0, (255, 128, 128, 255), 100, 25,f":resources:images/space_shooter/playerLife1_orange.png")
            var.emits.append(emit)

    # update emitters
    for emit in var.emits:
        emit.update()

    # remove finished emitters
    for emit in var.emits:
        if emit.can_reap():
            var.emits.remove(emit)
    #-------------------------------------------------------------------



### ====================================================================================================
### DRAW YOUR IMAGES ON THE SCREEN
### ====================================================================================================
def draw():
    #-------------------------------------------------------------------
    # draw bg
    var.bg1.draw()
    var.bg2.draw()
    # draw lasers
    for lz in var.lasers:
        lz.draw()
    # draw missiles
    for m in var.turretMissiles:
        m[0].draw()
    # draw ship
    var.ship.draw()
    # draw enemies
    for e in var.enemies:
        e.draw()
    # draw emitters
    for emit in var.emits:
        emit.draw()
    # draw lives
    for i in range(var.life):
        var.lifeShips[i].draw()
    # draw score
    arcade.draw_text("SCORE = "+str(var.score), SCREEN_WIDTH-25, SCREEN_HEIGHT-45, arcade.color.ORANGE, 30, anchor_x="right", anchor_y="top", bold=True    )
    #-------------------------------------------------------------------



### ====================================================================================================
### FUNCTION CALLED WHEN YOU PRESS A KEY ON THE KEYBOARD
### ====================================================================================================
def onKeyEvent(key,isPressed):
    #-------------------------------------------------------------------
    if key == arcade.key.LEFT:
        if isPressed:
            var.move[0] = 1
        else:
            var.move[0] = 0
    if key == arcade.key.RIGHT:
        if isPressed:
            var.move[1] = 1
        else:
            var.move[1] = 0
    if key == arcade.key.UP:
        if isPressed:
            var.move[2] = 1
        else:
            var.move[2] = 0
    if key == arcade.key.DOWN:
        if isPressed:
            var.move[3] = 1
        else:
            var.move[3] = 0
    # Laser shoot
    if key == arcade.key.SPACE:
        if var.life > 0:
            if len(var.lasers) < var.nbLasers:
                laz = createSprite(f":resources:images/space_shooter/laserRed01.png",(50,50),False)
                laz.center_x = var.ship.center_x
                laz.center_y = var.ship.center_y
                var.lasers.append(laz)

    # RESTART GAME
    if key == arcade.key.ENTER:
        var.life = 5
        var.score = 0
        var.ship.center_x = SCREEN_WIDTH / 2
        var.ship.center_y = 50
        var.emits = []
        var.enemies = []
        var.enemyFireStep = 1.0
    #-------------------------------------------------------------------



### ====================================================================================================
### FUNCTION CALLED WHEN YOU PRESS A BUTTON ON A GAMEPAD CONTROLLER
### ====================================================================================================
def onButtonEvent(gamepadNum,buttonNum,isPressed):
    #-------------------------------------------------------------------
    #Laser shoot
    if isPressed:
        if len(var.lasers) < var.nbLasers:
            laz = createSprite(f":resources:images/space_shooter/laserRed01.png",(50,50),False)
            laz.center_x = var.ship.center_x
            laz.center_y = var.ship.center_y
            var.lasers.append(laz)
    #-------------------------------------------------------------------



### ====================================================================================================
### FUNCTION CALLED WHEN YOU MOVE AN AXIS ON A GAMEPAD CONTROLLER
### ====================================================================================================
def onAxisEvent(gamepadNum,axisName,analogValue):
    #-------------------------------------------------------------------
    if axisName == "x":
        if analogValue <= -0.2:
            var.move[0] = -analogValue
        elif analogValue >= 0.2:
            var.move[1] = analogValue
        else:
            var.move[0] = var.move[1] = 0
    if axisName == "y":
        if analogValue <= -0.2:
            var.move[2] = -analogValue
        elif analogValue >= 0.2:
            var.move[3] = analogValue
        else:
            var.move[2] = var.move[3] = 0
    # TURRET
    if axisName == "rx":
        var.turretX = analogValue
    if axisName == "ry":
        var.turretY = -analogValue
    if axisName == "z":
        var.turretFiring = abs(analogValue) >= 0.5
    #-------------------------------------------------------------------


