import json
import html
import markdown
from bs4 import BeautifulSoup

with open('articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scraped Archive: Sandesh Rajbhandari</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; background-color: #f9f9f9; }
        h1 { text-align: center; color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; margin-bottom: 30px; }
        .notice { background-color: #fff3cd; color: #856404; padding: 15px; border-radius: 4px; border: 1px solid #ffeeba; margin-bottom: 30px; text-align: center; font-weight: bold; }
        .article { background-color: #fff; padding: 20px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 20px; cursor: pointer; transition: transform 0.2s, box-shadow 0.2s; }
        .article:hover { transform: translateY(-2px); box-shadow: 0 4px 10px rgba(0,0,0,0.15); }
        .article-title { margin: 0 0 10px 0; color: #2980b9; }
        .article-meta { font-size: 0.9em; color: #7f8c8d; margin-bottom: 15px; }
        .article-preview { margin-bottom: 15px; color: #555; }
        .reference-link { font-size: 0.9em; display: inline-block; background-color: #ecf0f1; padding: 5px 10px; border-radius: 3px; text-decoration: none; color: #34495e; transition: background-color 0.2s; }
        .reference-link:hover { background-color: #bdc3c7; }
        .full-content-hidden { display: none; }
        
        .modal { display: none; position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; overflow: auto; background-color: rgba(0,0,0,0.6); }
        .modal-content { background-color: #fefefe; margin: 5% auto; padding: 30px; border: 1px solid #888; width: 80%; max-width: 800px; border-radius: 8px; box-shadow: 0 4px 20px rgba(0,0,0,0.2); position: relative; }
        .close-btn { color: #aaa; position: absolute; top: 15px; right: 25px; font-size: 28px; font-weight: bold; cursor: pointer; }
        .close-btn:hover, .close-btn:focus { color: black; text-decoration: none; }
        #modalBody { margin-top: 20px; line-height: 1.8; color: #222; }
        #modalBody img { max-width: 100%; height: auto; }
        #modalBody h1, #modalBody h2, #modalBody h3 { color: #2c3e50; }
        #modalBody p { margin-bottom: 15px; }
        #modalBody a { color: #3498db; text-decoration: none; }
        #modalBody a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>Archive: Articles by Sandesh Rajbhandari</h1>
    <div class="notice">Note: This is a locally scraped archive. The articles below are generated from scraped data, not live pages. Click an article to view its full content.</div>
    <div id="articles-container">
"""

for i, article in enumerate(articles):
    content_md = article.get('content', '')
    
    # Render markdown to HTML
    rendered_html = markdown.markdown(content_md, extensions=['extra'])
    
    # Safely extract a preview (first paragraph or 300 chars of text)
    soup = BeautifulSoup(rendered_html, 'html.parser')
    preview_html = ""
    for p in soup.find_all('p'):
        if p.text.strip():
            # Get the first paragraph as a preview, keep HTML formatting like <strong>
            preview_html = str(p)
            break
            
    if not preview_html:
        preview_text = soup.get_text()
        preview_html = html.escape(preview_text[:300] + "...") if preview_text else "No preview available."
    
    safe_title = html.escape(article['title'])
    safe_date = html.escape(article['date'])
    safe_category = html.escape(article['category'])
    safe_link = html.escape(article['link'])
    
    # We don't escape the rendered HTML because we want to inject it as actual HTML
    # We can use base64 or a script tag to safely store it, but a hidden div is usually fine
    # if the source markdown is trusted (which it is here, mostly).
    # To avoid quoting issues, we'll store it inside a div directly.
    
    html_content += f"""
        <div class="article" onclick="openModal({i})">
            <h2 class="article-title">{safe_title}</h2>
            <div class="article-meta">
                <span><strong>Date:</strong> {safe_date}</span> | 
                <span><strong>Category:</strong> {safe_category}</span>
            </div>
            <div class="article-preview">
                {preview_html}
            </div>
            <a href="{safe_link}" class="reference-link" target="_blank" rel="noopener noreferrer" onclick="event.stopPropagation();">View Original Source &rarr;</a>
            <div id="full-content-{i}" class="full-content-hidden">{rendered_html}</div>
        </div>
"""

html_content += """
    </div>

    <div id="articleModal" class="modal">
        <div class="modal-content">
            <span class="close-btn" onclick="closeModal()">&times;</span>
            <h2 id="modalTitle" class="article-title"></h2>
            <div id="modalMeta" class="article-meta"></div>
            <div id="modalBody"></div>
            <br><br>
            <a id="modalLink" href="" class="reference-link" target="_blank" rel="noopener noreferrer">View Original Source &rarr;</a>
        </div>
    </div>

    <script>
        var modal = document.getElementById("articleModal");
        
        function openModal(index) {
            var fullContentDiv = document.getElementById('full-content-' + index);
            var articleDiv = fullContentDiv.closest('.article');
            
            var title = articleDiv.querySelector('.article-title').innerText;
            var meta = articleDiv.querySelector('.article-meta').innerHTML;
            var link = articleDiv.querySelector('.reference-link').href;
            var fullContent = fullContentDiv.innerHTML;
            
            document.getElementById("modalTitle").innerText = title;
            document.getElementById("modalMeta").innerHTML = meta;
            document.getElementById("modalBody").innerHTML = fullContent;
            document.getElementById("modalLink").href = link;
            
            modal.style.display = "block";
            document.body.style.overflow = "hidden";
        }
        
        function closeModal() {
            modal.style.display = "none";
            document.body.style.overflow = "auto";
        }
        
        window.onclick = function(event) {
            if (event.target == modal) {
                closeModal();
            }
        }
        
        document.addEventListener('keydown', function(event) {
            if (event.key === "Escape") {
                closeModal();
            }
        });
    </script>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("index.html generated with Markdown rendered!")
