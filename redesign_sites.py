import os
from bs4 import BeautifulSoup

ROOT_DIR = "sites"

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title} - DAEA</title>
    
    <!-- Tailwind CSS -->
    <link href="{depth}css/output.css" rel="stylesheet">
</head>
<body class="bg-gray-50 text-gray-800 font-sans antialiased">

    <!-- Navbar -->
    <div id="central-nav"></div>

    <!-- Hero Section -->
    <header class="bg-blue-900 text-white py-24 mb-12 shadow-xl relative overflow-hidden">
        <div class="absolute inset-0 bg-black/30 z-0"></div>
        <div class="container mx-auto px-4 relative z-10 text-center">
            <h1 class="text-5xl md:text-6xl font-extrabold mb-4 tracking-tight drop-shadow-md">{title}</h1>
            <p class="text-2xl text-blue-100 mb-6 font-light tracking-wide">{subtitle}</p>
            <div class="inline-block bg-white/10 backdrop-blur-sm px-4 py-2 rounded-full border border-white/20">
                <p class="text-sm uppercase tracking-widest text-blue-50 font-semibold">{author}</p>
            </div>
        </div>
    </header>

    <!-- Main Content -->
    <div class="container mx-auto px-4 mb-24">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-12">
            <!-- Left Column: Content -->
            <div class="lg:col-span-8">
                <div class="bg-white rounded-3xl shadow-xl p-8 md:p-12 prose prose-lg max-w-none text-gray-700 leading-relaxed">
                    {content}
                </div>
            </div>
            
            <!-- Right Column: Quick Facts / Sidebar -->
            <div class="lg:col-span-4 space-y-8">
                <div class="bg-white rounded-3xl shadow-xl overflow-hidden border border-gray-100">
                    <div class="bg-gradient-to-r from-gray-50 to-white px-8 py-6 border-b border-gray-100">
                        <h5 class="font-bold text-gray-800 uppercase tracking-wider text-sm flex items-center">
                            <span class="w-2 h-2 bg-blue-500 rounded-full mr-3"></span>
                            Quick Facts
                        </h5>
                    </div>
                    <div class="p-8">
                        <ul class="space-y-6">
                            <li class="flex flex-col group">
                                <span class="text-gray-400 text-xs uppercase font-bold tracking-wider mb-1 group-hover:text-blue-500 transition-colors">Period</span>
                                <span class="font-medium text-gray-900 text-lg">{subtitle}</span>
                            </li>
                            <!-- Placeholder for more facts if we could extract them -->
                        </ul>
                    </div>
                </div>
                
                <div class="bg-gradient-to-br from-blue-600 to-blue-800 rounded-3xl shadow-xl p-8 text-white relative overflow-hidden group">
                    <div class="absolute top-0 right-0 -mt-4 -mr-4 w-24 h-24 bg-white/10 rounded-full blur-xl group-hover:bg-white/20 transition-all duration-500"></div>
                    <h5 class="font-bold text-2xl mb-3 relative z-10">Explore More</h5>
                    <p class="text-blue-100 mb-8 relative z-10">View this site on the interactive map to see its location and surrounding context.</p>
                    <a href="{depth}index.html" class="block w-full py-4 px-6 bg-white text-blue-700 font-bold text-center rounded-xl hover:bg-blue-50 transition transform hover:-translate-y-1 shadow-lg relative z-10">
                        Back to Atlas
                    </a>
                </div>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <div id="central-foot"></div>

    <!-- Scripts -->
    <script src="{depth}centralize-nav-foot/nav-foot.js"></script>
    <script src="{depth}js/main.js"></script>
</body>
</html>"""

def process_file(filepath):
    with open(filepath, 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')

    detail = soup.find(id="detail")
    
    # Fallback for already redesigned pages
    if not detail:
        content_body = soup.find(class_="content-body")
        if content_body:
            print(f"Found .content-body in {filepath}, using fallback extraction.")
            # Create a dummy detail object to standardize processing
            detail = soup.new_tag("div")
            detail.append(content_body) # Move content into detail
            
            # Extract header info from existing header if possible
            header = soup.find("header")
            if header:
                h1 = header.find("h1")
                if h1: detail.insert(0, h1) # Prepend to detail so extraction works
                
                # Subtitle (p.lead)
                lead = header.find("p", class_="lead")
                if lead: 
                    # Convert to h3 for standard extraction
                    h3 = soup.new_tag("h3")
                    h3.string = lead.get_text()
                    detail.insert(1, h3)
                    
                # Author (p.fst-italic)
                italic = header.find("p", class_="fst-italic")
                if italic:
                    # Convert to h4 for standard extraction
                    h4 = soup.new_tag("h4")
                    h4.string = italic.get_text()
                    detail.insert(2, h4)
        else:
            print(f"Skipping {filepath}: No #detail or .content-body found")
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

    # Fix images: Tailwind responsive images
    for img in detail.find_all('img'):
        # Add Tailwind classes
        current_classes = img.get('class', [])
        new_classes = ['w-full', 'h-auto', 'rounded-2xl', 'mb-8', 'shadow-lg']
        img['class'] = list(set(current_classes + new_classes))
        
        # Remove width/height attributes to let CSS handle it
        if img.has_attr('width'): del img['width']
        if img.has_attr('height'): del img['height']
        
    # Fix figures
    for figure in detail.find_all('figure'):
        figure['class'] = figure.get('class', []) + ['w-full', 'mb-8']
        # Remove inline styles that float
        if figure.has_attr('style'): del figure['style']
        
    for figcaption in detail.find_all('figcaption'):
        figcaption['class'] = figcaption.get('class', []) + ['text-sm', 'text-gray-500', 'mt-3', 'italic', 'text-center']

    # Fix HRs
    for hr in detail.find_all('hr'):
        hr['class'] = hr.get('class', []) + ['my-10', 'border-gray-100']

    # Fix Headers in content
    for h in detail.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        h['class'] = h.get('class', []) + ['font-bold', 'text-gray-900', 'mt-10', 'mb-6']
        if h.name == 'h3': h['class'].append('text-2xl')

    content = detail.decode_contents()

    # Calculate depth
    rel_path = os.path.relpath(filepath, ".")
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
            if file.endswith(".html") and "aa-template" not in root:
                process_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
