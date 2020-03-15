### ====================================================================================================
### IMPORTS
### ====================================================================================================
import arcade
from Utils import *
from random import *
import time
import math

SCREEN_WIDTH  = 900
SCREEN_HEIGHT = 900
var = Variables()

# UP / RIGHT / DOWN / LEFT
NOTES = [f":resources:images/items/gemYellow.png",
         f":resources:images/items/gemRed.png",
         f":resources:images/items/gemGreen.png",
         f":resources:images/items/gemBlue.png"
        ]

ANGLES = [0,-90,180,90]
DX = [0,-1,0,1]
DY = [-1,0,1,0]



### ====================================================================================================
### INITIALISATION OF YOUR VARIABLES
### ====================================================================================================
def setup():
    #-------------------------------------------------------------------
    # bg sprite
    var.bg = createSprite(f":resources:images/backgrounds/abstract_2.jpg", (SCREEN_WIDTH,SCREEN_HEIGHT), True)
    var.bg.center_x = SCREEN_WIDTH/2
    var.bg.center_y = SCREEN_HEIGHT / 2
    # target Sprites
    var.targets = []
    for i in range(4):
        tgt = createSprite(NOTES[i], (50,50), True)
        tgt.center_x = SCREEN_WIDTH/2  - DX[i]*50
        tgt.center_y = SCREEN_HEIGHT/2 - DY[i]*50
        tgt.angle = ANGLES[i]
        var.targets.append(tgt)
    # GENERATION
    var.timer = 0
    var.timeStep = 3.5
    var.nextTempo = randint(1,4);
    # note list
    var.notes = []
    # buttons events
    var.buttons = [False,False,False,False]
    # score
    var.nbHits = 0
    var.cumul = 0
    # game time
    var.gameTime = 3 * 60 # 3 minutes
    #-------------------------------------------------------------------



### ====================================================================================================
### UPDATE OF YOUR GAME DATA
### ====================================================================================================
def update(deltaTime):
    # -------------------------------------------------------------------

    # decrease gameTime
    if var.gameTime > 0:
        var.gameTime -= deltaTime
    else:
        var.gameTime = 0

    # decrease timeStep
    var.timeStep = ((var.gameTime * 2.0) / 180) + 1.5

    # INCREASE TIMER and create notes
    var.timer += deltaTime
    if var.gameTime > 0:
        if var.timer >= var.timeStep/var.nextTempo:
            var.timer = 0
            var.nextTempo = randint(1,4)
            # create gem in random direction (between 1 and 2 directions)
            nbNotes = randint(1,2)
            # create first note
            dir1 = randint(0,3)
            note = createSprite(NOTES[dir1],(50,50), True)
            nx = var.targets[dir1].center_x - (SCREEN_WIDTH/2)
            ny = var.targets[dir1].center_y - (SCREEN_HEIGHT/2)
            note.center_x = SCREEN_WIDTH/2 + 8*nx;
            note.center_y = SCREEN_HEIGHT/2 + 8*ny;
            note.angle = ANGLES[dir1]
            var.notes.append( [note,dir1] )
            # create second note if needed
            if nbNotes == 2:
                dir2 = randint(1, 2)
                if dir2 == 2:
                    dir2 = 3
                dir2 = (dir1 + dir2)%4
                note = createSprite(NOTES[dir2], (50, 50), True)
                nx = var.targets[dir2].center_x - (SCREEN_WIDTH / 2)
                ny = var.targets[dir2].center_y - (SCREEN_HEIGHT / 2)
                note.center_x = SCREEN_WIDTH / 2 + 8 * nx;
                note.center_y = SCREEN_HEIGHT / 2 + 8 * ny;
                note.angle = ANGLES[dir2]
                var.notes.append([note, dir2])

    # move notes
    for n in var.notes:
        n[0].center_x += deltaTime * 60 * 3 * DX[n[1]]
        n[0].center_y += deltaTime * 60 * 3 * DY[n[1]]

    # remove notes
    for n in var.notes:
        if abs(n[0].center_x-(SCREEN_WIDTH/2)) < 10 and abs(n[0].center_y-(SCREEN_HEIGHT/2)) < 10:
            var.notes.remove(n)
            var.nbHits += 1

    # press button events (SCALE)
    for i in range(len(var.buttons)):
        # if this is a small target
        if var.targets[i].scale == 0.25:
            if var.buttons[i]:
                var.targets[i].scale = 0.85
                var.buttons[i] = False
                var.nbHits += 1
                # check for closest note
                minDist = 1000000000
                closestNote = None
                for n in var.notes:
                    # check direction
                    if n[1] == i:
                        dx = n[0].center_x - var.targets[i].center_x
                        dy = n[0].center_y - var.targets[i].center_y
                        dx = dx*dx
                        dy = dy*dy
                        dist = math.sqrt(dx+dy)
                        if dist < minDist:
                            minDist = dist
                            closestNote = n
                if closestNote != None:
                    var.notes.remove(closestNote)
                    delta = 1.0*max(0, 100-abs(minDist))
                    var.cumul += delta
        elif var.targets[i].scale > 0.25:
            var.targets[i].scale -= 0.20
        else:
            var.targets[i].scale = 0.25



    #-------------------------------------------------------------------



### ====================================================================================================
### DRAW YOUR IMAGES ON THE SCREEN
### ====================================================================================================
def draw():
    #-------------------------------------------------------------------
    # draw BG
    var.bg.draw()
    arcade.draw_rectangle_filled(SCREEN_WIDTH/2,SCREEN_HEIGHT/2,SCREEN_WIDTH, SCREEN_HEIGHT, (0, 0, 0, 192))

    # draw circles
    for i in range(50,500,100):
        arcade.draw_circle_outline(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, i, (0,0,0,128), 1)
    # Draw targets
    for t in var.targets:
        t.draw()
    # Draw notes
    for n in var.notes:
        n[0].draw()
    # draw score
    if var.nbHits > 0:
        perc = round(var.cumul/var.nbHits,2)
        arcade.draw_text("SCORE = "+str(perc)+"%", SCREEN_WIDTH-25, SCREEN_HEIGHT-60, arcade.color.ORANGE, 30, anchor_x="right", anchor_y="top", bold=True    )
    # draw game time
    gt = round(var.gameTime, 1)
    arcade.draw_text("TIME = " + str(gt) +" sec.", SCREEN_WIDTH - 25, SCREEN_HEIGHT - 30, arcade.color.ORANGE, 30,anchor_x="right", anchor_y="top", bold=True)
    # Draw finish game
    if var.gameTime <= 0 and len(var.notes) == 0:
        arcade.draw_text("GAME OVER", SCREEN_WIDTH/2, SCREEN_HEIGHT/2, arcade.color.ORANGE, 100, anchor_x="center", anchor_y="center", bold=True)
    #-------------------------------------------------------------------



### ====================================================================================================
### FUNCTION CALLED WHEN YOU PRESS A KEY ON THE KEYBOARD
### ====================================================================================================
def onKeyEvent(key,isPressed):
    #-------------------------------------------------------------------
    if key == arcade.key.UP:
        var.buttons[0] = isPressed
    if key == arcade.key.RIGHT:
        var.buttons[1] = isPressed
    if key == arcade.key.DOWN:
        var.buttons[2] = isPressed
    if key == arcade.key.LEFT:
        var.buttons[3] = isPressed

    if key == arcade.key.ENTER and isPressed:
        # GENERATION
        var.timer = 0
        var.timeStep = 3.5
        var.nextTempo = randint(1, 4);
        # note list
        var.notes = []
        # buttons events
        var.buttons = [False, False, False, False]
        # score
        var.nbHits = 0
        var.cumul = 0
        # game time
        var.gameTime = 3 * 60  # 3 minutes
    #-------------------------------------------------------------------



### ====================================================================================================
### FUNCTION CALLED WHEN YOU PRESS A BUTTON ON A GAMEPAD CONTROLLER
### ====================================================================================================
def onButtonEvent(gamepadNum,buttonNum,isPressed):
    #-------------------------------------------------------------------
    if buttonNum == 3:
        var.buttons[0] = isPressed
    if buttonNum == 1:
        var.buttons[1] = isPressed
    if buttonNum == 0:
        var.buttons[2] = isPressed
    if buttonNum == 2:
        var.buttons[3] = isPressed
    #-------------------------------------------------------------------



### ====================================================================================================
### FUNCTION CALLED WHEN YOU MOVE AN AXIS ON A GAMEPAD CONTROLLER
### ====================================================================================================
def onAxisEvent(gamepadNum,axisName,analogValue):
    #-------------------------------------------------------------------
    pass
    #-------------------------------------------------------------------


