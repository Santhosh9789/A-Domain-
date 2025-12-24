import os

DEMO_DIR = r"f:/vs code project/Domain-main (3)/Domain-main/Projects/projects"

LENIS_CDN = '<script src="https://unpkg.com/lenis@1.0.45/dist/lenis.min.js"></script>'
LENIS_INIT = """
<script>
    // Smooth scrolling for demos
    const lenis = new Lenis({
      duration: 1.2,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      direction: 'vertical',
      gestureDirection: 'vertical',
      smooth: true,
      mouseMultiplier: 0.8,
      smoothTouch: false,
      touchMultiplier: 2,
    });

    function raf(time) {
      lenis.raf(time);
      requestAnimationFrame(raf);
    }

    requestAnimationFrame(raf);
</script>
"""

def add_smooth_scroll(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if "new Lenis" in content:
            # print(f"Skipping {file_path}, already has smooth scroll.")
            return

        # Insert CDN before </head> or body
        if "</body>" in content:
            # Add CDN and Init script right before body end
            # It's safer to put script at end
            to_insert = f"{LENIS_CDN}\n{LENIS_INIT}\n"
            content = content.replace("</body>", f"{to_insert}</body>")
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Added smooth scroll to {file_path}")
        else:
            print(f"Could not find </body> in {file_path}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# Walk through the demo directory
count = 0
for root, dirs, files in os.walk(DEMO_DIR):
    for file in files:
        if file.lower().endswith(".html"):
            add_smooth_scroll(os.path.join(root, file))
            count += 1

print(f"Processed {count} demo HTML files.")
