import re
import glob

for f in glob.glob('public/assets/*.js'):
    with open(f, encoding='utf-8') as file:
        content = file.read()
        matches = set(re.findall(r'["\'](/[^"\']+\.(?:png|jpg|svg|webp|gif))["\']', content))
        if matches:
            print(f, matches)
