from pytube import YouTube


def download_video(url):
    yt = YouTube(url)
    yt.streams.filter(adaptive=True, only_video=True, resolution="480p", video_codec="vp9").first().download(filename="video")