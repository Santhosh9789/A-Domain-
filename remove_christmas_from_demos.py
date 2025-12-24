import os

# Subdirectory containing the demos
DEMO_DIR = r"f:/vs code project/Domain-main (3)/Domain-main/Projects/projects"

def remove_effect(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        lines = content.splitlines()
        new_lines = []
        modified = False
        
        for line in lines:
            # Check for our specific christmas assets
            if "christmas.css" in line or "christmas.js" in line:
                modified = True
                continue # Skip writing this line
            new_lines.append(line)

        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("\n".join(new_lines))
            print(f"Removed effect from {file_path}")
        else:
            print(f"No effect found in {file_path}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# Walk through the demo directory
count = 0
for root, dirs, files in os.walk(DEMO_DIR):
    for file in files:
        if file.lower().endswith(".html"):
            remove_effect(os.path.join(root, file))
            count += 1

print(f"Processed {count} demo HTML files.")
