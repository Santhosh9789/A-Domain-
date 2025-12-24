import os

ROOT_DIR = r"f:/vs code project/Domain-main (3)/Domain-main"

def get_relative_assets_path(file_path):
    # Calculate depth relative to ROOT_DIR
    rel_path = os.path.relpath(file_path, ROOT_DIR)
    depth = rel_path.count(os.sep)
    
    if depth == 0:
        return "assets/img/"
    else:
        return "../" * depth + "assets/img/"

def add_favicon(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if 'rel="icon"' in content or "rel='icon'" in content:
            # print(f"Skipping {file_path}, favicon already present.")
            return

        assets_path = get_relative_assets_path(os.path.dirname(file_path))
        favicon_link = f'<link href="{assets_path}favicon.png" rel="icon" type="image/png">'
        apple_link = f'<link href="{assets_path}apple-touch-icon.png" rel="apple-touch-icon">'

        # Insertion point: try before <title> or before </head>
        if "</title>" in content:
            # Insert after title
            insert_marker = "</title>"
            new_content = content.replace(insert_marker, f"{insert_marker}\n  {favicon_link}\n  {apple_link}")
        elif "</head>" in content:
            new_content = content.replace("</head>", f"  {favicon_link}\n  {apple_link}\n</head>")
        else:
            print(f"Could not find insert point in {file_path}")
            return

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Added favicon to {file_path}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# Walk through all directories
count = 0
for root, dirs, files in os.walk(ROOT_DIR):
    for file in files:
        if file.lower().endswith(".html"):
            add_favicon(os.path.join(root, file))
            count += 1

print(f"Processed {count} HTML files for favicon injection.")
