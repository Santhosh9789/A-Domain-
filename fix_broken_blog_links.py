import re

file_path = "f:/vs code project/Domain-main (3)/Domain-main/blog/index.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Pattern to remove the specific broken anchor tags.
# They look like: <a href="../process-discovery" class="read-more...">Read More <i ...></i></a>
# I'll use a regex that matches these <a href="../process-..." ...>...</a> and valid ones too if they are broken.
# List of known broken prefixes
broken_prefixes = [
    "../process-",
    "../service-",
    "../future-"
]

# We need to be careful not to remove valid links if any.
# Only those starting with the above.

# Regex explanation:
# <a\s+[^>]*href="(\.\./(process-|service-|future-)[^"]+)"[^>]*>.*?</a>
# Flags: DOTALL to match across lines

pattern = r'<a\s+[^>]*href="(\.\./(?:process-|service-|future-)[^"]+)"[^>]*>.*?</a>'

# Also remove the wrapping <h5> links if they exist, e.g. <a href="../service-ui-ux"><h5...></a>
# Pattern for wrapping titles: <a href="..."><h5 ...>...</h5></a>
pattern_title_link = r'<a\s+href="(\.\./(?:process-|service-|future-)[^"]+)">\s*(<h5.*?</h5>)\s*</a>'

# First remove title links, keeping the h5
def replace_title_link(match):
    # Return just the inner h5
    return match.group(2)

new_content = re.sub(pattern_title_link, replace_title_link, content, flags=re.DOTALL)

# Now remove the "Read More" buttons entirely
new_content = re.sub(pattern, "", new_content, flags=re.DOTALL)

if content != new_content:
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Successfully removed broken 'Read More' links and title links.")
else:
    print("No broken links found matching the pattern.")
