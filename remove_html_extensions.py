
import os
import re

# Define the root directory
ROOT_DIR = r"f:/vs code project/Domain-main (3)/Domain-main"

# Regex to find hrefs ending in .html
# We want to match text like href="something.html" or href='something.html'
# We capture the quote to put it back, and the url content.
# Only modifying relative paths or absolute paths on this domain (but assuming relative for internal links usually)

# Pattern: attributes regex is tricky. Simple find/replace is safer if we target href="...".
# pattern = r'href=(["\'])(.*?)\.html(["\'])'
# But we need to exclude http:// and https://

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified_content = content
    
    # Callback function for regex sub
    def replacement(match):
        quote = match.group(1)
        url = match.group(2)
        end_quote = match.group(3)
        
        # Skip external links
        if url.startswith(('http:', 'https:', '#', 'mailto:', 'tel:')):
            return match.group(0)
        
        # Handle index.html special cases
        if url.endswith('index.html'):
             # index.html -> ./
             # folder/index.html -> folder/
             # /index.html -> /
             new_url = url[:-10] # remove index.html
             if new_url == "":
                 new_url = "./"
             elif new_url == "/":
                 new_url = "/" # keep as root
             # else it might be folder/ which is fine
        else:
             # Just remove .html
             new_url = url[:-5]
        
        # If new_url is empty (e.g. was just .html? unlikely), set to ./
        if not new_url: 
            new_url = "./"
            
        print(f"  Replacing {url}.html with {new_url}")
        return f'href={quote}{new_url}{end_quote}'

    # Regex search for href="... .html" 
    # We use a broad regex: href=["']([^"']+\.html)["']
    pattern = re.compile(r'href=(["\'])([^"\']+?)\.html(["\'])', re.IGNORECASE)
    
    modified_content = pattern.sub(replacement, content)
    
    if content != modified_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        print(f"Updated: {file_path}")

# Walk recursively
for root, dirs, files in os.walk(ROOT_DIR):
    for file in files:
        if file.endswith('.html'):
            process_file(os.path.join(root, file))
