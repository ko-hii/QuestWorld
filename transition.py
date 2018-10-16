import time
from useGUI import getPosition
from collections import deque
from main import getMonitoringScreenSize, calPointFromPic


def recordTransition():
    transition = list()
    transition_time = deque()

    offset = getMonitoringScreenSize()
    if offset is False:
        print("Get Screen Error")
        return False
    else:
        print("Top-left: {}, Bottom-right: {}, Rect-size: {}".format(offset["start"], offset["end"], offset["size_1"]))

    time.sleep(2)
    pre_time = time.time()
    while True:
        print("Click Point to move Area (Cancel:[ESC]): ", end="", flush=True)
        position = getPosition()

        now = time.time()
        transition_time.append(int(now - pre_time)+1)
        pre_time = now

        if position is None:
            print("Canceled")
            break
        else:
            point = calPointFromPic(offset, position)
            transition.append(point)
            print("Append {}".format(point))
        time.sleep(0.5)
    transition_time.popleft()

    print("Copy And Paste data below, to settings.py")
    print("transition = {}".format(transition))
    print("transition_time = {}".format(list(transition_time)))


if __name__ == '__main__':
    recordTransition()