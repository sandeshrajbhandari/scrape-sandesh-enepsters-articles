import sys
from bs4 import BeautifulSoup

with open('index.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

posts = soup.find_all(class_='type-post') or soup.find_all(class_='post')
if posts:
    print(posts[0].prettify())
