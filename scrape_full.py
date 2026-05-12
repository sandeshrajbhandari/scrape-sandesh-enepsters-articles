import json
import requests
from bs4 import BeautifulSoup
import time
import markdownify

with open('articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

print(f"Starting to fetch full content for {len(articles)} articles...")

for i, article in enumerate(articles):
    url = article['link']
    print(f"[{i+1}/{len(articles)}] Fetching {url}...")
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            content_div = soup.find('div', class_='post-content')
            if content_div:
                for script in content_div(["script", "style"]):
                    script.extract()
                
                # Convert HTML to Markdown
                md_text = markdownify.markdownify(str(content_div), heading_style="ATX", strip=['img']).strip()
                article['content'] = md_text
            else:
                article['content'] = ""
                print(f"  -> Warning: No post-content found for {url}")
        else:
            print(f"  -> Failed to fetch. Status code: {response.status_code}")
            article['content'] = ""
            
    except Exception as e:
        print(f"  -> Error fetching {url}: {e}")
        article['content'] = ""
        
    time.sleep(0.5) 

with open('articles.json', 'w', encoding='utf-8') as f:
    json.dump(articles, f, indent=4, ensure_ascii=False)

print("Finished fetching full content. Updated articles.json")