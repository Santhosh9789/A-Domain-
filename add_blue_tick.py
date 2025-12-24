
import os
import re

files_to_update = [
    r"f:/vs code project/Domain-main (3)/Domain-main/index.html",
    r"f:/vs code project/Domain-main (3)/Domain-main/blog/index.html",
    r"f:/vs code project/Domain-main (3)/Domain-main/Projects/index.html",
    r"f:/vs code project/Domain-main (3)/Domain-main/careers/index.html"
]

# The Verified Badge HTML
# Using a slightly smaller font size for the tick to ensure it looks elegant.
blue_tick_html = ' <i class="bi bi-patch-check-fill" style="color: #47b2e4; font-size: 0.6em; margin-left: 5px; vertical-align: middle;"></i>'

def process_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Regex patterns to safely insert the tick if it's not already there
    
    # 1. Header Logo (H1)
    # Pattern looks for Blueidealteck inside h1 with class sitename, NOT followed by the icon already.
    # regex: (<h1 class="sitename">Blueidealteck)(?!.*bi-patch-check-fill)(</h1>)
    # Note: simple string replace is safer if we are sure it's not there, but let's be robust.
    
    # We will just do a string replacement for the specific tag structure we observed, 
    # but check if the icon is already present to avoid duplicates.
    
    # Target 1: Header H1
    target_h1 = '<h1 class="sitename">Blueidealteck</h1>'
    replacement_h1 = f'<h1 class="sitename">Blueidealteck{blue_tick_html}</h1>'
    
    if target_h1 in content and 'bi-patch-check-fill' not in content.split(target_h1)[1][:100]: # simplistic check
         content = content.replace(target_h1, replacement_h1)

    # Target 2: Footer Logo (Span)
    target_span = '<span class="sitename">Blueidealteck</span>'
    replacement_span = f'<span class="sitename">Blueidealteck{blue_tick_html}</span>'
    
    if target_span in content:
        # Be careful not to replace it if it's already done (though string replace handles exact match)
        content = content.replace(target_span, replacement_span)

    # Target 3: Copyright (Strong)
    target_strong = '<strong class="px-1 sitename">Blueidealteck</strong>'
    replacement_strong = f'<strong class="px-1 sitename">Blueidealteck{blue_tick_html}</strong>'
    
    if target_strong in content:
        content = content.replace(target_strong, replacement_strong)

    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {file_path}")
    else:
        print(f"No changes needed (or patterns not found): {file_path}")

for file_path in files_to_update:
    process_file(file_path)
