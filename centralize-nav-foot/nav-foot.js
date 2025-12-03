document.addEventListener('DOMContentLoaded', () => {
    // Calculate depth relative to root
    // We assume the site root is where index.html is.
    // If we are in /sites/subdir/file.html, we need ../../
    // If we are in /sites/file.html, we need ../
    // If we are in /index.html, we need ./ (or empty)

    // Simple heuristic: count slashes after the domain/port
    // But this depends on where the site is hosted (e.g. localhost:8000/ vs localhost:8000/daea/)
    // Better: use the script tag src to find the relative path to the script itself?
    // The script is at [prefix]centralize-nav-foot/nav-foot.js

    const scripts = document.getElementsByTagName('script');
    let scriptSrc = "";
    for (let i = 0; i < scripts.length; i++) {
        if (scripts[i].src && scripts[i].src.includes("nav-foot.js")) {
            scriptSrc = scripts[i].getAttribute("src");
            break;
        }
    }

    const prefix = scriptSrc.replace("centralize-nav-foot/nav-foot.js", "");
    const navPath = prefix + "centralize-nav-foot/navbar.html";
    const footPath = prefix + "centralize-nav-foot/footer.html";

    // Helper to load HTML
    const loadHtml = async (elementId, path) => {
        try {
            const response = await fetch(path);
            if (!response.ok) throw new Error(`Failed to load ${path}`);
            const html = await response.text();
            const element = document.getElementById(elementId);
            if (element) {
                element.innerHTML = html;

                // Fix links/images if needed
                if (prefix) {
                    const links = element.querySelectorAll("a");
                    links.forEach(link => {
                        const href = link.getAttribute("href");
                        if (href && !href.startsWith("http") && !href.startsWith("#") && !href.startsWith("mailto:")) {
                            link.setAttribute("href", prefix + href);
                        }
                    });

                    const images = element.querySelectorAll("img");
                    images.forEach(img => {
                        const src = img.getAttribute("src");
                        if (src && !src.startsWith("http")) {
                            img.setAttribute("src", prefix + src);
                        }
                    });
                }
            }
        } catch (error) {
            console.error(error);
        }
    };

    loadHtml("central-nav", navPath);
    loadHtml("central-foot", footPath);
});
