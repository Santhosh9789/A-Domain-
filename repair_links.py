
import os
import re

ROOT_DIR = r"f:/vs code project/Domain-main (3)/Domain-main"

# Map of 'Damaged Suffix' -> 'Correct Name'
# Derived from manual analysis of "Strip 5 chars from end of relative link"
# We assume the link structure matches what was in the file (e.g. "../tool-java.html" became "../tool")

# Unique Repairs (Global Replace)
# We can be aggressive with these if the string is unique enough.
unique_repairs = {
    'tool-kuber': 'tool-kubernetes',
    'tool-prome': 'tool-prometheus',
    'tool-tenso': 'tool-tensorflow',
    'tool-terr': 'tool-terraform',
    'tool-sel': 'tool-selenium',
    'tool-ado': 'tool-adobe-xd',
    'tool-py': 'tool-pytorch',
    'tool-fas': 'tool-fastapi',
    'tool-gra': 'tool-grafana', # grafana (7) -> gr (2)? No. grafana (7). -5 = 2. tool-gr.
    'tool-gr': 'tool-grafana',
    'tool-fl': 'tool-flutter',
    'tool-mo': 'tool-mongodb', # mongodb (7). -5 = 2. tool-mo.
    'tool-re': 'tool-react', # react (5). -5 = 0. tool-
                             # Wait. tool-react. react is 5 chars. tool-react[:-5] is "tool-".
                             # Collision with tool-azure?
                             # azure (5). tool-azure[:-5] is "tool-".
                             # figma (5). tool-figma[:-5] is "tool-".
                             # So tool-react is also a collision!
                             
    'tool-no': 'tool-nodejs', # nodejs (6). -5 = 1. tool-n.
    'tool-ne': 'tool-nextjs', # nextjs (6). tool-n.
                              # Collision: nodejs vs nextjs. Link is "tool-n".

    'caree': 'career-bde',
    
    'blog-details-cl': 'blog-details-cloud', # cloud (5). blog-details-cloud[:-5] -> blog-details-
                                             # WAIT. blog-details-cloud (18). -5 -> blog-details- (13).
    'blog-details-so': 'blog-details-software', # software(8). blog-details-soft(17). -5 -> blog-details-soft (No)
                                                # software (8). 8-5=3. sof.
                                                # blog-details-software -> blog-details-sof
    'blog-det': 'blog-details', # blog-details (12). -5 -> blog-de (7)? 
                                # details (7). -5 = 2. de.
                                # blog-details -> blog-de.
                                # Wait, my manual calculation might be flawed.
                                # Python: "blog-details"[:-5] -> "blog-det".
                                # s(1),l(2),i(3),a(4),t(5). Yes, 'ails' is 4. 'tails' is 5.
                                # "details" ends with "tails". "de" remains.
                                # So "blog-de".
                                
    'process-disco': 'process-discovery',
    'process-devel': 'process-development',
    'process-d': 'process-design', # design (6). -5=1. d. process-d.
    'process-': 'process-launch', # launch (6). -5=1. l. process-l.
                                  # Wait. "launch" is 6 chars. l,a,u,n,c,h.
                                  # remove 5: l remains.
                                  # process-launch -> process-l.
                                  # Is there any "process-" collision? 
                                  # process-discovery -> process-disco
                                  # process-development -> process-devel
                                  # process-design -> process-d
                                  # process-launch -> process-l
                                  # So no collision on process-.
                                  
    'future-block': 'future-blockchain',
    'future-cyber-secu': 'future-cyber-security',
    'future-game-de': 'future-game-design',
    
    'service-custom-soft': 'service-custom-software',
    'service-devops': 'service-devops', # devops (6). -5=1. service-d.
                                        # Collision with process-d? No, prefix different.
    'service-web-app': 'service-web-app', # web-app (7). -5=2. service-we.
}

# Context Repairs (Ambiguous)
# (regex_pattern_for_context, target_link_value)
# We find: href="<ambiguous>" and replace with href="<target>"
# Pattern must include a lookahead or lookbehind or capturing group for the identifier.

context_repairs = [
    # tool (Java, Jest, Make)
    (r'(Java.*?href=["\']\.\./)tool(["\'])', r'\1tool-java\2'),
    (r'(Jest.*?href=["\']\.\./)tool(["\'])', r'\1tool-jest\2'),
    (r'(Make.*?href=["\']\.\./)tool(["\'])', r'\1tool-make\2'),
    
    # tool- (Azure, Figma, React)
    (r'(Azure.*?href=["\']\.\./)tool-(["\'])', r'\1tool-azure\2'),
    (r'(Figma.*?href=["\']\.\./)tool-(["\'])', r'\1tool-figma\2'),
    (r'(React.*?href=["\']\.\./)tool-(["\'])', r'\1tool-react\2'),
    
    # too (AWS, GCP, n8n)
    (r'(AWS.*?href=["\']\.\./)too(["\'])', r'\1tool-aws\2'),
    (r'(GCP.*?href=["\']\.\./)too(["\'])', r'\1tool-gcp\2'),
    (r'(Google.*?href=["\']\.\./)too(["\'])', r'\1tool-gcp\2'),
    (r'(n8n.*?href=["\']\.\./)too(["\'])', r'\1tool-n8n\2'),
    
    # tool-d (Docker, Dotnet)
    (r'(Docker.*?href=["\']\.\./)tool-d(["\'])', r'\1tool-docker\2'),
    (r'(\.NET.*?href=["\']\.\./)tool-d(["\'])', r'\1tool-dotnet\2'),
    
    # tool-n (Node, Next)
    (r'(Node.*?href=["\']\.\./)tool-n(["\'])', r'\1tool-nodejs\2'),
    (r'(Next.*?href=["\']\.\./)tool-n(["\'])', r'\1tool-nextjs\2'),
    
    # service- (Ai/ML, UI/UX)
    # ai-ml (5) -> -5=0. service-
    # ui-ux (5) -> -5=0. service-
    (r'(AI.*?href=["\']\.\./)service-(["\'])', r'\1service-ai-ml\2'),
    (r'(Machine.*?href=["\']\.\./)service-(["\'])', r'\1service-ai-ml\2'),
    (r'(UI.*?href=["\']\.\./)service-(["\'])', r'\1service-ui-ux\2'),
    (r'(Design.*?href=["\']\.\./)service-(["\'])', r'\1service-ui-ux\2'),
]

# Simple replacements for exact matches found in unique_repairs keys
# (Since the damaged strings are partials, we must match them exactly to avoid partial replacements of correct words if any)
# But wait, "tool-kuber" is unique enough.

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content
    
    # Apply Context Repairs first (more specific)
    for pattern, repl in context_repairs:
        # These regexes assume text precedes href. 
        # If text follows href, we need another regex.
        # href="tool" ... Java
        # (href=["']\.\./)tool(["'].*?Java)
        # We try both directions.
        
        # Direction 1: Text ... Href
        new_content = re.sub(pattern, repl, new_content, flags=re.DOTALL | re.IGNORECASE)
        
        # Direction 2: Href ... Text (e.g. icon before text, but anchor around both? or anchor before text?)
        # Pattern: (href=["']\.\./)ambiguous(["'].*?Identifier)
        # Note: the group indices change.
        # Let's construct reverse regex from the logic:
        # pattern was (Context)(Prefix)(Ambiguous)(Suffix) -> \1\2Target\3
        # We need (Prefix)(Ambiguous)(Suffix)(Context) -> \1Target\2\3
        
        # Extract keywords from the original pattern roughly
        # This is hard to automate purely. I'll just add manual reverse patterns if needed.
        pass

    # Apply Unique Repairs
    for damaged, target in unique_repairs.items():
        # precise match for href="../damaged" or href="damaged"
        # We match href=(['"])(.*?/)?damaged(['"])
        
        def replacer(match):
            quote1 = match.group(1)
            prefix = match.group(2) or ""
            quote2 = match.group(3)
            return f'href={quote1}{prefix}{target}{quote2}'
            
        # Regex to find the damaged link ending
        # e.g. href="../tool-kuber"
        safe_damaged = re.escape(damaged)
        pattern = re.compile(r'href=(["\'])(.*?/)?' + safe_damaged + r'(["\'])')
        new_content = pattern.sub(replacer, new_content)
        
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Repaired: {file_path}")

# Add Reverse Context Repairs explicitly
reverse_context_repairs = [
    # tool (Java, Jest, Make)
    (r'(href=["\']\.\./)tool(["\'].*?Java)', r'\1tool-java\2'),
    (r'(href=["\']\.\./)tool(["\'].*?Jest)', r'\1tool-jest\2'),
    (r'(href=["\']\.\./)tool(["\'].*?Make)', r'\1tool-make\2'),
    
    # tool- (Azure, Figma, React)
    (r'(href=["\']\.\./)tool-(["\'].*?Azure)', r'\1tool-azure\2'),
    (r'(href=["\']\.\./)tool-(["\'].*?Figma)', r'\1tool-figma\2'),
    (r'(href=["\']\.\./)tool-(["\'].*?React)', r'\1tool-react\2'),
    
    # too (AWS, GCP, n8n)
    (r'(href=["\']\.\./)too(["\'].*?AWS)', r'\1tool-aws\2'),
    (r'(href=["\']\.\./)too(["\'].*?GCP)', r'\1tool-gcp\2'),
    (r'(href=["\']\.\./)too(["\'].*?Google)', r'\1tool-gcp\2'),
    (r'(href=["\']\.\./)too(["\'].*?n8n)', r'\1tool-n8n\2'),
    
    # tool-d (Docker, Dotnet)
    (r'(href=["\']\.\./)tool-d(["\'].*?Docker)', r'\1tool-docker\2'),
    (r'(href=["\']\.\./)tool-d(["\'].*?\.HOT)', r'\1tool-dotnet\2'), # .NET regex issues?
    (r'(href=["\']\.\./)tool-d(["\'].*?\.NET)', r'\1tool-dotnet\2'),
    
     # tool-n (Node, Next)
    (r'(href=["\']\.\./)tool-n(["\'].*?Node)', r'\1tool-nodejs\2'),
    (r'(href=["\']\.\./)tool-n(["\'].*?Next)', r'\1tool-nextjs\2'),
    
    # service-
    (r'(href=["\']\.\./)service-(["\'].*?AI)', r'\1service-ai-ml\2'),
    (r'(href=["\']\.\./)service-(["\'].*?UI)', r'\1service-ui-ux\2'),
]

# Run
for root, dirs, files in os.walk(ROOT_DIR):
    for file in files:
        if file.endswith('.html'):
            path = os.path.join(root, file)
            # We apply dictionary repairs first? No, context first.
            # But script structure above separates them. I will merge logic in loop.
            
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            nc = content
            # Apply reverse context
            for p, r in reverse_context_repairs:
                nc = re.sub(p, r, nc, flags=re.DOTALL | re.IGNORECASE)
            
            # Apply forward context
            for p, r in context_repairs:
                nc = re.sub(p, r, nc, flags=re.DOTALL | re.IGNORECASE)
                
            # Apply unique
            for damaged, target in unique_repairs.items():
                def replacer(match):
                    quote1 = match.group(1)
                    prefix = match.group(2) or ""
                    quote2 = match.group(3)
                    return f'href={quote1}{prefix}{target}{quote2}'
                safe_damaged = re.escape(damaged)
                pattern = re.compile(r'href=(["\'])(.*?/)?' + safe_damaged + r'(["\'])')
                nc = pattern.sub(replacer, nc)
            
            if nc != content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(nc)
                print(f"Fixed: {path}")

