import os

ROOT_DIR = r"f:/vs code project/Domain-main (3)/Domain-main"

def get_relative_assets_path(file_path):
    # file_path is the directory containing the HTML file
    rel_path = os.path.relpath(file_path, ROOT_DIR)
    
    if rel_path == ".":
        return ""
    
    # Split by separator to count segments
    # Handle both forward and backward slashes just in case, though os.sep should suffice
    segments = rel_path.replace('\\', '/').split('/')
    depth = len(segments)
    
    return "../" * depth

def fix_favicons(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        relative_prefix = get_relative_assets_path(os.path.dirname(file_path))
        correct_favicon_href = f'{relative_prefix}assets/img/favicon.png'
        correct_apple_href = f'{relative_prefix}assets/img/apple-touch-icon.png'

        lines = content.splitlines()
        new_lines = []
        modified = False

        for line in lines:
            if 'rel="icon"' in line or "rel='icon'" in line:
                # We want to replace the href attribute, or the whole line.
                # Replacing the whole line is safer to ensure valid syntax.
                # Check indentation (approximate)
                indent = line[:len(line) - len(line.lstrip())]
                new_lines.append(f'{indent}<link href="{correct_favicon_href}" rel="icon" type="image/png">')
                modified = True
            elif 'rel="apple-touch-icon"' in line or "rel='apple-touch-icon'" in line:
                indent = line[:len(line) - len(line.lstrip())]
                new_lines.append(f'{indent}<link href="{correct_apple_href}" rel="apple-touch-icon">')
                modified = True
            else:
                new_lines.append(line)
        
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("\n".join(new_lines))
            print(f"Fixed favicons in {file_path}. Pfx: {relative_prefix}")
        else:
             pass

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# Walk through all directories
count = 0
for root, dirs, files in os.walk(ROOT_DIR):
    for file in files:
        if file.lower().endswith(".html"):
            fix_favicons(os.path.join(root, file))
            count += 1

print(f"Processed {count} HTML files for favicon correction.")
