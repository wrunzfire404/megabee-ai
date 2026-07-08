import glob

files_changed = 0

def replace_in_file(filepath):
    global files_changed
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 1. Images
    content = content.replace('"/gigabee-logo.png"', '"https://gigabee.io/gigabee-logo.png"')
    content = content.replace("'/gigabee-logo.png'", "'https://gigabee.io/gigabee-logo.png'")
    content = content.replace('"/opengraph.jpg"', '"https://gigabee.io/opengraph.jpg"')
    content = content.replace('"/favicon.ico"', '"https://gigabee.io/favicon.ico"')
    
    # 2. Network (devnet -> mainnet-beta)
    content = content.replace('devnet', 'mainnet-beta')
    content = content.replace('Devnet', 'Mainnet')
    
    # 3. $GB -> $MB
    content = content.replace('$GB', '$MB')
    
    # 4. Token address -> coming soon
    content = content.replace('7NcMKMrXPBVCWPcs9SSqnF6ZGy5neAtzTZpFqZqLquaP', 'coming soon on pump.fun')

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        files_changed += 1
        print(f"Updated {filepath}")

for f in glob.glob('public/assets/*.js'):
    replace_in_file(f)
for f in glob.glob('public/assets/*.css'):
    replace_in_file(f)
replace_in_file('index.html')

print(f"Total files updated: {files_changed}")
