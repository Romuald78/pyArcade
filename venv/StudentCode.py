### ====================================================================================================
### IMPORTS
### ====================================================================================================
import arcade
from Utils import *
from random import *
import time
var = Variables()






def setup():
    print("setup")

    # BACKGROUND
    arcade.set_background_color(arcade.color.BLUE)
    var.bg = createSprite(f":resources:images/backgrounds/abstract_1.jpg",(SCREEN_WIDTH,SCREEN_HEIGHT),True)
    var.bg.center_x = SCREEN_WIDTH / 2
    var.bg.center_y = SCREEN_HEIGHT / 2

    # ROBOT SPRITE
    var.robot = createSprite(f":resources:images/animated_characters/robot/robot_idle.png",(200,200))

    # robot position
    var.robot.center_x = 100
    var.robot.center_y = 100

    # movement
    var.moveLeft  = False
    var.moveRight = False

    # ONE FRUIT
    var.fruits = []


    var.life = 3
    var.stars = []
    for i in range(var.life):
        star = createSprite(f":resources:images/items/star.png",(100,100))
        star.center_y = SCREEN_HEIGHT - 50;
        star.center_x = 50 + 75 * i
        var.stars.append(star)

    var.time = 0




def update(deltaTime):
    var.time += deltaTime

    if var.life > 0:

        if var.moveLeft:
            var.robot.center_x -= 7;
        if var.moveRight:
            var.robot.center_x += 7;

        if var.robot.center_x < 0:
            var.robot.center_x = 0

        if var.robot.center_x > SCREEN_WIDTH:
            var.robot.center_x = SCREEN_WIDTH



        if var.time >= 1:
            var.time -= 1
            fruit = createSprite(f":resources:images/items/gemYellow.png",(75,75));
            fruit.center_x = randint(0,SCREEN_WIDTH)
            fruit.center_y = SCREEN_HEIGHT+100
            var.fruits.append( fruit )





    for f in var.fruits:
        f.center_y -= 5

        if f.center_y < 100:
            if abs( var.robot.center_x - f.center_x) < 50:
                var.fruits.remove(f)

        if f.center_y < 0:
            var.fruits.remove(f)
            var.life -= 1


def draw():
    var.bg.draw()

    var.robot.draw()

    for i in range(var.life):
        var.stars[i].draw()

    for f in var.fruits:
        f.draw()


def onKeyEvent(key,isPressed):
    if key == arcade.key.LEFT:
        var.moveLeft = isPressed
    if key == arcade.key.RIGHT:
        var.moveRight = isPressed

    if key == arcade.key.ENTER:
        var.life = 3
        var.fruits = []
