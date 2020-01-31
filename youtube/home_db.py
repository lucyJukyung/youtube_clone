import requests
from bs4 import BeautifulSoup

#start beautifulsoup scraping
URL="https://www.youtube.com"
result = requests.get(URL)
soup = BeautifulSoup(result.text, "html.parser")
div_s = soup.findAll('div', class_= 'yt-lockup')
rsSet = []

for test in div_s:
    rsSet.append(test)

num_of_block = len(rsSet) #extracted number of video blocks
block = rsSet
print(num_of_block)

#start scraping contents from each block
def extract_detail(html):
    title = html.find('div', class_= 'yt-lockup-content').find("a")["title"]
    channel = html.find('div', class_= 'yt-lockup-content').find("div", class_= 'yt-lockup-byline').text
    link = html.find('div', class_= 'yt-lockup-content').find("a")["href"]
    views_dates = html.find('div', class_= 'yt-lockup-content').findAll("li")

    view_list=[]
    for li in views_dates:
        view_list.append(li.text)

    image = html.find("span", class_="yt-thumb-simple").find("img")["src"]
    if "https://" not in image:
        image = html.find("span", class_="yt-thumb-simple").find("img")["data-thumb"]

    video_time = html.find("span", class_="yt-thumb-simple").find("span").text

    return {
        'title': title,
        'channel': channel,
        'views': view_list[0],
        'date': view_list[1],
        'link': f"{URL}{link}",
        'image': image,
        'video_time': video_time
    }

def extract_videos(num_of_block):
    contents = []

    for i in range(num_of_block):
        content = block[i].findAll('div', class_='yt-lockup-dismissable')
        for details in content:
            block_content = extract_detail(details)
            contents.append(block_content)

    return contents

extract_videos(num_of_block)
