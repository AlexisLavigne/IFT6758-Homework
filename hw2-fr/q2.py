import ffmpeg
import pandas as pd
import numpy as np
import csv
import threading
from tqdm import tqdm
from os.path import exists
import os
import yt_dlp as youtube_dl


def download_audio(YTID: str, path: str) -> None:
    """
    Créez une fonction qui télécharge l'audio de la vidéo Youtube avec un identifiant donné
    et l'enregistre dans le dossier donné par `path`. Téléchargez-le en mp3. S'il y a un problème lors du téléchargement du fichier, gérez l'exception. Si il y a déjà un fichier à `path`, la fonction devrait retourner sans tenter de le télécharger à nouveau.

    ** Utilisez la librairie youtube_dl : https://github.com/ytdl-org/youtube-dl/ **
    
    Arguments :
    - YTID : Contient l'identifiant youtube, la vidéo youtube correspondante peut être trouvée sur
    'https://www.youtube.com/watch?v='+YTID
    - path : Le chemin d'accès au fichier où l'audio sera enregistré
    """
    url_prefix = "https://www.youtube.com/watch?v="
    video_url = url_prefix + YTID

    target_file = f"{path}/{YTID}.mp3"

    if exists(target_file):
        print(f"File already exists at: {target_file}")
        return

    def my_hook(d):
        if d['status'] == 'finished':
            print('Done downloading, now converting ...')

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(path, f"{YTID}.%(ext)s"),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'progress_hooks': [my_hook],
        'verbose': False,
        'source_address': '0.0.0.0',
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/114.0.0.0 Safari/537.36'
        },
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
    except Exception:
        raise


def cut_audio(in_path: str, out_path: str, start: float, end: float) -> None:
    """
    Créez une fonction qui coupe l'audio de in_path pour n'inclure que le segment de start à end et l'enregistre dans out_path.

    ** Utilisez la bibliothèque ffmpeg : https://github.com/kkroening/ffmpeg-python
    Arguments :
    - in_path : Chemin du fichier audio à couper
    - out_path : Chemin du fichier pour enregistrer l'audio coupé
    - start : Indique le début de la séquence (en secondes)
    - end : Indique la fin de la séquence (en secondes)
    """
    if exists(out_path):
        print(f"File already exists at: {out_path}")
        return
    try:
        in_mp3 = ffmpeg.input(in_path, ss=start, to=end)
        out = ffmpeg.output(in_mp3, out_path)
        out.run(overwrite_output=True)
    except ffmpeg.Error:
        raise
