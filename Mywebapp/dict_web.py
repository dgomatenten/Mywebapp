from bs4 import BeautifulSoup
import requests
import re

url = "https://dictionary.com/browse/empirical"
req = requests.get(url)

soup=BeautifulSoup(req.text, 'lxml')
audio = soup.find_all('source',type='audio/mpeg')

for link in audio:
    print(link.get('src'))
