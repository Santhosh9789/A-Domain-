import os
import re

# List of tool files to convert to folders
tools = [
    "tool-react", "tool-cloud-migration", "tool-python", "tool-docker",
    "tool-aws", "tool-nodejs", "tool-nextjs", "tool-flutter",
    "tool-mongodb", "tool-fastapi", "tool-java", "tool-dotnet", "tool-kubernetes"
]

base_dir = "f:/vs code project/Domain-main (3)/Domain-main/"

for tool in tools:
    html_file = os.path.join(base_dir, f"{tool}.html")
    folder_path = os.path.join(base_dir, tool)
    new_file_path = os.path.join(folder_path, "index.html")

    if os.path.exists(html_file):
        # Create folder
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Created folder: {tool}")

        # Read content
        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Fix relative paths (add ../ to assets, blog link, etc.)
        # Logic: If it's already ../assets, keep it (unlikely in root).
        # Convert "assets/" to "../assets/"
        # Convert "blog/" to "../blog/"
        # Convert "./" (home) to "../"
        
        content = content.replace('href="assets/', 'href="../assets/')
        content = content.replace('src="assets/', 'src="../assets/')
        content = content.replace('href="blog/', 'href="../blog/')
        content = content.replace('href="./"', 'href="../"')
        
        # Also fix any root relative links if specific ones exist
        content = content.replace('href="index.html"', 'href="../index.html"')

        # Write to new location
        with open(new_file_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        # Remove old file
        os.remove(html_file)
        print(f"Moved {tool}.html -> {tool}/index.html and updated links.")

print("Tool files migration complete!")
