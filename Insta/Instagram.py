import requests
from bs4 import BeautifulSoup

url = "https://www.instagram.com/pomalaw/"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
soup.prettify()
print(soup)