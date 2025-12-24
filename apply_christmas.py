import os

ROOT_DIR = r"f:/vs code project/Domain-main (3)/Domain-main"
ASSETS_DIR = "assets/season"
CSS_FILE = "christmas.css"
JS_FILE = "christmas.js"

def apply_effect(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Calculate relative path to assets
        rel_path_to_root = os.path.relpath(ROOT_DIR, os.path.dirname(file_path))
        
        # Normalize path
        if rel_path_to_root == ".":
            path_prefix = ""
        else:
            path_prefix = rel_path_to_root.replace("\\", "/") + "/"

        css_link = f'<link href="{path_prefix}{ASSETS_DIR}/{CSS_FILE}" rel="stylesheet">'
        js_script = f'<script src="{path_prefix}{ASSETS_DIR}/{JS_FILE}"></script>'

        modified = False

        # CSS Handling
        if css_link not in content:
            # Check if commented out version exists? (optional, but good for cleanup)
            # Just insert it
            if "</head>" in content:
                content = content.replace("</head>", f"  {css_link}\n</head>")
                modified = True
            elif "christmas.css" in content:
                 # It exists but maybe with different quoting or spacing, or commented. 
                 # For now, if exact match fails, we assume it's missing or broken.
                 # But to avoid double insert if it's just spacing, let's just proceed.
                 pass

        # JS Handling
        if js_script not in content:
             if "</body>" in content:
                content = content.replace("</body>", f"  {js_script}\n</body>")
                modified = True
        
        # Handle the specific commented out case seen in blog/index.html
        # If we just inserted it, we might now have a duplicate (one active, one commented). 
        # That's visual clutter but functionally fine. 
        # However, if the file HAD it commented, 'js_script not in content' was True (unless the comment EXACTLY matched).
        # The comment in blog/index.html was:
        # <!-- <script src="../assets/season/christmas.js"></script> Uncomment if needed on blog -->
        # My constructed js_script string is: <script src="../assets/season/christmas.js"></script>
        # So 'js_script' IS in the content (inside the comment).  
        # Wait. "<!-- <script ...>" contains "<script ...>".
        # So 'if js_script not in content' would be FALSE. It would think it's there.
        # This is why it skipped.
        
        # FIX: Check if the line is commented.
        # Simple hack: Replace the commented line if found.
        commented_pattern = f'<!-- {js_script} Uncomment if needed on blog -->'
        if commented_pattern in content:
            content = content.replace(commented_pattern, js_script)
            modified = True
        
        # General case: if we found the script tag but it is wrapped in <!-- -->
        # This is getting complex to parse with just strings.
        # Let's trust the "Add if missing" but we need to ensure "Missing" means "Not active".
        
        # Let's change strategy:
        # Always remove any existing reference to christmas.js/css (to clean up comments or old versions)
        # Then add the fresh correct tags.
        # This ensures consistency.
        
        # Remove old lines
        lines = content.splitlines()
        new_lines = []
        for line in lines:
            if "christmas.css" in line or "christmas.js" in line:
                continue # Skip it -> effectively deleting it
            new_lines.append(line)
        
        content = "\n".join(new_lines)
        
        # Now add them back
        if "</head>" in content:
             content = content.replace("</head>", f"  {css_link}\n</head>")
             modified = True
        
        if "</body>" in content:
             content = content.replace("</body>", f"  {js_script}\n</body>")
             modified = True

        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {file_path}")
        else:
            print(f"No changes needed for {file_path}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# Walk through all directories
count = 0
for root, dirs, files in os.walk(ROOT_DIR):
    for file in files:
        if file.lower().endswith(".html"):
            apply_effect(os.path.join(root, file))
            count += 1

print(f"Processed {count} HTML files.")
