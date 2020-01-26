### ====================================================================================================
### IMPORTS
### ====================================================================================================
import arcade
import random



### ====================================================================================================
### CONSTANTS
### ====================================================================================================
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TITLE = "My supa game in Python !"



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
        self.circleX = SCREEN_WIDTH  / 2
        self.circleY = SCREEN_HEIGHT / 2
        self.radius  = 75
        self.move = 0
        #- - - - - - - - - - - - - - - - - - - - - - - - -#


    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    #                               DRAW your game elements here
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def on_draw(self):
        #- - - - - - - - - - - - - - - - - - - - - - - - -#
        arcade.start_render()
        arcade.draw_circle_filled(self.circleX, self.circleY, self.radius, arcade.color.BLUE)
        #- - - - - - - - - - - - - - - - - - - - - - - - -#


    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    #                                  UPDATE your game model here
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def update(self, delta_time):
        #- - - - - - - - - - - - - - - - - - - - - - - - -#
        # update position and radius according to move variable
        if self.move & 1 != 0:
            self.circleY += 5
        if self.move & 2 != 0:
            self.circleY -= 5
        if self.move & 4 != 0:
            self.circleX -= 5
        if self.move & 8 != 0:
            self.circleX += 5
        if self.move & 16 != 0:
            self.radius += 5
        if self.move & 32 != 0:
            self.radius -= 5
        #- - - - - - - - - - - - - - - - - - - - - - - - -#


    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # KEY PRESSED events
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def on_key_press(self, key, modifiers):
        #- - - - - - - - - - - - - - - - - - - - - - - - -#
        # Close application if ESCAPE key is hit
        if key == arcade.key.ESCAPE:
            self.close()

        # Store movement according to key press
        if key == arcade.key.UP:
            self.move |= 1
        if key == arcade.key.DOWN:
            self.move |= 2
        if key == arcade.key.LEFT:
            self.move |= 4
        if key == arcade.key.RIGHT:
            self.move |= 8
        if key == arcade.key.P:
            self.move |= 16
        if key == arcade.key.M:
            self.move |= 32
        #- - - - - - - - - - - - - - - - - - - - - - - - -#


    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # KEY RELEASED events
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def on_key_release(self, key, modifiers):
        #- - - - - - - - - - - - - - - - - - - - - - - - -#
        # Store movement according to key release
        if key == arcade.key.UP:
            self.move &=  ~1
        if key == arcade.key.DOWN:
            self.move &=  ~2
        if key == arcade.key.LEFT:
            self.move &=  ~4
        if key == arcade.key.RIGHT:
            self.move &=  ~8
        if key == arcade.key.P:
            self.move &=  ~16
        if key == arcade.key.M:
            self.move &=  ~32
        #- - - - - - - - - - - - - - - - - - - - - - - - -#


    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # GAMEPAD BUTTON PRESSED events
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def onButtonPressed(self, gamepadNum, buttonNum):
        #- - - - - - - - - - - - - - - - - - - - - - - - -#
        if buttonNum == 0:
            self.move |= 16
        if buttonNum == 1:
            self.move |= 32
        #- - - - - - - - - - - - - - - - - - - - - - - - -#


    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # GAMEPAD BUTTON RELEASED events
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def onButtonReleased(self, gamepadNum, buttonNum):
        #- - - - - - - - - - - - - - - - - - - - - - - - -#
        if buttonNum == 0:
            self.move &= ~16
        if buttonNum == 1:
            self.move &= ~32
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
        if axisName == 'x':
            d = (SCREEN_WIDTH / 2)
            self.circleX = d + d*analogValue
        if axisName == 'y':
            d = (SCREEN_HEIGHT / 2)
            self.circleY = d - d*analogValue
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


