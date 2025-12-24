
import os
import datetime

ROOT_DIR = r"f:/vs code project/Domain-main (3)/Domain-main"
BASE_URL = "https://blueidealteck.com"

# Exclude these files from sitemap
EXCLUDE_FILES = {
    '404.html',
    'google301f85c669284430.html',
    'privacy-policy.html', # Usually included, but if user wants "top" ranking, maybe focus on content? No, include them for trust.
    'terms-conditions.html',
    # 'index.html' is handled specially as root
}

# Directories to exclude
EXCLUDE_DIRS = {
    'assets', '.github', '.git', '__pycache__', 'forms', 'vendor'
}

def generate_sitemap():
    urls = []
    
    # Walk the directory
    for root, dirs, files in os.walk(ROOT_DIR):
        # Filter directories in place
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for file in files:
            if file.endswith('.html'):
                if file in EXCLUDE_FILES:
                    continue
                
                # Calculate relative path
                rel_path = os.path.relpath(os.path.join(root, file), ROOT_DIR)
                
                # Convert to standard URL format
                # Replace backslashes with forward slashes
                rel_path = rel_path.replace('\\', '/')
                
                # Handle Extensions and Index
                if rel_path == "index.html":
                    # Root
                    final_url = BASE_URL + "/"
                    priority = "1.0"
                elif rel_path.endswith("/index.html"):
                    # Subdirectory root (e.g. blog/index.html -> blog/)
                    final_url = BASE_URL + "/" + rel_path[:-10] # remove index.html, keep trailing slash
                    priority = "0.9"
                else:
                    # Regular page (e.g. contact.html -> contact)
                    # We removed .html extensions in links, so sitemap should reflect that?
                    # Ideally yes, if the server supports it (which Python server.py did).
                    # Assuming production server (Apache/Nginx) also configured for extensionless.
                    clean_name = rel_path[:-5] # remove .html
                    final_url = BASE_URL + "/" + clean_name
                    priority = "0.8"
                
                # Last Modified
                # Use current date or file mtime. For SEO "freshness", current date is okay if we are updating now.
                lastmod = datetime.date.today().isoformat()
                
                urls.append({
                    'loc': final_url,
                    'lastmod': lastmod,
                    'priority': priority
                })

    # Sort URLs for consistency
    urls.sort(key=lambda x: x['loc'])

    # Build XML
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for url in urls:
        xml_content += '  <url>\n'
        xml_content += f'    <loc>{url["loc"]}</loc>\n'
        xml_content += f'    <lastmod>{url["lastmod"]}</lastmod>\n'
        xml_content += '    <changefreq>weekly</changefreq>\n'
        xml_content += f'    <priority>{url["priority"]}</priority>\n'
        xml_content += '  </url>\n'
    
    xml_content += '</urlset>'
    
    with open(os.path.join(ROOT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(xml_content)
    
    print(f"Generated sitemap.xml with {len(urls)} URLs.")

if __name__ == "__main__":
    generate_sitemap()
