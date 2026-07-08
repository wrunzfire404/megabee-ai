import os
import requests
import re
import concurrent.futures

url_base = "https://gigabee.io/assets/"
public_dir = r"c:\Tools\project crypto\megabee-ai\public\assets"
index_file = os.path.join(public_dir, "index-NMUXAlof.js")

with open(index_file, "r", encoding="utf-8") as f:
    content = f.read()

# Find all potential asset filenames like home-BSm88Wsi.js or icons-B8-CkEFo.js
matches = set(re.findall(r'([a-zA-Z0-9_-]+\.(?:js|css))', content))
print(f"Found {len(matches)} potential assets in index.js")

# Find them in the css file too
css_file = os.path.join(public_dir, "index-DeAnbZhz.css")
if os.path.exists(css_file):
    with open(css_file, "r", encoding="utf-8") as f:
        matches.update(re.findall(r'([a-zA-Z0-9_-]+\.(?:woff2|woff|ttf|png|svg|jpg))', f.read()))

# Exclude already downloaded index files
matches.discard("index-NMUXAlof.js")
matches.discard("index-DeAnbZhz.css")

def download_and_process(filename):
    file_url = url_base + filename
    r = requests.get(file_url)
    if r.status_code == 200:
        file_content = r.text
        if filename.endswith(".js") or filename.endswith(".css"):
            file_content = file_content.replace("Gigabee", "Megabee AI")
            file_content = file_content.replace("GIGABEE", "MEGABEE AI")
            file_content = file_content.replace("Gigabee_", "megabeeAI")
            file_content = file_content.replace("gigabee.io", "megabee.ai")
            file_content = re.sub(r'lovable-badge[^"\'>]*', '', file_content, flags=re.IGNORECASE)
            file_content = re.sub(r'Made with Lovable', 'Made with ❤️', file_content, flags=re.IGNORECASE)
            
            with open(os.path.join(public_dir, filename), "w", encoding="utf-8") as f:
                f.write(file_content)
        else:
            with open(os.path.join(public_dir, filename), "wb") as f:
                f.write(r.content)
        print(f"Downloaded and processed: {filename}")
        return filename
    else:
        # Some matches might just be random strings, not files, ignore 404s
        pass
    return None

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(download_and_process, filename) for filename in matches]
    concurrent.futures.wait(futures)

print("Finished downloading chunks.")
