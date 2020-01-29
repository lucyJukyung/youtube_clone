import requests
from bs4 import BeautifulSoup

URL="https://www.youtube.com"

result = requests.get(URL)
soup = BeautifulSoup(result.text, "html.parser")

def extract_numOfVideos():
    div_s = soup.findAll('div', class_= 'yt-lockup')
    rsSet = []

    for test in div_s:
        rsSet.append(test)

    contents = rsSet

    return contents

block = extract_numOfVideos()
num_of_block = len(block)

# def extract_detail(html):
#     title = html.find("a")["title"]
#     channel = html.find("div", class_= 'yt-lockup-byline').text
#     link = html.find("a")["href"]
#     views_dates = html.findAll("li")
#
#     view_list=[]
#     for li in views_dates:
#         view_list.append(li.text)
#
#     return {
#         'title': title,
#         'channel': channel,
#         'views': view_list[0],
#         'date': view_list[1],
#         'link': f"{URL}{link}"}


def extract_videos(num_of_block):
    videos=[]

    for i in range(num_of_block):
        video  = block[i].findAll('div', class_= 'yt-lockup-content')
        for content in video:
            # block_content = extract_detail(content)
            videos.append(content)

    print(videos[3])
    return videos

# def get_videos():
#     video_contents = extract_numOfVideos()
#     videos = extract_videos(video_contents)
#     return videos

extract_videos(num_of_block)
