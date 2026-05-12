import requests
from bs4 import BeautifulSoup
import json
import time

base_url = "https://www.enepsters.com/author/sandesrb/"
page_url_template = "https://www.enepsters.com/author/sandesrb/page/{}/"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

articles = []
page = 1

while True:
    if page == 1:
        url = base_url
    else:
        url = page_url_template.format(page)
    
    print(f"Scraping {url}...")
    response = requests.get(url, headers=headers, allow_redirects=False)
    
    if response.status_code != 200:
        print(f"Failed to fetch {url} or reached the end. Status code: {response.status_code}")
        break
        
    soup = BeautifulSoup(response.text, 'html.parser')
    posts = soup.find_all(class_='type-post')
    
    if not posts:
        print("No more posts found on this page.")
        break
        
    for post in posts:
        title_tag = post.find('h5', class_='entry-title')
        if not title_tag:
            continue
            
        link_tag = title_tag.find('a')
        if not link_tag:
            continue
            
        title = link_tag.text.strip()
        link = link_tag.get('href')
        
        date_div = post.find('div', class_='time')
        date = date_div.text.strip() if date_div else ""
        
        category_tag = post.find('a', class_='single_category_title')
        category = category_tag.text.strip() if category_tag else ""
        
        articles.append({
            'title': title,
            'link': link,
            'date': date,
            'category': category
        })
        
    page += 1
    time.sleep(1) # Be nice to the server

print(f"Total articles scraped: {len(articles)}")

with open('articles.json', 'w', encoding='utf-8') as f:
    json.dump(articles, f, indent=4, ensure_ascii=False)

print("Saved articles to articles.json")
