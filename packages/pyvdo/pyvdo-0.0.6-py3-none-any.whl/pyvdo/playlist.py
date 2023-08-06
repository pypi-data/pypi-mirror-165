from pytube import Playlist, StreamQuery, Stream
from pytube.helpers import safe_filename
from click import echo


res = ["720p", "480p", "360p", "240p", "144p"]


def getHighResolutionVideo(streams: StreamQuery) -> Stream:
    st = streams.filter(resolution="1080p").first()
    idx = 0
    while not st:
        st = streams.filter(resolution=res[idx]).first()
        idx += 1
    return st
#


def downloadPlaylist(playlist: str):
    p = Playlist(playlist)
    echo(f'Downloading: {p.title}')

    for index, video in enumerate(p.videos):
        st = getHighResolutionVideo(video.streams)

        if st:
            filename = f'{index+1}. {safe_filename(st.title)} ({st.resolution}).mp4'
            echo(filename)
            st.download(output_path=safe_filename(p.title), filename=filename)
            # video.streams.first().download()
