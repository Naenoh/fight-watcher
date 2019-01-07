import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import time

def open_video(videopath):
    cap = cv.VideoCapture(videopath)
    template = cv.imread("inputs/xrdTemplate.png", 0)
    frame_count = 0
    round_count = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        try:
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        except cv.error:
            break
        if find_timer(gray, template) > 0.94:
            round_count += 1
            cv.imwrite("outputs/ress" + str(round_count) + ".jpg", gray)
            skip_frames(cap, frame_count, 600)
            frame_count += 600
        skip_frames(cap, frame_count, 26)
        frame_count += 27
    cap.release()
    cv.destroyAllWindows()

def skip_frames(cap, current_frame, n):
     for i in range(0, n):
        cap.grab()

def find_timer(img, template):
    # Apply template Matching
    res = cv.matchTemplate(img,template,cv.TM_CCORR_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    return max_val

def find_timer_all_methods(imgpath, templatepath):
    template = cv.imread(templatepath,0)
    w, h = template.shape[::-1]
    # All the 6 methods for comparison in a list
    #methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED','cv.TM_CCORR',
    #            'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
    methods = ['cv.TM_CCORR_NORMED']
    img = cv.imread(imgpath,0)
    img2 = img.copy()
    for meth in methods:
        start = time.time()
        img = img2.copy()
        method = eval(meth)
        # Apply template Matching
        res = cv.matchTemplate(img,template,method)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        end = time.time()
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
            res = min_val
            top_left = min_loc
        else:
            res = max_val
            top_left = max_loc
        print(meth, res, end - start)
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv.rectangle(img,top_left, bottom_right, 255, 4)
        plt.imshow(img,cmap = 'gray')
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        plt.suptitle(meth)
        plt.show()