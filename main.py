
from imgproc import open_video
import time
import cv2 as cv
import sys
from videodl import download_video

def matches_to_sql(outputname, matches, url, date):
    with open(outputname, 'w') as output:
        output.write("INSERT INTO unisttv.matches (playerone, playertwo, link, upload_date) values \n")
        lines = []
        for (p1, p2, seconds) in matches:
            minutes, seconds = divmod(seconds, 60)
            hours, minutes = divmod(minutes, 60)
            lines.append(f"('{p1}','{p2}','{url}&t={hours}h{minutes}m{seconds}s', '{date}')")
        output.write(",\n".join(lines))
        output.write(";")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage : python main.py <yt link to video>")
        exit()
    start = time.time()
    folder = 'inputs/unist/'
    url, upload_date = download_video(sys.argv[1], folder)
    formatted_date = f'{upload_date[0:4]}-{upload_date[4:6]}-{upload_date[6:8]}'
    matches = open_video(folder + upload_date + '.mp4')
    matches_to_sql(f'outputs/unist/{formatted_date}.sql', matches, url, formatted_date)
    end = time.time()
    print("Processing took : " + str(end - start) + "s")
    