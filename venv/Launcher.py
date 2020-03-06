### ====================================================================================================
### IMPORTS
### ====================================================================================================
import arcade
import random
import time
import StudentCode
from Utils import *


### ====================================================================================================
### CONSTANTS
### ====================================================================================================
TITLE = "Coding Factory Mini-Game !"



### ====================================================================================================
### GAME CLASS
### ====================================================================================================
class MyGame(arcade.Window):


    # ----------------------------------
    # PRIVATE METHODS FOR INPUT MANAGEMENT
    # ----------------------------------
    def __onButtonPressed(self, _gamepad, button):
        idx = self.gamepads[_gamepad]
        print("Button {}-{} pressed".format(idx, button))
        self.onButtonPressed(idx, button)
    def __onButtonReleased(self, _gamepad, button):
        idx = self.gamepads[_gamepad]
        print("Button {}-{} released".format(idx, button))
        self.onButtonReleased(idx, button)
    def __onCrossMove(self, _gamepad, x, y):
        idx = self.gamepads[_gamepad]
        print("Cross {}-({}-{})".format(idx, x, y))
        self.onCrossMove(idx, x, y)
    def __onAxisMove(self, _gamepad, axis, value):
        idx = self.gamepads[_gamepad]
        ## print("Axis {}-{}-{}".format(idx, axis, value))
        self.onAxisMove(idx, axis, value)


    # ----------------------------------
    # CONSTRUCTOR
    # ----------------------------------
    def __init__(self, width, height, title):
        #init application window
        super().__init__(width, height, title)
        # set application window background color
        arcade.set_background_color(arcade.color.BLACK)
        # Store gamepad list
        self.gamepads = arcade.get_joysticks()
        # check every connected gamepad
        if self.gamepads:
            for g in self.gamepads:
                #link all gamepad callbacks to the current class methods
                g.open()
                g.on_joybutton_press   = self.__onButtonPressed
                g.on_joybutton_release = self.__onButtonReleased
                g.on_joyhat_motion     = self.__onCrossMove
                g.on_joyaxis_motion    = self.__onAxisMove
            # transform list into a dictionary to get its index faster
            self.gamepads = { self.gamepads[idx]:idx for idx in range(len(self.gamepads)) }
        else:
            print("There are no Gamepad connected !")
            self.gamepads = None


    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    #                                SETUP your game here
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def setup(self):
        #- - - - - - - - - - - - - - - - - - - - - - - - -#
        StudentCode.setup()
        #- - - - - - - - - - - - - - - - - - - - - - - - -#


    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    #                               DRAW your game elements here
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def on_draw(self):
        #- - - - - - - - - - - - - - - - - - - - - - - - -#
        arcade.start_render()
        StudentCode.draw()
        #- - - - - - - - - - - - - - - - - - - - - - - - -#


    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    #                                  UPDATE your game model here
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def update(self, delta_time):
        #- - - - - - - - - - - - - - - - - - - - - - - - -#
        StudentCode.update(delta_time)
        #- - - - - - - - - - - - - - - - - - - - - - - - -#


    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # KEY PRESSED events
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def on_key_press(self, key, modifiers):
        #- - - - - - - - - - - - - - - - - - - - - - - - -#
        # Close application if ESCAPE key is hit
        if key == arcade.key.ESCAPE:
            self.close()
        StudentCode.onKeyEvent(key,True)
        #- - - - - - - - - - - - - - - - - - - - - - - - -#


    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # KEY RELEASED events
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def on_key_release(self, key, modifiers):
        #- - - - - - - - - - - - - - - - - - - - - - - - -#
        StudentCode.onKeyEvent(key,False)
        #- - - - - - - - - - - - - - - - - - - - - - - - -#


    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # GAMEPAD BUTTON PRESSED events
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def onButtonPressed(self, gamepadNum, buttonNum):
        #- - - - - - - - - - - - - - - - - - - - - - - - -#
        pass
        #- - - - - - - - - - - - - - - - - - - - - - - - -#


    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # GAMEPAD BUTTON RELEASED events
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def onButtonReleased(self, gamepadNum, buttonNum):
        #- - - - - - - - - - - - - - - - - - - - - - - - -#
        pass
        #- - - - - - - - - - - - - - - - - - - - - - - - -#


    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # GAMEPAD CROSSPAD events
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def onCrossMove(self, gamepadNum, xValue, yValue):
        #- - - - - - - - - - - - - - - - - - - - - - - - -#
        pass
        #- - - - - - - - - - - - - - - - - - - - - - - - -#


    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # GAMEPAD AXIS events
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def onAxisMove(self, gamepadNum, axisName, analogValue):
        #- - - - - - - - - - - - - - - - - - - - - - - - -#
        pass
        #- - - - - - - - - - - - - - - - - - - - - - - - -#






### ====================================================================================================
### MAIN PROCESS
### ====================================================================================================
def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()


