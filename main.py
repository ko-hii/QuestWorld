from PIL import ImageGrab
from time import sleep
import cv2
from detect import detectTarget, getTargetDict, makeTargetHistDict
from useGUI import clickThePoint, clickTheArround, getScreen, moveToPoint
import numpy as np
from collections import deque
from watchHP import WatchHP
from settings import settings


def calPointFromPic(offset, position):
    top_x, top_y = offset["start"]
    pos_x, pos_y = position

    x = int((pos_x - top_x) / offset["size_1"])
    y = int((pos_y - top_y) / offset["size_1"])
    return tuple((x, y))


def getMonitoringScreenSize():
    start, end = getScreen()
    if start is False:
        return False
    x = (end[0] - start[0]) / 30
    y = (end[1] - start[1]) / 14
    size_1 = round((x + y) / 2)
    offset = {"start": start, "end": end, "size_1": size_1}  # if 1960*1080 then 32 * 32
    return offset


def capture(offset=None):
    if offset is None:
        offset = {"start": (480, 112), "end": (1440, 560), "size_1": 32}

    x1, y1 = offset["start"]
    x2, y2 = offset["end"]
    img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    return img


def calMyPoint(candidate, test=False):
    if "Me" in candidate:
        me = sorted(candidate["Me"], key=lambda x: max(x["ret"]))[0]
        my_x, my_y = me["point"]
    elif "MyHead" in candidate:
        me = sorted(candidate["MyHead"], key=lambda x: max(x["ret"]))[0]
        my_x, my_y = me["point"]
        my_y += 1
    else:
        my_x, my_y = (15, 7)  # if cannot find me
    my_point = np.array([my_x, my_y])

    if test is False:
        if "Me" in candidate:
            del candidate["Me"]
        if "MyHead" in candidate:
            del candidate["MyHead"]
    return my_point


def canClickPoint(point, range_):
    x_min, x_max, y_min, y_max = range_
    if (x_min <= point[0] <= x_max) and (y_min <= point[1] <= y_max):
        return True
    else:
        return False

def automaticFarm():
    click_history = deque()   # History of click point for the past 3 times
    place = "iceCastle"

    dic = settings(place=place)
    threshold_dict = dic["threshold_dict"]
    target_list = dic["target_list"]
    time_to_kill = dic["time_to_kill"]
    move_another_area = dic["move_another_area"]
    target_img_path = dic["target_img_path"]
    area_dict = dic["area_dict"]
    click_range_ = dic["range"]
    x_min, x_max, y_min, y_max = click_range_
    transition = dic["transition"]
    transition_time = dic["transition_time"]


    # Get screen to monitor
    print("----- Ready -----")
    offset = getMonitoringScreenSize()
    if offset is False:
        print("Get Screen Error")
        return False
    else:
        print("Top-left: {}, Bottom-right: {}, Rect-size: {}".format(offset["start"], offset["end"], offset["size_1"]))

    # Get target histogram
    target_img_dict = getTargetDict(target_img_path, target_list, offset["size_1"])
    target_hist_dict = makeTargetHistDict(target_img_dict)

    # start thread to monitoring HP
    # t = WatchHP(offset=offset)
    # t.daemon = True
    # t.start()

    # Move to Farming Area
    print("Move to Farming Area : ", end="", flush=True)
    for point, interval in zip(transition, transition_time):
        clickThePoint(point, offset)
        sleep(interval)
    print("Has Arrived")

    # main loop
    print("--- Start ---")
    while True:
        moveToPoint(point=(0,0), offset=offset)

        # ScreenShots
        img = capture(offset)
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        candidate, closest = detectTarget(img, target_hist_dict, threshold_dict, offset["size_1"])
        for i, v in candidate.items():
            print(i, [(t["point"], max(t["ret"])) for t in v])

        # set my position
        my_point = calMyPoint(candidate)
        print("My point is {}".format(my_point))

        move_flag = False
        point = None
        if candidate:  # if detect characters without me
            for target in target_list:
                if target in candidate:
                    # move to target-point which is the nearest me
                    candy_list = candidate[target]
                    candy_list = sorted(candy_list, key=lambda c: np.linalg.norm(my_point - c["point"]))
                    print("Near me : {}".format([can["point"] for can in candy_list]))
                    for candy in candy_list:
                        point = candy["point"]
                        # if
                        if (len(set(click_history)) == 1) and (click_history[0] == point):
                            print("\tClick the same point {} 5 times".format(point))
                            moveToPoint(point=point, offset=offset)
                            clickTheArround(offset, 1)
                            continue
                        # if target is in can-attack area, click the point
                        if canClickPoint(point, range_=click_range_):
                            print("\tGet {} at {} : {}".format(target, candy["point"], max(candy["ret"])))
                            print("\tClosest {}".format(closest))
                            clickThePoint(point=point, offset=offset)
                            if (target == "Berger") or (target == "Item"):
                                sleep(3)
                            else:
                                sleep(time_to_kill)
                            move_flag = True
                            break
                        elif move_another_area is False:
                            if point[0] < x_min:
                                point = (point[0]+2, point[1])
                            if point[0] > x_max:
                                point = (point[0]-2, point[1])
                            if point[1] < y_min:
                                point = (point[0], point[1]+2)
                            if point[1] > y_max:
                                point = (point[0], point[1]-2)
                            print("\t{} is not in can-attack area so move to {}".format(target, point))
                            clickThePoint(point=point, offset=offset)
                            sleep(1.5)
                            move_flag = True
                            break
                if move_flag:
                    click_history.append(point)
                    if len(click_history) > 3:
                        click_history.popleft()
                    break
        if move_flag is False:
            print("No-candidate : {} is closest.".format(closest))
            if move_another_area:
                print("\tMove Area -> {}".format(area_dict["next_area"]))
                next_area = area_dict["next_area"]
                clickThePoint(point=area_dict["area" + next_area], offset=offset)
                sleep(time_to_kill/2)
                area_dict["next_area"] = str(int(next_area) % 2 + 1)
            else:
                if click_history:
                    moveToPoint(click_history[-1], offset)
                    sleep(0.1)
                    clickTheArround(offset, 4)
                else:
                    sleep(2)


if __name__ == '__main__':
    automaticFarm()
