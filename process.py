### ====================================================================================================
### IMPORTS
### ====================================================================================================
import arcade
from utils import *



class Process:

    ### ====================================================================================================
    ### PARAMETERS
    ### ====================================================================================================
    SCREEN_WIDTH  = 1200
    SCREEN_HEIGHT = 675

    

    ### ====================================================================================================
    ### CONSTRUCTOR
    ### ====================================================================================================
    def __init__(self):
        pass

        

    ### ====================================================================================================
    ### INIT
    ### ====================================================================================================
    def setup(self):
        pass



    ### ====================================================================================================
    ### UPDATE
    ### ====================================================================================================
    def update(self,deltaTime):
        pass

        

    ### ====================================================================================================
    ### RENDERING
    ### ====================================================================================================
    def draw(self):
        message  = "INSTALL OK" + "\n"
        message += "- Press any key from keyboard" + "\n"
        message += "- Press any button from controllers" + "\n"
        message += "- Move any stick from controllers" + "\n"
        message += "- Press any button from mouse" + "\n"
        message += "- Move the mouse in any direction" + "\n"
        message += "==> See information on the output console" + "\n"

        paramTxt = {"x": self.SCREEN_WIDTH//2,
                    "y": self.SCREEN_HEIGHT//2,
                    "alignH": "center",
                    "alignV": "center",
                    "message": message,
                    "size": 50,
                    "color": (160, 255, 160, 255),
                    }
        drawText(paramTxt)



    ### ====================================================================================================
    ### KEYBOARD EVENTS
    ### key is taken from : arcade.key.xxx
    ### ====================================================================================================
    def onKeyEvent(self,key,isPressed):
        print(f"key={key} - isPressed={isPressed}")
        


    ### ====================================================================================================
    ### GAMEPAD BUTTON EVENTS
    ### buttonName can be "A", "B", "X", "Y", "LB", "RB", "VIEW", "MENU", "LSTICK", "RSTICK"
    ### ====================================================================================================
    def onButtonEvent(self, gamepadNum,buttonName,isPressed):
        print(f"GamePad={gamepadNum} - ButtonNum={buttonName} - isPressed={isPressed}")
        


    ### ====================================================================================================
    ### GAMEPAD AXIS EVENTS
    ### axisName can be "X", "Y", "RX", "RY", "Z"
    ### ====================================================================================================
    def onAxisEvent(self, gamepadNum,axisName,analogValue):
        print(f"GamePad={gamepadNum} - AxisName={axisName} - Value={analogValue}")
        


    ### ====================================================================================================
    ### MOUSE MOTION EVENTS
    ### ====================================================================================================
    def onMouseMotionEvent(self,x,y,dx,dy):
        print(f"MOUSE MOTION : x={x}/y={y} dx={dx}/dy={dy}")



    ### ====================================================================================================
    ### MOUSE BUTTON EVENTS
    ### ====================================================================================================
    def onMouseButtonEvent(self,x,y,buttonNum,isPressed):
        print(f"MOUSE BUTTON : x={x}/y={y} buttonNum={buttonNum} isPressed={isPressed}")


