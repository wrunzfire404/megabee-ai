import os
import requests
import re
import concurrent.futures
import shutil

url_base = "https://gigabee.io/"
target_dir = r"c:\Tools\project crypto\megabee-ai"
public_dir = os.path.join(target_dir, "public")
assets_dir = os.path.join(public_dir, "assets")

# Wipe assets dir
if os.path.exists(assets_dir):
    shutil.rmtree(assets_dir)
os.makedirs(assets_dir)

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0"})

# Step 1: Download new index.html
res = session.get(url_base)
res.raise_for_status()
html_content = res.text

# Find index JS and CSS
js_match = re.search(r'src="(/assets/index-[a-zA-Z0-9_-]+\.js)"', html_content)
css_match = re.search(r'href="(/assets/index-[a-zA-Z0-9_-]+\.css)"', html_content)

main_js_path = js_match.group(1)
main_css_path = css_match.group(1)

# Step 2: Download main JS and CSS
main_js_content = session.get(url_base.rstrip('/') + main_js_path).text
main_css_content = session.get(url_base.rstrip('/') + main_css_path).text

# Step 3: Extract chunks from main JS
matches = set(re.findall(r'([a-zA-Z0-9_-]+\.(?:js|css))', main_js_content))
matches.update(re.findall(r'([a-zA-Z0-9_-]+\.(?:woff2|woff|ttf|png|svg|jpg))', main_css_content))
matches.add(main_js_path.replace('/assets/', ''))
matches.add(main_css_path.replace('/assets/', ''))

def download_and_process(filename):
    file_url = url_base.rstrip('/') + '/assets/' + filename
    r = session.get(file_url)
    
    # If Vercel responds with index.html (SPA fallback), skip it.
    if r.status_code == 200 and not r.text.startswith('<!DOCTYPE html>'):
        file_content = r.text
        if filename.endswith(".js") or filename.endswith(".css"):
            file_content = file_content.replace("Gigabee", "Megabee AI")
            file_content = file_content.replace("GIGABEE", "MEGABEE AI")
            file_content = file_content.replace("Gigabee_", "megabeeAI")
            file_content = file_content.replace("gigabee.io", "megabee.ai")
            file_content = re.sub(r'lovable-badge[^"\'>]*', '', file_content, flags=re.IGNORECASE)
            file_content = re.sub(r'Made with Lovable', 'Made with ❤️', file_content, flags=re.IGNORECASE)
            
            with open(os.path.join(assets_dir, filename), "w", encoding="utf-8") as f:
                f.write(file_content)
        else:
            with open(os.path.join(assets_dir, filename), "wb") as f:
                f.write(r.content)
        return True
    return False

# Download all chunks
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(download_and_process, filename) for filename in matches]
    concurrent.futures.wait(futures)

# Process HTML
html_content = html_content.replace("Gigabee", "Megabee AI")
html_content = html_content.replace("GIGABEE", "MEGABEE AI")
html_content = html_content.replace("@Gigabee_", "@megabeeAI")
html_content = html_content.replace('href="/gigabee-logo.png"', 'href="https://gigabee.io/gigabee-logo.png"')
html_content = html_content.replace('content="/opengraph.jpg"', 'content="https://gigabee.io/opengraph.jpg"')
html_content = html_content.replace("Gigabee_", "megabeeAI")

# Important: ensure script tag uses crossorigin properly or adjust if Vite complains
# Actually, since Vite bundles index.html, we can just save it.
with open(os.path.join(target_dir, "index.html"), "w", encoding="utf-8") as f:
    f.write(html_content)

print("Full scrape completed!")
