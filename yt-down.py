#first, install yt-dl: pip install yt-dlp
import yt_dlp
from tkinter import Tk, filedialog

#ask the user for the YouTube URL
url = input("URL do YouTube: ")

#Perguntar a pasta onde o vídeo ou áudio será salvo
root = Tk()
root.withdraw()

#Confirmar a pasta selecionada pelo usuário
while True:

    folder = filedialog.askdirectory()

    if not folder:

        print("Nenhuma pasta selecionada.")
        continue

    print(f"\nPasta selecionada:\n{folder}\n")

    confirmar = input("Usar esta pasta? (s/n): ").lower()

    if confirmar == "s":
        break

#Pergunta ao usuário qual formato ele deseja baixar
print("""
1 - Vídeo MP4 (Melhor qualidade)
2 - Vídeo MP4 (Resolução 720p)
3 - Áudio MP3
4 - Áudio M4A
""")
opcao = input("Escolha uma opção: ")

#Verifica a opção escolhida e configura as opções de download do yt-dlp
match opcao:
    case "1":
        opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
            'outtmpl': f'{folder}/%(title)s.%(ext)s',   
        }
    case "2":
        opts = {
            'format': 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/mp4',
            'outtmpl': f'{folder}/%(title)s.%(ext)s',   
        }
    case "3":
        opts = {
            'format': 'bestaudio/best',
            'writethumbnail': True,
            'outtmpl': f'{folder}/%(title)s.%(ext)s',
            'postprocessors': [
                {
                    'key': 'FFmpegThumbnailsConvertor',
                    'format': 'jpg',
                },
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                },
                {
                    'key': 'EmbedThumbnail',
                }
            ],
            'postprocessor_args': {
                'ThumbnailsConvertor+FFmpeg_o': [
                    '-vf',
                    "crop='if(gt(ih,iw),iw,ih):if(gt(iw,ih),ih,iw)'"
                ]
            }
        }
    case "4":
        opts = {
            'format': 'bestaudio[ext=m4a]/best',
            'writethumbnail': True,
            'outtmpl': f'{folder}/%(title)s.%(ext)s',

            'postprocessors': [
                {
                    'key': 'FFmpegThumbnailsConvertor',
                    'format': 'jpg',
                },
                {
                    'key': 'EmbedThumbnail',
                }
            ],

            'postprocessor_args': {
                'ThumbnailsConvertor+FFmpeg_o': [
                    '-vf',
                    "crop='if(gt(ih,iw),iw,ih):if(gt(iw,ih),ih,iw)'"
                ]
            }
        }
    case _:
        print("Opção inválida.")
        exit()

#Baixa o vídeo ou áudio usando yt-dlp
with yt_dlp.YoutubeDL(opts) as ydl:
    ydl.download([url])