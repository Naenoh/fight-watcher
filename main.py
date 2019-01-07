
from imgproc import find_timer, open_video, find_timer_all_methods
import time

if __name__ == '__main__':
    start = time.time()
    open_video("inputs/video.webm")
    end = time.time()
    print(end - start)