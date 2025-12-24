
import os

files = [
    r"f:/vs code project/Domain-main (3)/Domain-main/index.html",
    r"f:/vs code project/Domain-main (3)/Domain-main/blog/index.html",
    r"f:/vs code project/Domain-main (3)/Domain-main/Projects/index.html",
    r"f:/vs code project/Domain-main (3)/Domain-main/careers/index.html"
]

# The precise string we added
tick_html = ' <i class="bi bi-patch-check-fill" style="color: #47b2e4; font-size: 0.6em; margin-left: 5px; vertical-align: middle;"></i>'

for fp in files:
    try:
        if os.path.exists(fp):
            with open(fp, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if tick_html in content:
                new_content = content.replace(tick_html, '')
                with open(fp, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Reverted: {fp}")
            else:
                print(f"No tick found in: {fp}")
    except Exception as e:
        print(f"Error processing {fp}: {e}")
