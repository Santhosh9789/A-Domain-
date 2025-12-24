
import os
import re

ROOT_DIR = r"f:/vs code project/Domain-main (3)/Domain-main/Projects/projects"

def remove_lenis_and_enable_native_smooth_scroll(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Remove Lenis CDN script
    new_content = re.sub(r'<script src="https://unpkg\.com/lenis[^"]+"></script>', '', content)
    
    # 2. Remove Lenis Initialization Script
    # Matches <script>...new Lenis...raf...</script>
    # We use DOTALL to match newlines
    new_content = re.sub(r'<script>\s*// Smooth scrolling.*?\bnew Lenis\b.*?</script>', '', new_content, flags=re.DOTALL)
    
    # Fallback: if the comment isn't there, just look for new Lenis block
    new_content = re.sub(r'<script>\s*const lenis = new Lenis.*?</script>', '', new_content, flags=re.DOTALL)
    
    # 3. Add scroll-behavior: smooth to CSS if not present
    if 'scroll-behavior: smooth' not in new_content:
        # Inject into <style> or existing CSS
        if '</style>' in new_content:
            new_content = new_content.replace('</style>', 'html { scroll-behavior: smooth; }\n</style>')
            
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Removed Lenis from: {file_path}")

for root, dirs, files in os.walk(ROOT_DIR):
    for file in files:
        if file.endswith('.html'):
             remove_lenis_and_enable_native_smooth_scroll(os.path.join(root, file))
