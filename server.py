
import http.server
import socketserver
import os
import sys

# Port logic
PORT = 8000
if len(sys.argv) > 1:
    PORT = int(sys.argv[1])

class CleanUrlHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Handle Clean URLs (extensionless)
        
        # 1. If it's a directory, let standard handler index it (e.g. /, /blog/)
        if self.path.endswith('/'):
             return super().do_GET()
        
        # 2. Translate path to local filesystem
        path = self.translate_path(self.path)
        
        # 3. If file exists as-is, serve it (e.g. styles.css, image.png)
        if os.path.exists(path):
            return super().do_GET()
            
        # 4. If file doesn't exist, try appending .html
        # e.g. /careers -> /careers/index.html
        if os.path.exists(path + ".html"):
            self.path += ".html"
            return super().do_GET()
            
        # 5. Fallback (404)
        return super().do_GET()

# Allow fast restart
socketserver.TCPServer.allow_reuse_address = True

print(f"Starting Blueidealteck Server at http://localhost:{PORT}")
print("Features: Clean URLs (no .html needed), Local Development")

with socketserver.TCPServer(("", PORT), CleanUrlHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
