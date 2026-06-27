import yt_dlp


def baixar_clip(url):

    ydl_opts = {

        "outtmpl": "../downloads/%(title)s.%(ext)s"

    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        ydl.download([url])