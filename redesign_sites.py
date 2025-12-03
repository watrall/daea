import os
from bs4 import BeautifulSoup

ROOT_DIR = "sites"

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title} - DAEA</title>
    
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
    <!-- Custom CSS -->
    <link href="{depth}css/style.css" rel="stylesheet">
</head>
<body class="bg-light">

    <!-- Navbar -->
    <div id="central-nav"></div>

    <!-- Hero Section -->
    <header class="bg-primary text-white py-5 mb-4">
        <div class="container">
            <h1 class="display-4 fw-bold">{title}</h1>
            <p class="lead">{subtitle}</p>
            <p class="fst-italic">{author}</p>
        </div>
    </header>

    <!-- Main Content -->
    <div class="container mb-5">
        <div class="row">
            <!-- Left Column: Content -->
            <div class="col-lg-8">
                <div class="card shadow-sm">
                    <div class="card-body content-body">
                        {content}
                    </div>
                </div>
            </div>
            
            <!-- Right Column: Quick Facts / Sidebar -->
            <div class="col-lg-4">
                <div class="card shadow-sm mb-4">
                    <div class="card-header bg-secondary text-white">
                        <h5 class="card-title mb-0">Quick Facts</h5>
                    </div>
                    <div class="card-body">
                        <ul class="list-unstyled">
                            <li><strong>Period:</strong> {subtitle}</li>
                            <!-- Placeholder for more facts if we could extract them -->
                        </ul>
                    </div>
                </div>
                
                <div class="card shadow-sm">
                    <div class="card-body">
                        <h5 class="card-title">Explore More</h5>
                        <p class="card-text">View this site on the interactive map.</p>
                        <a href="{depth}index.html" class="btn btn-outline-primary w-100">Back to Atlas</a>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <div id="central-foot"></div>

    <!-- Scripts -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>
    <script src="{depth}centralize-nav-foot/nav-foot.js"></script>
    <script src="{depth}js/main.js"></script>
</body>
</html>"""

def process_file(filepath):
    with open(filepath, 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')

    detail = soup.find(id="detail")
    if not detail:
        print(f"Skipping {filepath}: No #detail found")
        return

    # Extract Title (h1)
    h1 = detail.find('h1')
    title = h1.get_text(strip=True) if h1 else "Unknown Site"
    if h1: h1.decompose()

    # Extract Subtitle (first h3 usually)
    h3 = detail.find('h3')
    subtitle = h3.get_text(strip=True) if h3 else ""
    if h3: h3.decompose()

    # Extract Author (h4)
    h4 = detail.find('h4')
    author = h4.get_text(strip=True) if h4 else ""
    if h4: h4.decompose()

    # Extract Content
    # We want everything else in #detail
    # But we need to be careful not to include the removed tags
    # detail.encode_contents() might work, but we decomposed the headers.
    
    # Fix images: Bootstrap 5 responsive images
    for img in detail.find_all('img'):
        img['class'] = img.get('class', []) + ['img-fluid', 'rounded', 'mb-3']
        # Remove width/height attributes to let CSS handle it
        if img.has_attr('width'): del img['width']
        if img.has_attr('height'): del img['height']
        
    # Fix figures
    for figure in detail.find_all('figure'):
        figure['class'] = figure.get('class', []) + ['figure', 'w-100']
        # Remove inline styles that float
        if figure.has_attr('style'): del figure['style']
        
    for figcaption in detail.find_all('figcaption'):
        figcaption['class'] = figcaption.get('class', []) + ['figure-caption']

    content = detail.decode_contents()

    # Calculate depth
    # sites/file.html -> depth = "../"
    # sites/subdir/file.html -> depth = "../../"
    rel_path = os.path.relpath(filepath, ".")
    depth_count = rel_path.count(os.sep) - 1
    depth = "../" * depth_count if depth_count > 0 else "./"
    if rel_path.startswith("sites/"): # sites/ is one level deep from root
         # If file is sites/foo.html, it is 1 level from root.
         # But relpath is sites/foo.html. count(/) is 1.
         # We need ../ for sites/foo.html
         # We need ../../ for sites/subdir/foo.html
         depth = "../" * rel_path.count(os.sep)

    new_html = TEMPLATE.format(
        title=title,
        subtitle=subtitle,
        author=author,
        content=content,
        depth=depth
    )

    with open(filepath, 'w') as f:
        f.write(new_html)
    print(f"Redesigned {filepath}")

def main():
    for root, dirs, files in os.walk(ROOT_DIR):
        for file in files:
            if file.endswith(".html") and "AA-template" not in root:
                process_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
