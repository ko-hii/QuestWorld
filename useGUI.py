import pyautogui
from time import sleep
import ctypes


def getPosition():
    vk_leftbutton = 0x01  # Left-Click Virtual Keyboad
    vk_esc = 0x1B  # ESC Virtual Keyboad
    position = None

    while True:
        if ctypes.windll.user32.GetAsyncKeyState(vk_leftbutton) == 0x8000:
            position = pyautogui.position()
            break
        elif ctypes.windll.user32.GetAsyncKeyState(vk_esc) == 0x8000:
            break
    return position

def getScreen():
    print("Click Top-Left-Point to decide Monitoring Area : ", end="", flush=True)
    top_left = getPosition()
    print("OK") if top_left else print("Canceled")
    sleep(1)
    print("Click Bottom-Right-Point to decide Monitoring Area : ", end="", flush=True)
    bottom_right = getPosition()
    print("OK") if bottom_right else print("Canceled")

    if top_left and bottom_right:
        return top_left, bottom_right
    else:
        return False, False


def moveToPoint(point, offset):
    time_to_move = 0
    x, y = point
    size_1 = offset["size_1"]

    x = x * size_1 + offset["start"][0] + round(size_1 / 2)  # adding size_1/2 to focus on center
    y = y * size_1 + offset["start"][1] + round(size_1 / 2)

    pyautogui.moveTo(x, y, time_to_move)


def clickThePoint(point, offset):
    x, y = point
    size_1 = offset["size_1"]
    x = x*size_1 + offset["start"][0] + round(size_1/2)  # adding size_1/2 to focus on center
    y = y*size_1 + offset["start"][1] + round(size_1/2)

    # print("Move to ({}, {})".format(x, y))
    pyautogui.click(x=x, y=y, clicks=1, interval=0, button="left")


def clickTheArround(offset, time_to_kill):
    """"
        敵が右にいる場合 -> 1, 3回目で攻撃
        敵が左にいる場合 -> 2, 4回目で攻撃
        敵が下にいる場合 -> 右に移動すると敵は左に来るので2, 4回目で攻撃
        敵が上にいる場合 -> 右に移動して左に移動すると敵は右に来るので3回目で攻撃
    """
    size_1 = offset["size_1"]
    # right
    pyautogui.moveRel(xOffset=size_1, yOffset=0, duration=0)
    pyautogui.click(x=None, y=None, clicks=1, interval=0, button="left")
    sleep(time_to_kill/4)
    # left
    pyautogui.moveRel(xOffset=-size_1, yOffset=0, duration=0)
    pyautogui.click(x=None, y=None, clicks=1, interval=0, button="left")
    sleep(time_to_kill/4)
    # right
    pyautogui.moveRel(xOffset=size_1, yOffset=0, duration=0)
    pyautogui.click(x=None, y=None, clicks=1, interval=0, button="left")
    sleep(time_to_kill/4)
    # left
    pyautogui.moveRel(xOffset=-size_1, yOffset=0, duration=0)
    pyautogui.click(x=None, y=None, clicks=1, interval=0, button="left")


def pressKey(char, interval=0.0):
    pyautogui.typewrite(char, interval=interval)
