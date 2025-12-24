
import os
import re

base_dir = "f:/vs code project/Domain-main (3)/Domain-main/"

# 1. Convert remaining HTML files to folders
remaining_files = [
    "future-blockchain",
    "service-custom-software",
    "service-devops"
]

for item in remaining_files:
    html_file = os.path.join(base_dir, f"{item}.html")
    folder_path = os.path.join(base_dir, item)
    new_file = os.path.join(folder_path, "index.html")
    
    if os.path.exists(html_file):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Fix relative links
        content = content.replace('href="assets/', 'href="../assets/')
        content = content.replace('src="assets/', 'src="../assets/')
        content = content.replace('href="blog/', 'href="../blog/')
        content = content.replace('href="./"', 'href="../"')
        content = content.replace('href="index.html"', 'href="../index.html"')
        
        with open(new_file, "w", encoding="utf-8") as f:
            f.write(content)
            
        os.remove(html_file)
        print(f"Converted {item}.html -> {item}/index.html")

# 2. Update blog/index.html to have "Read More" on ALL cards
blog_path = os.path.join(base_dir, "blog/index.html")

with open(blog_path, "r", encoding="utf-8") as f:
    content = f.read()

# Logic: Find tool cards. They currently look like:
# <p class="small text-muted mb-2">Frontend Powerhouse</p>
# <a href="../tool-react/" class="stretched-link"></a>
#
# We want to change them to:
# <p class="small text-muted mb-2">Frontend Powerhouse</p>
# <div class="mt-2 text-primary small fw-bold">Read More <i class="bi bi-arrow-right"></i></div>
# <a href="../tool-react/" class="stretched-link"></a>
#
# (The stretched-link will overlay the "Read More" text making it clickable too)

# Regex to match the pattern inside the tool cards
# Matches: <p class="small text-muted mb-2">...</p>\s*<a href="..." class="stretched-link"></a>
pattern = r'(<p class="small text-muted mb-2">[^<]+</p>)\s*(<a href="[^"]+" class="stretched-link"></a>)'

replacement = r'\1\n                            <div class="mt-2 text-primary small fw-bold">Read More <i class="bi bi-arrow-right"></i></div>\n                            \2'

new_content = re.sub(pattern, replacement, content)

if content != new_content:
    with open(blog_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Updated blog/index.html with Read More links on tool cards.")
else:
    print("No tool cards found to update or already updated.")

