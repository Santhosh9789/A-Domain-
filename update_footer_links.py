import os

ROOT_DIR = r"f:/vs code project/Domain-main (3)/Domain-main"

def update_footer(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Define the target line and the line to insert
        # Note: We try to handle potentially slightly different formatting if possible, 
        # but exact match is safest for now based on what we saw.
        target_str = '<li><i class="bi bi-chevron-right"></i> <a href="/careers/">Careers</a></li>'
        insert_str = '\n            <li><i class="bi bi-chevron-right"></i> <a href="/Projects/">Projects</a></li>'

        if target_str in content:
            if '/Projects/"' not in content[content.index(target_str):content.index(target_str)+300]: 
                 # crude check to see if it's already there in the immediate vicinity
                 new_content = content.replace(target_str, target_str + insert_str)
                 
                 with open(file_path, 'w', encoding='utf-8') as f:
                     f.write(new_content)
                 print(f"Updated footer in {file_path}")
            else:
                 # print(f"Projects link already exists in {file_path}")
                 pass
        else:
            # Try finding without leading / in case some pages use relative
            target_str_rel = '<li><i class="bi bi-chevron-right"></i> <a href="careers/">Careers</a></li>'
            if target_str_rel in content:
                if 'Projects' not in content[content.index(target_str_rel):content.index(target_str_rel)+300]:
                    new_content = content.replace(target_str_rel, target_str_rel + insert_str)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated footer (relative) in {file_path}")
            else:
                # print(f"Could not find 'Careers' link in footer of {file_path}")
                pass

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# Walk through all directories
count = 0
for root, dirs, files in os.walk(ROOT_DIR):
    for file in files:
        if file.lower().endswith(".html"):
            update_footer(os.path.join(root, file))
            count += 1

print(f"Processed {count} HTML files for footer update.")
