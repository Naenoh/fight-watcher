# itags: 135 for 480p mp4 video, 242 for 408 webm video

import youtube_dl

def download_video(url, folder):
    ydl_opts = {
        'format': 'mp4[height=480]',
        'outtmpl': folder + '%(upload_date)s.mp4'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        infos = ydl.extract_info(url, download=True) # This also downloads the video
        return infos['webpage_url'], infos['upload_date']