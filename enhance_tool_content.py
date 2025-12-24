
import os
import re

base_dir = "f:/vs code project/Domain-main (3)/Domain-main/"
blog_path = os.path.join(base_dir, "blog/index.html")

# Map of Tool Titles to Client-Friendly Descriptions
tool_descriptions = {
    "React.js": "Builds fast, interactive user interfaces that improve user engagement and performance.",
    "Python": "The top choice for AI, data analysis, and secure backend systems development.",
    "Docker": "Ensures your app runs consistently everywhere by packaging it into secure containers.",
    "AWS": "World-leading cloud platform offering unlimited scalability and reliability for your business.",
    "Node.js": "Handles thousands of concurrent connections for fast, real-time applications.",
    "Next.js": "Optimized methodology for faster page loads and better Search Engine (SEO) ranking.",
    "Flutter": "One codebase to build beautiful native apps for both iOS and Android simultaneously.",
    "MongoDB": "Flexible database that handles massive volumes of unstructured data efficiently.",
    "FastAPI": "High-performance framework for building lightning-fast APIs for your software.",
    "Java": "The gold standard for secure, large-scale enterprise banking and business systems.",
    ".NET Core": "Microsoft's robust framework for building modern, cloud-connected applications.",
    "Cloud Migration Tools": "Seamlessly move your legacy systems to the cloud with zero data loss.",
    "Kubernetes": "Automatically manages and scales your applications to handle high user traffic.",
    "Azure": "Microsoft’s enterprise-grade cloud for building and managing intelligent apps.",
    "Prometheus": "Monitors your system health 24/7 to prevent downtime before it happens.",
    "Grafana": "Visual dashboards that give you real-time insights into your business performance.",
    "GCP": "Run your applications on the same powerful infrastructure that Google uses.",
    "Jenkins": "Automates software delivery, ensuring new features reach your users faster.",
    "Terraform": "Automates infrastructure setup, reducing manual errors and deployment time.",
    "Figma": "Collaborative design tool that lets you visualize the product before we build it.",
    "Adobe XD": "Prototyping tool to test and refine user experiences early in the process.",
    "Selenium": "Automated testing framework that ensures your web app is bug-free and stable.",
    "Jest": "Ensures your JavaScript code is reliable and functions exactly as expected.",
    "TensorFlow": "Google's AI library for building smart applications that learn and adapt.",
    "PyTorch": "Facebook's AI framework for powering deep learning and complex research.",
    "n8n": "Connects your favorite apps to automate workflows without expensive developers.",
    "Zapier": "Instantly connects thousands of apps to automate your daily business tasks.",
    "Make": "Visual automation platform to streamline complex business processes effortlessly.",
}

with open(blog_path, "r", encoding="utf-8") as f:
    content = f.read()

# We need a regex that matches:
# <h4>Title</h4>
# <p class="small text-muted mb-2">Tagline</p>
# AND INJECTS description after the <p>

count = 0

for title, description in tool_descriptions.items():
    # Regex to find the specific card content
    # Note: Regex allows for some whitespace variations
    # We look for the Title tag, then capture the Tagline paragraph
    
    # Escape special regex chars in title (like .)
    safe_title = re.escape(title)
    
    pattern = rf'(<h4>{safe_title}</h4>\s*<p class="small text-muted mb-2">[^<]+</p>)'
    
    # New content adds a hidden/small description that helps clients
    # Using a slightly different style to distinguish it
    replacement_text = f'\\1\n                                        <p class="tool-desc small text-dark mt-2" style="font-size: 0.85rem; line-height: 1.4;">{description}</p>'
    
    # Perform substitution
    new_content = re.sub(pattern, replacement_text, content, count=1)
    
    if new_content != content:
        content = new_content
        count += 1
        print(f"Updated: {title}")
    else:
        print(f"Skipped (Not found): {title}")

if count > 0:
    with open(blog_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Successfully updated {count} tool cards with descriptions.")
else:
    print("No updates made.")
