### ====================================================================================================
### IMPORTS
### ====================================================================================================
import arcade
import random
import time



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

        #init SPRITES
        self.robot = {"idle":None, "walk":None}

        # Add IDLE
        filepath = f":resources:images/animated_characters/robot/robot_idle.png"
        self.robot["idle"] = arcade.AnimatedTimeSprite()
        self.robot["idle"].textures = []
        self.robot["idle"].textures.append(arcade.load_texture(filepath))

        # Add WALK
        self.robot["walk"] = {"left":arcade.AnimatedTimeSprite(),"right":arcade.AnimatedTimeSprite()}
        self.robot["walk"]["left"].textures  = []
        self.robot["walk"]["right"].textures = []
        for i in range(8):
            filepath = f":resources:images/animated_characters/robot/robot_walk{i}.png"
            self.robot["walk"]["left"].textures.append(  arcade.load_texture(filepath, mirrored=True) )
            self.robot["walk"]["right"].textures.append( arcade.load_texture(filepath) )

        # select current sprite
        self.currentSprite = self.robot["idle"]

        # Load box sprites
        bSize = 75
        self.boxes = []
        for i in range(10):
            xb = random.random() * SCREEN_WIDTH
            yb = random.random() * SCREEN_HEIGHT
            self.boxes.append( arcade.AnimatedTimeSprite() )
            self.boxes[i].textures = []
            filepath = f":resources:images/tiles/boxCrate_double.png"
            self.boxes[i].textures.append( arcade.load_texture(filepath) )
            self.boxes[i].set_position(int(xb),int(yb))
            self.boxes[i].set_points([[-bSize,-bSize],[bSize,-bSize],[bSize,bSize],[-bSize,bSize]])
            self.boxes[i].update_animation(0)
            self.boxes[i].scale = 0.5

        self.emit = arcade.Emitter(
            center_xy        = (SCREEN_HEIGHT/2, SCREEN_WIDTH/2),
            emit_controller  = arcade.EmitMaintainCount(400),
            particle_factory = lambda emitter: arcade.FadeParticle(
                filename_or_texture = arcade.make_circle_texture(30, arcade.color.WHITE),
                change_xy           = arcade.rand_in_circle((0.0, 0.0), random.uniform(0.5,0.6)),
                lifetime            = random.uniform(0.1, 5.0),
                scale = 0.1,
                start_alpha=100,
                end_alpha=0,
            ),
        )

        #- - - - - - - - - - - - - - - - - - - - - - - - -#


    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    #                               DRAW your game elements here
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def on_draw(self):
        #- - - - - - - - - - - - - - - - - - - - - - - - -#
        arcade.start_render()

        # draw boxes
        for b in self.boxes:
            b.draw()

        # draw robot
        self.currentSprite.draw()



        self.emit.draw()
        #- - - - - - - - - - - - - - - - - - - - - - - - -#


    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    #                                  UPDATE your game model here
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def update(self, delta_time):
        #- - - - - - - - - - - - - - - - - - - - - - - - -#
        # update position and radius according to move variable
        movX = 0
        movY = 0
        if self.move & 1 != 0:
            movY += 5
        if self.move & 2 != 0:
            movY -= 5
        if self.move & 4 != 0:
            movX -= 5
        if self.move & 8 != 0:
            movX += 5

        # Check if robot is in collision with any box
        curX = self.circleX
        curY = self.circleY
        nxtX = self.circleX + movX
        nxtY = self.circleY + movY
        for b in self.boxes:
            pts = b.get_points()
            minX = pts[0][0]
            maxX = pts[2][0]
            minY = pts[0][1]
            maxY = pts[2][1]
            if nxtX >= minX and nxtX <= maxX and nxtY >= minY and nxtY <= maxY :
                # check if we push HORIZONTALLY
                if curY >= minY and curY <=maxY:
                    if curX < minX:
                        b.center_x = b.center_x + 5
                    elif curX > maxX:
                        b.center_x = b.center_x - 5
                # push VERTICALLY
                if curX >= minX and curX <=maxX:
                    if curY < minY:
                        b.center_y = b.center_y + 5
                    elif curY > maxY:
                        b.center_y = b.center_y - 5

        # update position
        self.circleX += movX
        self.circleY += movY

        # block robot position to the screen borders
        if self.circleX < 0:
            self.circleX = 0;
        if self.circleX > SCREEN_WIDTH:
            self.circleX = SCREEN_WIDTH;
        if self.circleY < 0:
            self.circleY = 0;
        if self.circleY > SCREEN_HEIGHT:
            self.circleY = SCREEN_HEIGHT;

        # Select robot animation
        self.currentSprite = self.robot["idle"]
        if self.move != 0:
            i = int(time.time() * 1000 / 100) % 8;
            dir = "right"
            if (self.move & 4) == 4:
                dir = "left"
            self.currentSprite = self.robot["walk"][dir]

        # update animation and position of the robot
        self.currentSprite.update_animation(delta_time)
        self.currentSprite.set_position(self.circleX,self.circleY+60)


        self.emit.center_x = self.circleX
        self.emit.center_y = self.circleY + self.currentSprite.height*0.5
        self.emit.update()

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
        if axisName == 'x':
            if analogValue >= 0.5:
                self.move |= 8
            elif analogValue <= -0.5:
                self.move |= 4
            else:
                self.move &= ~12
        if axisName == 'y':
            if analogValue >= 0.5:
                self.move |= 2
            elif analogValue <= -0.5:
                self.move |= 1
            else:
                self.move &= ~3
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


