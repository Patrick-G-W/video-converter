import youtube_dl
import ffmpeg
import subprocess
import os
import time
import multiprocessing

youtubeLink = input("YouTube link to download: ")
outputFormat = input("Output format (mp4, flv, webm, ogg, mkv, avi, raw): ")
outputName = input("Output filename: ")

audioCodec = ""
ffmpegVideo = ""


ydl_opts = {
    #'forcefilename': 'test.mp4',
    'outtmpl': 'ydlVideo.mp4',# + outputFormat,
    'format': 'bestvideo/best',
    #'postprocessors': [{
    #    'key': 'FFmpegVideoConvertor',
    #    'preferedformat': 'mp4',
        #'preferedformat': outputFormat,
        #'preferredquality': '192',
    #}],
}

if outputFormat == "avi" or "flv" or "mp4":
    audioCodec = "aac"
if outputFormat == "flv":
    ffmpegVideo = "libx264"
if outputFormat == "mkv":
    ffmpegVideo = "libx265"
if outputFormat == "mp4":
    ffmpegVideo = "libx265"
if outputFormat == "webm":
    ffmpegVideo = "vp9"
    audioCodec = "libvorbis"
if outputFormat == "ogg":
    ffmpegVideo = "libtheora"
    audioCodec = "libvorbis"
if outputFormat == "avi":
    ffmpegVideo = "copy"
if outputFormat == "raw":
    ffmpegVideo = "copy"
    audioCodec = "copy"
    outputFormat = "mp4"

fullOutputName = outputName + "." + outputFormat

print(outputFormat)

audio_ydl_opts = {
    'outtmpl': 'ydlAudio.aac',# + audioCodec,
    'format': 'bestaudio/best',
    #'postprocessors': [{
    #    'key': 'FFmpegExtractAudio',
    #    'preferredcodec': 'aac',
        #'preferredcodec': audioCodec,
        #'preferredquality': '192'
    #}]
}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([youtubeLink])

with youtube_dl.YoutubeDL(audio_ydl_opts) as ydl:
    ydl.download([youtubeLink])


time.sleep(3)

def convert_video(video_output):
    cmds = ['ffmpeg', '-i', 'ydlVideo.mp4', '-i', 'ydlAudio.aac', '-threads', str(multiprocessing.cpu_count()), '-c:v', ffmpegVideo, '-c:a', audioCodec, '-strict', 'experimental', video_output]
    subprocess.Popen(cmds)
    print(cmds)

print(fullOutputName)
#print(videofile)
#print(audiofile)

time.sleep(3)

convert_video(fullOutputName)


time.sleep(1)

os.remove('ydlVideo.mp4')# + outputFormat)
os.remove('ydlAudio.aac')# + audioCodec)
