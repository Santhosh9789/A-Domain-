
import os
import re

ROOT_DIR = r"f:/vs code project/Domain-main (3)/Domain-main/Projects/projects"

def optimize_images_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Regex for Unsplash images that might be missing optimization params
    # We look for src="https://images.unsplash.com/..."
    # We want to ensure it has w=... and q=...
    
    def replacer(match):
        url = match.group(0)
        
        # Check if it already has width
        if 'w=' in url and 'q=' in url:
            return url
        
        # If it has query params already (?), append with &
        # If not, add ?
        separator = '&' if '?' in url else '?'
        
        # Add optimization params: width 800 (good for most desktop), quality 80, format auto
        # We don't want to double add if some exist
        params = []
        if 'w=' not in url:
            params.append('w=800')
        if 'q=' not in url:
            params.append('q=80')
        if 'auto=format' not in url:
            params.append('auto=format')
        if 'fit=crop' not in url:
            params.append('fit=crop')
            
        return url + separator + "&".join(params)

    # Regex: src="(https://images.unsplash.com/[^"]+)"
    # Captures the URL inside src attribute
    # We only modify the URL part.
    
    new_content = re.sub(r'https://images\.unsplash\.com/[^"\']+', replacer, content)
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Optimized images in: {file_path}")

for root, dirs, files in os.walk(ROOT_DIR):
    for file in files:
        if file.endswith('.html') or file.endswith('.js') or file.endswith('.css'):
            optimize_images_in_file(os.path.join(root, file))
