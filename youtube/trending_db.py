import requests
from bs4 import BeautifulSoup

#start beautifulsoup scraping
URL="https://www.youtube.com/feed/trending"
result = requests.get(URL)
soup = BeautifulSoup(result.text, "html.parser")
div = soup.findAll('div', class_= 'yt-lockup')

rsSet=[]

for result in div:
    rsSet.append(result)

num_of_block = len(rsSet)
block = rsSet
print(num_of_block)

contents = []

for i in range(num_of_block):
    content = block[i].findAll('div', class_='yt-lockup-dismissable')

    for details in content:
        contents.append(details)

# print(contents[3])

image = contents[3].find("span", class_="yt-thumb-simple").find("img")["src"]
title = contents[3].find('div', class_= 'yt-lockup-content').find("a")["title"]
channel = contents[3].find('div', class_='yt-lockup-description').text

print(channel)
