
import os

files_to_update = [
    r"f:/vs code project/Domain-main (3)/Domain-main/index.html",
    r"f:/vs code project/Domain-main (3)/Domain-main/blog/index.html",
    r"f:/vs code project/Domain-main (3)/Domain-main/Projects/index.html",
    r"f:/vs code project/Domain-main (3)/Domain-main/careers/index.html"
]

# Emoji to add. 
# ☑️ is often blue-ish. 
# 🔹 is blue. 
# But standard "Verified" is often implied by a check.
# Let's use the text checkmark or the ballot box.
# User asked for "Blue Tick". 
# We will add "☑️" (Ballot Box with Check) which renders as a blue box with white check on many systems (Windows 10/11, Android, iOS).

tick_emoji = " ☑️"

def update_title(file_path):
    if not os.path.exists(file_path):
        print(f"File found: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple logic: Find <title>...</title> and insert if not present.
    import re
    
    # Regex to find title content
    # We want to replace the closing </title> with emoji + </title>, but only if it's not already there.
    
    pattern = re.compile(r'(<title>.*?)(</title>)', re.IGNORECASE | re.DOTALL)
    
    def replacer(match):
        title_content = match.group(1)
        closing = match.group(2)
        if "☑️" in title_content or "✔" in title_content:
            return match.group(0) # Already has a tick
        return f"{title_content}{tick_emoji}{closing}"
    
    new_content = pattern.sub(replacer, content)
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated Title in: {file_path}")
    else:
        print(f"No changes (Title already has tick or not found): {file_path}")

for fp in files_to_update:
    update_title(fp)
