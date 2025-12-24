
import os

# List of files to delete (duplicates of folders)
files_to_delete = [
    "blog-details.html",
    "blog-details-cloud.html",
    "blog-details-software.html",
    "careers.html",
    "future-cyber-security.html",
    "future-game-design.html",
    "future-blockchain.html", # Double check if folder exists, if not keep it? Folder NOT in list. Keeping for safety if folder mismatch. Actually, earlier I didn't see future-blockchain folder. Wait.
    "process-design.html",
    "process-development.html",
    "process-discovery.html",
    "process-launch.html",
    "service-ai-ml.html",
    "service-ui-ux.html",
    "service-web-app.html",
    "tool-adobe-xd.html",
    "tool-azure.html",
    "tool-figma.html",
    "tool-gcp.html",
    "tool-grafana.html",
    "tool-jenkins.html",
    "tool-jest.html",
    "tool-make.html",
    "tool-n8n.html",
    "tool-prometheus.html",
    "tool-pytorch.html",
    "tool-selenium.html",
    "tool-tensorflow.html",
    "tool-terraform.html",
    "tool-zapier.html",
    "blog.html",
    "service-custom-software.html", # Check if folder exists? I recall service-custom-software link, but didn't create folder.
    "service-devops.html" # Same check.
]

# Only delete if a corresponding FOLDER exists to replace it, otherwise we lose content.
# Exception: blog.html and careers.html can go if they are empty/redirects.

base_dir = "f:/vs code project/Domain-main (3)/Domain-main/"

deleted_count = 0

for filename in files_to_delete:
    file_path = os.path.join(base_dir, filename)
    folder_name = filename.replace(".html", "")
    folder_path = os.path.join(base_dir, folder_name)
    
    # Check if folder exists before deleting file (Security check)
    # For blog.html, folder is 'blog'
    # For careers.html, folder is 'careers'
    
    should_delete = False
    
    if os.path.exists(folder_path):
        should_delete = True
    elif filename == "blog.html" and os.path.exists(os.path.join(base_dir, "blog")):
        should_delete = True
    elif filename == "careers.html" and os.path.exists(os.path.join(base_dir, "careers")):
        should_delete = True
        
    # Safety Check for specific missing folders from my previous list
    if filename in ["future-blockchain.html", "service-custom-software.html", "service-devops.html"]:
        # I did NOT create folders for these in previous turn. 
        # I must NOT delete them yet, or convert them.
        # Let's SKIP them for deletion now.
        print(f"Skipping {filename} - No directory replacement found.")
        continue

    if should_delete and os.path.exists(file_path):
        os.remove(file_path)
        print(f"Deleted duplicate: {filename}")
        deleted_count += 1
    elif not os.path.exists(file_path):
        print(f"File not found (already gone): {filename}")
    else:
        print(f"SKIPPED {filename}: Folder {folder_name} does not exist! Keeping file.")

print(f"Total deleted: {deleted_count}")
