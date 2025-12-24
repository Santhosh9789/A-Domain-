
import re

file_path = "f:/vs code project/Domain-main (3)/Domain-main/blog/index.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Function to add Read More link back
def add_read_more(text_snippet, link_slug):
    # This regex finds the paragraph containing the text snippet and appends the link if not present
    pattern = re.escape(text_snippet) + r"(?!\s*<a)(.*?</div>)"
    replacement = text_snippet + r'\n                                        <a href="../' + link_slug + r'/" class="read-more mt-3">Read More <i class="bi bi-arrow-right"></i></a>\1'
    return re.sub(pattern, replacement, content, flags=re.DOTALL)

# Re-adding links based on unique text content in the paragraphs

# 1. Services
content = content.replace(
    'internal tools to customer-facing platforms.\n                                        </p>',
    'internal tools to customer-facing platforms.\n                                        </p>\n                                        <a href="../service-web-app/" class="read-more mt-3">Read More <i class="bi bi-arrow-right"></i></a>'
)

content = content.replace(
    'providing users with a smooth and delightful experience.\n                                        </p>',
    'providing users with a smooth and delightful experience.\n                                        </p>\n                                        <a href="../service-ui-ux/" class="read-more mt-3">Read More <i class="bi bi-arrow-right"></i></a>'
)

content = content.replace(
    'smarter applications.\n                                        </p>',
    'smarter applications.\n                                        </p>\n                                        <a href="../service-ai-ml/" class="read-more mt-3">Read More <i class="bi bi-arrow-right"></i></a>'
)

# 2. Future Horizons
content = content.replace(
    'crafting worlds that blur the line between reality and digital.\n                                        </p>',
    'crafting worlds that blur the line between reality and digital.\n                                        </p>\n                                        <a href="../future-game-design/" class="read-more mt-3">Read More <i class="bi bi-arrow-right"></i></a>'
)

content = content.replace(
    'against evolving threats.</p>',
    'against evolving threats.</p>\n                                        <a href="../future-cyber-security/" class="read-more mt-3">Read More <i class="bi bi-arrow-right"></i></a>'
)

# 3. Process (Discovery, Design, Development, Launch)
# These used slightly different classes (justify-content-center)
content = content.replace(
    'goals and requirements.\n                                        </p>',
    'goals and requirements.\n                                        </p>\n                                        <a href="../process-discovery/" class="read-more justify-content-center">Read More <i class="bi bi-arrow-right"></i></a>'
)

content = content.replace(
    'engaging designs/prototypes.</p>',
    'engaging designs/prototypes.</p>\n                                        <a href="../process-design/" class="read-more justify-content-center">Read More <i class="bi bi-arrow-right"></i></a>'
)

content = content.replace(
    'clean and scalable code.</p>',
    'clean and scalable code.</p>\n                                        <a href="../process-development/" class="read-more justify-content-center">Read More <i class="bi bi-arrow-right"></i></a>'
)

content = content.replace(
    'providing ongoing support.</p>',
    'providing ongoing support.</p>\n                                        <a href="../process-launch/" class="read-more justify-content-center">Read More <i class="bi bi-arrow-right"></i></a>'
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Restored all Read More links in blog/index.html")
