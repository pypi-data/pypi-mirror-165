from pytube import Playlist, YouTube, StreamQuery, Stream
from pytube.helpers import safe_filename

pin = input("Enter playlist url: ")
# pin = "https://www.youtube.com/playlist?list=PL3eAkoh7fypr8zrkiygiY1e9osoqjoV9w"
p = Playlist(pin)
# vid = YouTube("https://www.youtube.com/watch?v=Ypwv1mFZ5vU")

print(f'Downloading: {p.title}')

res = ["720p", "480p", "360p", "240p", "144p"]


def getHighResolutionVideo(streams: StreamQuery) -> Stream:
    st = streams.filter(resolution="1080p").first()
    idx = 0
    while not st:
        st = streams.filter(resolution=res[idx]).first()
        idx += 1
    return st
# 

for index, video in enumerate(p.videos):
    vid = YouTube(video.watch_url)
    st = getHighResolutionVideo(video.streams)

    if st:
        filename = f'{index+1}. {safe_filename(st.title)} ({st.resolution}).mp4'
        print(filename)
        st.download(output_path=safe_filename(p.title), filename=filename)
        # video.streams.first().download()
