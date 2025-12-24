import re

# Read the blog index file
with open('f:/vs code project/Domain-main (3)/Domain-main/blog/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# First, remove any .html.html (double extension)
content = content.replace('.html.html', '.html')

# Then fix links that don't have .html
# Pattern: href="../tool-XXXXX" (without .html) -> href="../tool-XXXXX.html"
content = re.sub(r'href="(\.\./tool-[^"]+)(?<!\.html)"', r'href="\1.html"', content)

# Write back
with open('f:/vs code project/Domain-main (3)/Domain-main/blog/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("DONE! Fixed all tool links in blog!")
print("All links now correctly point to .html files")
