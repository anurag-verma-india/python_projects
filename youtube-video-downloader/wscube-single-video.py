from pytube import YouTube

# link = "https://www.youtube.com/watch?v=FAyKDaXEAgc&list=PLu88KD9vmyro6jCAmn2fC6aiMjq830N7O&index=1"
link = "https://www.youtube.com/shorts/1VAENIcYEIw"
youtube_1 = YouTube(link)

# print(youtube_1.title)
# print(youtube_1.thumbnail_url)

# videos = youtube_1.streams.all()
videos = youtube_1.streams.filter(res="720p")

vid = list(enumerate(videos))
for i in vid:
    print(i)
print()
# strm = int(input("enter : "))
# videos[strm].download()
videos[0].download()
print(f"Successfully downloaded {youtube_1.title}")
