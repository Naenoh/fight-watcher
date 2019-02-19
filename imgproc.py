import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import time
from math import floor
import pytesseract
from difflib import get_close_matches

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

char_list = ["Hyde", "Linne", "Waldstein", "Carmine", "Orie", "Gordeau", "Merkava", "Vatista", "Seth", "Yuzuriha", "Hilda", "Eltnum", "Chaos", "Akatsuki", "Nanase", "Byakuya", "Phonon", "Mika", "Wagner", "Enkidu"]

def open_video(videopath):
    cap = cv.VideoCapture(videopath)
    framerate = cap.get(cv.CAP_PROP_FPS)
    frame_count = 0
    round_count = 0
    matches = []
    while(cap.isOpened()):
        frame = get_frame(cap)
        if frame is None:
            break
        if find_unist_roundstart(frame, round_count):
            # Here we're trying to verify its roundstart by checking if the white line in the middle is still there 5 frames after
            skip_frames(cap, frame_count, 5)
            frame = get_frame(cap)
            frame_count += 6
            if frame is None:
                break
            if find_unist_roundstart(frame, round_count) and find_unist_rounds(frame) == (0, 0):
                roundstart_frame = frame_count
                round_count += 1
                cv.imwrite(f"outputs/unist/{round_count}.jpg", frame)
                p1, p2 = extract_p1(frame), extract_p2(frame)
                cpt = 0
                # Trying to get the character name from subsequent frames up to a limit
                while((p1 == "" or p2 == "") and cpt < 50):
                    frame = get_frame(cap)
                    frame_count += 1
                    cpt += 1
                    if p1 == "":
                        p1 = extract_p1(frame)
                    if p2 == "":
                        p2 = extract_p2(frame)
                if cpt == 50:
                    if  p1 == "":
                        p1 = ask_manually(frame, "p1 : ")
                    if  p2 == "":
                        p2 = ask_manually(frame, "p2 : ")
                seconds = floor(roundstart_frame / framerate)
                matches.append([p1, p2, seconds])
                skip_frames(cap, frame_count, 600)
                frame_count += 600
        skip_frames(cap, frame_count, 24)
        frame_count += 25
    cap.release()
    cv.destroyAllWindows()
    return matches

def skip_frames(cap, current_frame, n):
     for i in range(n):
        cap.grab()

def get_frame(cap):
    ret, frame = cap.read()
    try:
        return cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    except cv.error:
        return None

def find_unist_roundstart(img, round_count):
    # 358-362 for 720p
    # 239-241 for 480p
    subimg = img[239:241, 0:852]
    roundstart = (subimg < 200).sum() < 100
    if not roundstart:
        return False
    p1line = img[64, 0:275]
    p2line = img[64, 577:852]
    fixed_ui = ((p1line < 150).sum() + (p2line < 150).sum()) < 150
    if not fixed_ui:
        return False
    p1rip = img[96:104, 69:72]
    p2rip = img[96:104, 716:719]
    p1name = img[71:89, 50:55]
    p2name = img[71:89, 798:803]
    humans = ((p1rip < 100).sum() + (p2rip < 100).sum()) < 20 and ((p1name > 150).sum() + (p2name > 150).sum()) < 30
    if not humans:
        cv.imwrite(f"outputs/unist/nothuman{round_count}.jpg", img)
        return False
    return True

def find_unist_rounds(img):
    #p1r1: 95:494 p1r2: 95:522, p2r2: 95:745, p2r1: 95:773
    p1 = 0
    if img[63, 329] > 60:
        p1 += 1
    p2 = 0
    if img[63, 515] > 60:
        p2 += 1
    return p1, p2

def find_orie(img, is_p1):
    if(img.shape[1] > 55):
        if is_p1:
            return (img[1:9, 16:26] < 190).sum() < 30
        else:    
            return (img[1:9, 45:55] < 190).sum() < 30
    return False

def extract_character(img, start, end, offset1, offset2, is_p1):
    line = img[60, start:end]
    whites = np.nonzero(line > 180)[0]
    minx = whites[0] - offset1 + start
    maxx = whites[-1] + offset2 + start
    charimg = img[54:64, minx:maxx]
    char = get_char(charimg)
    if char == "" and find_orie(charimg, is_p1):
        char = "Orie"
    return char
    
def get_char(img):
    read = pytesseract.image_to_string(img, config='--psm 9')
    matches = get_close_matches(read, char_list, 1)
    if(len(matches) == 0):
        return ""
    else:     
        return matches[0]

def extract_p1(img):
    return extract_character(img, 94, 190, 4, 6, True)

def extract_p2(img):
    return extract_character(img, 665, 760, 6, 6, False)

def ask_manually(img, msg):
    print(msg)
    plt.imshow(img,cmap = 'gray')
    plt.show()
    return get_close_matches(input(), char_list, 1)[0]
