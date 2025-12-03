import os
import re

# Configuration
ROOT_DIR = "."
BOOTSTRAP_CSS_CDN = '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">'
BOOTSTRAP_JS_CDN = '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>'

# Class Mappings (BS3 -> BS5)
CLASS_MAP = {
    r'col-xs-(\d+)': r'col-\1',
    r'col-sm-(\d+)': r'col-sm-\1', # No change, but good to be explicit
    r'col-md-(\d+)': r'col-md-\1',
    r'col-lg-(\d+)': r'col-lg-\1',
    r'col-xs-offset-(\d+)': r'offset-\1',
    r'col-sm-offset-(\d+)': r'offset-sm-\1',
    r'col-md-offset-(\d+)': r'offset-md-\1',
    r'col-lg-offset-(\d+)': r'offset-lg-\1',
    r'pull-right': 'float-end',
    r'pull-left': 'float-start',
    r'text-right': 'text-end',
    r'text-left': 'text-start',
    r'center-block': 'mx-auto',
    r'img-responsive': 'img-fluid',
    r'panel': 'card',
    r'panel-default': '', # Cards don't need this
    r'panel-body': 'card-body',
    r'panel-heading': 'card-header',
    r'panel-title': 'card-title',
    r'btn-default': 'btn-secondary', # BS5 removed default
    r'navbar-default': 'navbar-light bg-light',
    r'navbar-nav': 'navbar-nav', # Same
    r'navbar-right': 'ms-auto',
    r'navbar-left': 'me-auto',
    r'navbar-fixed-top': 'fixed-top',
    r'navbar-toggle': 'navbar-toggler',
    r'navbar-collapse': 'collapse navbar-collapse', # Ensure collapse is there
    r'data-toggle': 'data-bs-toggle',
    r'data-target': 'data-bs-target',
    r'data-dismiss': 'data-bs-dismiss',
    r'data-parent': 'data-bs-parent',
    r'data-slide': 'data-bs-slide',
}

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    original_content = content

    # 1. Remove old CSS/JS
    # Remove Bootstrap 3 CSS (local or CDN)
    content = re.sub(r'<link[^>]*bootstrap[^>]*css[^>]*>', '', content, flags=re.IGNORECASE)
    # Remove jQuery
    content = re.sub(r'<script[^>]*jquery[^>]*></script>', '', content, flags=re.IGNORECASE)
    # Remove Bootstrap 3 JS
    content = re.sub(r'<script[^>]*bootstrap[^>]*js[^>]*></script>', '', content, flags=re.IGNORECASE)
    # Remove html5shiv/respond.js
    content = re.sub(r'<!--\[if lt IE 9\]>.*?<!\[endif\]-->', '', content, flags=re.DOTALL)

    # 2. Add Bootstrap 5 CSS (in head)
    if BOOTSTRAP_CSS_CDN not in content:
        content = content.replace('</head>', f'{BOOTSTRAP_CSS_CDN}\n</head>')

    # 3. Add Bootstrap 5 JS (at end of body)
    if BOOTSTRAP_JS_CDN not in content:
        content = content.replace('</body>', f'{BOOTSTRAP_JS_CDN}\n</body>')

    # 4. Update Classes and Attributes
    # First, simple string replacements for attributes
    content = content.replace('data-toggle=', 'data-bs-toggle=')
    content = content.replace('data-target=', 'data-bs-target=')
    content = content.replace('data-dismiss=', 'data-bs-dismiss=')
    content = content.replace('data-parent=', 'data-bs-parent=')
    content = content.replace('data-slide=', 'data-bs-slide=')

    for pattern, replacement in CLASS_MAP.items():
        if pattern.startswith('data-'): continue # Skip attributes in class loop
        # Use regex to replace classes inside class="..." attributes
        # This is tricky with regex. A simpler approach is global replace if the pattern is unique enough.
        # But "panel" might appear in text.
        # We'll try a robust regex for class attributes.
        
        def replace_class(match):
            classes = match.group(1)
            # Replace specific class in the list
            new_classes = re.sub(r'\b' + pattern + r'\b', replacement, classes)
            return f'class="{new_classes}"'

        content = re.sub(r'class="([^"]*)"', replace_class, content)

    # 5. Specific Fixes
    # Modal centering
    content = content.replace('modal-dialog', 'modal-dialog modal-dialog-centered')

    if content != original_content:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Updated {filepath}")

def main():
    # Process index.html and projects.html
    if os.path.exists("index.html"):
        process_file("index.html")
    if os.path.exists("projects.html"):
        process_file("projects.html")

    # Process sites/
    for root, dirs, files in os.walk("sites"):
        for file in files:
            if file.endswith(".html"):
                process_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
