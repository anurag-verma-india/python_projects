from pytube import Playlist

py = Playlist(
    "https://www.youtube.com/playlist?list=PLu88KD9vmyro6jCAmn2fC6aiMjq830N7O"
)
print(f" Downloading : {py.title}")

for video in py.videos:
    video.streams.filter(res="720p").first().download()
