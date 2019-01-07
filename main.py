
from imgproc import find_timer, open_video, find_timer_all_methods
import time
import cv2 as cv
from videodl import download_video

if __name__ == '__main__':
    start = time.time()
    download_video("https://www.youtube.com/watch?v=DEGFrabMxLY", 135, "inputs/video.mp4") # 135
    open_video("inputs/video.mp4")
    end = time.time()
    print(end - start)