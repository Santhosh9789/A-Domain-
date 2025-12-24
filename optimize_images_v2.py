import os
import re

ROOT_DIR = r"f:/vs code project/Domain-main (3)/Domain-main"

def optimize_images(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Regex to find img tags
        # We want to add loading="lazy" and decoding="async" if not present.
        # This regex covers basic cases.
        
        def replacement(match):
            img_tag = match.group(0)
            
            # Check and add loading="lazy"
            if 'loading=' not in img_tag:
                 img_tag = img_tag[:-1] + ' loading="lazy">'
            
            # Check and add decoding="async"
            if 'decoding=' not in img_tag:
                 # Be careful not to break the tag if we just added loading
                 if img_tag.endswith(' loading="lazy">'):
                     img_tag = img_tag[:-16] + ' loading="lazy" decoding="async">'
                 else:
                     img_tag = img_tag[:-1] + ' decoding="async">'
            
            return img_tag

        new_content = re.sub(r'<img\s+[^>]*>', replacement, content, flags=re.IGNORECASE)

        if content != new_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Optimized images in {file_path}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# Walk through all directories
count = 0
for root, dirs, files in os.walk(ROOT_DIR):
    for file in files:
        if file.lower().endswith(".html"):
            optimize_images(os.path.join(root, file))
            count += 1

print(f"Processed {count} HTML files for image optimization.")
