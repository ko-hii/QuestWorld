import cv2
import os


def detectTarget(img, target_hist_dict, threshold_dict, size_1):
    candidate = dict()
    closest = dict()   # So close but it was not selected.

    for i in range(30):
        for j in range(14):
            x = i * size_1
            y = j * size_1
            dst_img = img[y:y+size_1, x:x+size_1]

            # compere by histogram
            result = dict()   # {"target": [ret, ret], "target": [ret]}
            hist = cv2.calcHist([dst_img], [0], None, [256], [0, 256])
            for target, target_hist_list in target_hist_dict.items():
                ret = [cv2.compareHist(target_hist, hist, 0) for target_hist in target_hist_list]
                result[target] = ret

                if max(ret) > threshold_dict[target]:
                    if target not in candidate:
                        candidate[target] = list()
                    candidate[target].append({"point": (i, j), "ret": ret})
                else:
                    # Update the closest target
                    if target in closest:
                        if closest[target][0] < max(ret):
                            closest[target] = (max(ret), (i, j))
                    else:
                        closest[target] = (max(ret), (i, j))
    return candidate, closest


def makeTargetHistDict(target_dict):
    """
    :param target_dict: {"target": [img, img,], "target2": [img, img,]}
    :return: {"Berger": [hist, hist], "Preta": [hist, hist]}
    """
    target_hist_dict = dict()

    for target, target_img_list in target_dict.items():
        for target_img in target_img_list:
            hist = cv2.calcHist([target_img], [0], None, [256], [0, 256])
            if target not in target_hist_dict:
                target_hist_dict[target] = list()
            target_hist_dict[target].append(hist)
    return target_hist_dict


def getTargetDict(target_path, target_list, size_1=32):
    target_img_dict = dict()
    lis = os.listdir(target_path)
    for li in lis:
        if li.endswith(".png"):
            key = li[0:li.find("_")]

            # skip when target-name not in target_list
            if key not in target_list:
                continue

            if key not in target_img_dict:
                target_img_dict[key] = list()
            img = cv2.imread(target_path + "/" + li)
            if size_1 > 32:
                img = cv2.resize(img, (size_1, size_1), interpolation=cv2.INTER_CUBIC)
            elif size_1 < 32:
                img = cv2.resize(img, (size_1, size_1), interpolation=cv2.INTER_AREA)
            target_img_dict[key].append(img)
    return target_img_dict


def cutTargetImage(img):
    for i in range(30):
        for j in range(14):
            x = i * 32
            y = j * 32
            dst_img = img[y:y + 32, x:x + 32]
            cv2.imwrite('data/temp/{}-{}.png'.format(i, j), dst_img)


def captureAndCut(file_name="TEMP"):
    from useGUI import getScreen
    from main import capture
    import numpy as np

    # Get screen area to capture
    print("----- Ready -----")
    start, end = getScreen()
    if start is False:
        print("Get Screen Error")
        return 0
    x = (end[0] - start[0]) / 30
    y = (end[1] - start[1]) / 14
    size_1 = round((x + y) / 2)
    print("Top-left: {}, Bottom-right: {}, Rect-size: {}".format(start, end, size_1))
    offset = {"start": start, "end": end, "size_1": size_1}

    # ScreenShots
    img = capture(offset)
    if not os.path.exists("data"):
        os.mkdir("data")
    img.save("data/{}.png".format(file_name))

    # cut target image
    # img = cv2.imread("data/detectionTest.png")
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    if not os.path.exists("data/temp"):
        os.mkdir("data/temp")
    cutTargetImage(img)


def detectionTest(place, img_path=None):
    import random
    from main import capture, getMonitoringScreenSize, calculateMyPosition
    import numpy as np
    from settings import settings

    dic = settings(place=place)
    threshold_dict = dic["threshold_dict"]
    target_list = dic["target_list"]
    time_to_kill = dic["time_to_kill"]
    move_another_area = dic["move_another_area"]
    target_img_path = dic["target_img_path"]
    area_dict = dic["area_dict"]
    x_max, x_min, y_max, y_min = (dic["x_max"], dic["x_min"], dic["y_max"], dic["y_min"])

    if img_path is not None:
        img = cv2.imread(img_path)
        if len(img.shape) == 3:
            height, width, channels = img.shape[:3]
        else:
            height, width = img.shape[:2]
            channels = 1
        x =  width / 30
        y = height / 14
        size_1 = round((x + y) / 2)
        offset = {"start": (0,0), "end": (width, height), "size_1": size_1}
    else:
        # Get screen to monitor
        print("----- Ready -----")
        offset = getMonitoringScreenSize()

    if offset is False:
        print("Get Screen Error")
        return False
    else:
        print("Top-left: {}, Bottom-right: {}, Rect-size: {}".format(offset["start"], offset["end"], offset["size_1"]))

    target_img_dict = getTargetDict(target_img_path, target_list, offset["size_1"])
    target_hist_dict = makeTargetHistDict(target_img_dict)

    if img_path is None:
        img = capture(offset)
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    candidate, closest = detectTarget(img, target_hist_dict, threshold_dict, offset["size_1"])

    # set my position
    my_position = calculateMyPosition(candidate, test=True)
    print("My position is {}".format(my_position))

    for target in target_list:
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        if target in candidate:
            # move to point which is the nearest me
            candy_list = candidate[target]
            candy_list = sorted(candy_list, key=lambda c: np.linalg.norm(my_position - c["point"]))
            print([can["point"] for can in candy_list])

            for candy in candy_list:
                x, y = candy["point"]
                x = x * offset["size_1"]
                y = y * offset["size_1"]
                print("\tGet {} at {} : {}".format(target, candy["point"], candy["ret"]))
                cv2.rectangle(img, (x, y), (x + offset["size_1"], y + offset["size_1"]), (b, g, r), thickness=3)

    print("Closest : {}".format(closest))
    cv2.imshow("detectionTest", img)
    print("Press any key to exit")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite("data/detectionTest.png", img)


def main():
    # capture and cut to 30*14 squares
    #captureAndCut(file_name="base")

    # Test
    # img_path = "data/forest.png"
    img_path = None
    detectionTest(place="iceCastle", img_path=img_path)


if __name__ == '__main__':
    main()
