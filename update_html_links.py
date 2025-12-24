import re
import os

files_to_update = [
    "f:/vs code project/Domain-main (3)/Domain-main/blog/index.html",
    "f:/vs code project/Domain-main (3)/Domain-main/index.html",
    "f:/vs code project/Domain-main (3)/Domain-main/tool-cloud-migration/index.html" # Also update internal links here if any
]

# Pattern: href=".../tool-name.html" -> href=".../tool-name/"
# Or href="tool-name.html" -> href="tool-name/"

def update_links(file_path):
    if not os.path.exists(file_path):
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace .html with / for tool links
    # Regex looks for tool-*.html and replaces with tool-*/
    new_content = re.sub(r'href="(.*?tool-[a-zA-Z0-9-]+)\.html"', r'href="\1/"', content)
    
    # Also handle the case where it might be just tool-react.html (no path)
    # new_content = re.sub(r'href="(tool-[a-zA-Z0-9-]+)\.html"', r'href="\1/"', new_content)

    if content != new_content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated links in {file_path}")
    else:
        print(f"No changes needed in {file_path}")

for file in files_to_update:
    update_links(file)
