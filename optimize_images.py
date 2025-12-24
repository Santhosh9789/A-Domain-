import os
import re

ROOT_DIR = r"f:/vs code project/Domain-main (3)/Domain-main"

def add_lazy_loading(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Regex to find img tags that don't have loading attribute
        # Check carefully to not corrupt tags
        # Strategy: find <img ... > and if "loading=" is not present, add loading="lazy"
        
        def replace_img(match):
            img_tag = match.group(0)
            if "loading=" not in img_tag:
                # Insert loading="lazy" before the closing >
                # Handle self-closing /> or just >
                if "/>" in img_tag:
                    return img_tag.replace("/>", ' loading="lazy" />')
                else:
                    return img_tag.replace(">", ' loading="lazy">')
            return img_tag

        new_content = re.sub(r'<img[^>]+>', replace_img, content)

        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated images in {file_path}")
        else:
            # print(f"No changes for {file_path}")
            pass

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# Walk through all directories
count = 0
for root, dirs, files in os.walk(ROOT_DIR):
    for file in files:
        if file.lower().endswith(".html"):
            add_lazy_loading(os.path.join(root, file))
            count += 1

print(f"Processed {count} HTML files for lazy loading.")
