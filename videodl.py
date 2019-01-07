# Shamelessly stolen from https://github.com/nficano/pytube/issues/180#issuecomment-363529167

import multiprocessing as mp
from math import ceil

import requests
from pytube import YouTube

CHUNK_SIZE = 3 * 2**20  # bytes

def download_video(video_url, itag, filename):
    stream = YouTube(video_url).streams.get_by_itag(itag)
    url = stream.url
    filesize = stream.filesize

    ranges = [[url, i * CHUNK_SIZE, (i+1) * CHUNK_SIZE - 1] for i in range(ceil(filesize / CHUNK_SIZE))]
    ranges[-1][2] = None  # Last range must be to the end of file, so it will be marked as None.

    pool = mp.Pool(min(len(ranges), 64))
    chunks = pool.map(download_chunk, ranges)

    with open(filename, 'wb') as outfile:
        for chunk in chunks:
            outfile.write(chunk)


def download_chunk(args):
    url, start, finish = args
    range_string = '{}-'.format(start)

    if finish is not None:
        range_string += str(finish)

    response = requests.get(url, headers={'Range': 'bytes=' + range_string})
    return response.content