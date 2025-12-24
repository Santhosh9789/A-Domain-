
with open('tool-cloud-migration.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix all relative paths by removing "../"
# This assumes the file is now in the root directory
new_content = content.replace('href="../', 'href="').replace('src="../', 'src="')

with open('tool-cloud-migration.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Fixed all relative paths in tool-cloud-migration.html")
