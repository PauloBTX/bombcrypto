from pyclick import HumanClicker
import pyautogui

hc = HumanClicker()
pyautogui.FAILSAFE = False

def moveTo(x,y):
    # initialize HumanClicker object
    x = int(x)
    y = int(y)

    # move the mouse to position (100,100) on the screen in approximately 2 seconds
    hc.move((x,y),1)

def mouseClick():
    # mouse click(left button)
    hc.click()

def ctrlF5():
    # Holds down the alt key
    pyautogui.keyDown("ctrl")
    # Presses the tab key once
    pyautogui.press("F5")
    # Lets go of the alt key
    pyautogui.keyUp("ctrl")
    pyautogui.keyUp("shift")

def ctrlShiftR():
    # Holds down the alt key
    pyautogui.keyDown("ctrl")
    pyautogui.keyDown("shift")
    # Presses the tab key once
    pyautogui.press("r")
    # Lets go of the alt key
    pyautogui.keyUp("ctrl")
    pyautogui.keyUp("shift")

def scrollTo(x,y,y2):
    moveTo(x,y)
    pyautogui.mouseDown(button="left")
    moveTo(x,y2)
    pyautogui.mouseUp(button="left")
    
def mouseMoveClick(x,y,w,h,cropX,cropY):
    center_x = x + int(w/2) + cropX
    center_y = y + int(h/2) + cropY
    moveTo(center_x,center_y)
    mouseClick()