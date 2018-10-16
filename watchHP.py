from threading import Thread
from PIL import ImageGrab, Image
from time import sleep
import numpy as np
from colorsys import rgb_to_hsv
from useGUI import pressKey

class WatchHP(Thread):
    def __init__(self, offset):
        super(WatchHP, self).__init__()
        x1, y1 = offset["start"]
        x2, y2 = offset["end"]
        size_1 = offset["size_1"]
        self.HPArea = (x1 + size_1*3, y2, x1 + size_1*6, y2 + size_1)

    def run(self):
        while True:
            img = ImageGrab.grab(bbox=self.HPArea)

            average_color_per_row = np.average(img, axis=0)
            average_color = np.average(average_color_per_row, axis=0)
            average_color = np.uint8(average_color)
            # average_color_img = np.array([[average_color] * 500] * 500, np.uint8)
            # Image.fromarray(average_color_img).save('data/average_color_img2.png')
            # print(type(average_color))

            # Full HP [152  86  86]  -> Low HP [94 94 94]
            # (0.0, 0.43421052631578944, 0.596078431372549) -> (0.0, 0.0, 0.3686274509803922)
            average_hsv = rgb_to_hsv(average_color[0]/255, average_color[1]/255, average_color[2]/255)
            if (average_hsv[1] < 0.1) and (average_hsv[2] < 0.4):
                print("HP low", average_hsv)
                pressKey("1", interval=0)    # Use Azalea
            elif average_hsv[2] < 0.2:  # Lightness is lower than 0.2
                print("HP low", average_hsv)
                pressKey("1", interval=0)    # Use Azalea

            sleep(0.5)
