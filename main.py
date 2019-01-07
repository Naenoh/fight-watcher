
from imgproc import find_timer, open_video, find_timer_all_methods
import time
import cv2 as cv
from videodl import download_video

if __name__ == '__main__':
    p1 = ["inputs/xrdp1r0.png", "inputs/xrdp1r1.png", "inputs/xrdp1r2.png"]
    p2 = ["inputs/xrdp2r0.png", "inputs/xrdp2r1.png", "inputs/xrdp2r2.png"]
    inputs = ["inputs/00.jpg", "inputs/01.jpg", "inputs/12.jpg", "inputs/20.jpg"]
    start = time.time()
    for inp in inputs:
        print("----------" + inp)
        img = cv.imread(inp, 0)
        print("P1", end = " ")
        for score in p1:
            template = cv.imread(score, 0)
            print(find_timer(img, template), end=" ")
        print("\nP2", end = " ")
        for score in p2:
            template = cv.imread(score, 0)
            print(find_timer(img, template), end=" ")
        print()
    end = time.time()
    print(end - start)