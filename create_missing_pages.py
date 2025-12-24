
import os

# Base HTML Template (Same as tool-react/index.html)
template = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta content="width=device-width, initial-scale=1.0" name="viewport" />
    <title>{title} - Blueidealteck</title>
  <link href="../assets/img/favicon.png" rel="icon" type="image/png">
  <link href="../assets/img/apple-touch-icon.png" rel="apple-touch-icon">
    <link
      href="../assets/vendor/bootstrap/css/bootstrap.min.css"
      rel="stylesheet"
    />
    <link
      href="../assets/vendor/bootstrap-icons/bootstrap-icons.css"
      rel="stylesheet"
    />
    <link href="../assets/css/main.css" rel="stylesheet" />
  <link href="../assets/season/christmas.css" rel="stylesheet">
</head>

  <body class="starter-page-page">
    <header id="header" class="header d-flex align-items-center fixed-top">
      <div
        class="container-fluid container-xl position-relative d-flex align-items-center"
      >
        <a href="../" class="logo d-flex align-items-center me-auto">
          <h1 class="sitename">Blueidealteck</h1>
        </a>
        <nav id="navmenu" class="navmenu">
          <ul>
            <li><a href="../blog/" class="active">Blog</a></li>
          </ul>
        </nav>
      <i class="mobile-nav-toggle d-xl-none bi bi-list"></i>
      </div>
    </header>
    <main class="main">
      <section class="section container">
        <div class="row justify-content-center">
          <div class="col-lg-10">
            <h1 class="mb-4 text-center">
              <i class="{icon} {color} me-2"></i>{title}
            </h1>
            <p class="lead text-center">
              {tagline}
            </p>
            <hr class="my-5" />
            <h3>Description</h3>
            <p>
              {description}
            </p>
            <ul>
              {features}
            </ul>
          </div>
        </div>
        <div class="mt-5 text-center">
          <a
            href="../blog/"
            class="btn btn-primary px-4 py-2"
            style="background-color: var(--accent-color); border: none"
          >
            <i class="bi bi-arrow-left me-2"></i>Back to Blog
          </a>
        </div>
      </section>
    </main>
<footer id="footer" class="footer">

    <div class="container footer-top">
      <div class="row gy-4">
        <div class="col-lg-5 col-md-12 footer-about">
          <a href="/" class="logo d-flex align-items-center">
            <span class="sitename">Blueidealteck</span>
          </a>
          <div class="footer-contact pt-3">
            <p>1/11 Anna Nagar, Mangalampet</p>
            <p>Virudhachalam(tk), Cuddalore(dist), 606104.</p>
            <p class="mt-3"><strong>Phone:</strong> <span>+91 9789836077</span></p>
            <p><strong>Email:</strong> <span>info@blueidealteck.com</span></p>
          </div>
        </div>

        <div class="col-lg-3 col-md-6 footer-links">
          <h4>Useful Links</h4>
          <ul>
            <li><i class="bi bi-chevron-right"></i> <a href="/">Home</a></li>
            <li><i class="bi bi-chevron-right"></i> <a href="/#about">About us</a></li>
            <li><i class="bi bi-chevron-right"></i> <a href="/#services">Services</a></li>
            <li><i class="bi bi-chevron-right"></i> <a href="/blog/">Blogs</a></li>
            <li><i class="bi bi-chevron-right"></i> <a href="/careers/">Careers</a></li>
            <li><i class="bi bi-chevron-right"></i> <a href="/Projects/">Projects</a></li>
            <li><i class="bi bi-chevron-right"></i> <a href="/privacy-policy">Privacy Policy</a></li>
            <li><i class="bi bi-chevron-right"></i> <a href="/terms-conditions">Terms & Conditions</a></li>
          </ul>
        </div>

        <div class="col-lg-4 col-md-6 footer-links">
          <h4>Follow Us</h4>
          <div class="social-links d-flex mt-4">
            <a href="https://x.com/blueidealteck" target="_blank"><i class="bi bi-twitter-x"></i></a>
            <a href="https://www.facebook.com/profile.php?id=61576888345818" target="_blank"><i class="bi bi-facebook"></i></a>
            <a href="https://www.instagram.com/blueidealteck/" target="_blank"><i class="bi bi-instagram"></i></a>
            <a href="https://linkedin.com/in/blueidealteck-software-solutions-2259b7358" target="_blank"><i class="bi bi-linkedin"></i></a>
          </div>
        </div>

      </div>
    </div>

    <div class="container copyright text-center mt-4">
      <p>© <span>2025 Copyright</span> <strong class="px-1 sitename">Blueidealteck</strong> <span>All Rights Reserved</span></p>
    </div>

  </footer>
    <script src="../assets/vendor/bootstrap/js/bootstrap.bundle.min.js"></script>
  <script src="../assets/season/christmas.js"></script>
</body>
</html>"""

# Data for all pages
pages = [
    {
        "folder": "process-discovery",
        "title": "Discovery Phase",
        "icon": "bi-search",
        "color": "text-primary",
        "tagline": "Understanding your vision, goals, and requirements.",
        "description": "The Discovery phase is the foundation of our development process. We dive deep into your business objectives, target audience, and functional requirements to create a comprehensive roadmap for success.",
        "features": """
            <li><strong>Requirement Analysis:</strong> Gathering detailing specs and business logic.</li>
            <li><strong>Market Research:</strong> Analyzing competitors and market trends.</li>
            <li><strong>Feasibility Study:</strong> Assessing technical and operational viability.</li>
            <li><strong>Project Roadmap:</strong> Defining timelines, milestones, and deliverables.</li>
        """
    },
    {
        "folder": "process-design",
        "title": "Design Phase",
        "icon": "bi-palette",
        "color": "text-danger",
        "tagline": "Crafting intuitive and engaging user experiences.",
        "description": "Our design team transforms concepts into stunning visuals. We focus on User Experience (UX) and User Interface (UI) design to ensure your product is not only beautiful but also easy to use.",
        "features": """
            <li><strong>Wireframing:</strong> Creating structural blueprints of the application.</li>
            <li><strong>Prototyping:</strong> Building interactive mockups for feedback.</li>
            <li><strong>UI Design:</strong> designing high-fidelity screens with your brand identity.</li>
            <li><strong>UX Research:</strong> ensuring logical flow and accessibility.</li>
        """
    },
    {
        "folder": "process-development",
        "title": "Development Phase",
        "icon": "bi-code-square",
        "color": "text-success",
        "tagline": "Building robust, scalable, and secure solutions.",
        "description": "This is where the magic happens. Our developers write clean, efficient code to bring designs to life. We use modern agile methodologies to ensure rapid progress and transparency.",
        "features": """
            <li><strong>Frontend Development:</strong> Building responsive client-side interfaces.</li>
            <li><strong>Backend Development:</strong> Creating powerful server-side logic and APIs.</li>
            <li><strong>Database Integration:</strong> Ssetting up secure and optimized data storage.</li>
            <li><strong>Code Review:</strong> rigorous peer reviews to maintain code quality.</li>
        """
    },
    {
        "folder": "process-launch",
        "title": "Launch Phase",
        "icon": "bi-rocket",
        "color": "text-warning",
        "tagline": "Deploying your product to the world.",
        "description": "We ensure a smooth go-live experience. From server setup to final testing, we handle everything required to launch your application successfully and securely.",
        "features": """
            <li><strong>Deployment:</strong> Scetting up production environments (AWS, Azure, etc.).</li>
            <li><strong>Final Testing:</strong> Smoke testing and user acceptance testing (UAT).</li>
            <li><strong>Performance Tuning:</strong> Optimizing load times and server response.</li>
            <li><strong>Post-Launch Support:</strong> Monitoring and fixing immediate issues.</li>
        """
    },
    {
        "folder": "service-web-app",
        "title": "Web App Development",
        "icon": "bi-browser-chrome",
        "color": "text-info",
        "tagline": "Secure, fast, and responsive web applications.",
        "description": "We build custom web applications tailored to your business needs, from simple portals to complex enterprise resource planning (ERP) systems.",
        "features": """
            <li><strong>Custom Solutions:</strong> Tailor-made for your specific requirements.</li>
            <li><strong>Responsive Design:</strong> Works perfectly on Mobile, Tablet, and Desktop.</li>
            <li><strong>Progressive Web Apps (PWA):</strong> App-like experience in the browser.</li>
            <li><strong>High Performance:</strong> Optimized for speed and SEO.</li>
        """
    },
    {
        "folder": "service-ui-ux",
        "title": "UI/UX Design",
        "icon": "bi-pencil-square",
        "color": "text-primary",
        "tagline": "Designing products users love.",
        "description": "Great design is about solving problems. We combine aesthetics with functionality to create digital products that engage users and drive conversions.",
        "features": """
            <li><strong>User Research:</strong> Understanding user behavior and needs.</li>
            <li><strong>Interaction Design:</strong> Creating engaging animations and transitions.</li>
            <li><strong>Visual Identity:</strong> Branding and style guides.</li>
            <li><strong>Accessibility:</strong> Ensuring inclusivity for all users.</li>
        """
    },
    {
        "folder": "service-ai-ml",
        "title": "AI & Machine Learning",
        "icon": "bi-robot",
        "color": "text-success",
        "tagline": "Intelligent solutions for the future.",
        "description": "Leverage the power of Artificial Intelligence to automate processes, gain insights, and create smarter applications.",
        "features": """
            <li><strong>Predictive Analytics:</strong> Forecasting trends based on data.</li>
            <li><strong>NLP:</strong> Natural Language Processing for chatbots and text analysis.</li>
            <li><strong>Computer Vision:</strong> Image and video recognition systems.</li>
            <li><strong>Automation:</strong> Streamlining repetitive workflows.</li>
        """
    },
    {
        "folder": "future-game-design",
        "title": "Next-Gen Game Design",
        "icon": "bi-controller",
        "color": "text-danger",
        "tagline": "Immersive gaming experiences.",
        "description": "We are pushing the boundaries of interactive entertainment with cutting-edge game development technologies.",
        "features": """
            <li><strong>Unreal Engine 5:</strong> Hyper-realistic graphics and physics.</li>
            <li><strong>Unity Development:</strong> Cross-platform game creation.</li>
            <li><strong>AR/VR:</strong> Augmented and Virtual Reality experiences.</li>
            <li><strong>Metaverse:</strong> Building virtual worlds and economies.</li>
        """
    },
    {
        "folder": "future-cyber-security",
        "title": "Elite Cyber Security",
        "icon": "bi-shield-lock-fill",
        "color": "text-warning",
        "tagline": "Protecting your digital assets.",
        "description": "In an era of evolving threats, we provide military-grade security solutions to safeguard your infrastructure and data.",
        "features": """
            <li><strong>Penetration Testing:</strong> Identifying and fixing vulnerabilities.</li>
            <li><strong>Zero Trust Architecture:</strong> Never trust, always verify.</li>
            <li><strong>Security Audits:</strong> Comprehensive compliance checks.</li>
            <li><strong>Encryption:</strong> Protecting sensitive data at rest and in transit.</li>
        """
    }
]

base_dir = "f:/vs code project/Domain-main (3)/Domain-main/"

for page in pages:
    folder_path = os.path.join(base_dir, page["folder"])
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    file_path = os.path.join(folder_path, "index.html")
    
    content = template.format(
        title=page["title"],
        icon=page["icon"],
        color=page["color"],
        tagline=page["tagline"],
        description=page["description"],
        features=page["features"]
    )
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"Created: {file_path}")

print("All missing pages created successfully!")
