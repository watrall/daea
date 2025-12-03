const init = () => {
    const scripts = document.getElementsByTagName('script');
    let scriptSrc = "";
    let absoluteScriptSrc = "";

    for (let i = 0; i < scripts.length; i++) {
        if (scripts[i].src && scripts[i].src.includes("nav-foot.js")) {
            scriptSrc = scripts[i].getAttribute("src");
            absoluteScriptSrc = scripts[i].src;
            break;
        }
    }

    const prefix = scriptSrc ? scriptSrc.replace("centralize-nav-foot/nav-foot.js", "") : "";
    console.log("nav-foot.js loaded.");
    console.log("Relative Script src:", scriptSrc);
    console.log("Absolute Script src:", absoluteScriptSrc);
    console.log("Calculated prefix:", prefix);

    // Use absolute paths for fetching to avoid relative path ambiguity
    // We assume navbar.html and footer.html are in the same directory as this script
    const scriptUrl = new URL(absoluteScriptSrc);
    const timestamp = new Date().getTime();
    const navUrl = new URL(`navbar.html?v=${timestamp}`, scriptUrl).href;
    const footUrl = new URL(`footer.html?v=${timestamp}`, scriptUrl).href;

    // Helper to load HTML
    const loadHtml = async (elementId, url) => {
        try {
            console.log(`Fetching ${url} for #${elementId}...`);
            const response = await fetch(url);
            if (!response.ok) throw new Error(`Failed to load ${url}: ${response.status} ${response.statusText}`);
            const html = await response.text();
            const element = document.getElementById(elementId);
            if (element) {
                element.innerHTML = html;
                console.log(`Injected content into #${elementId}`);

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
            } else {
                console.error(`Element #${elementId} not found!`);
            }
        } catch (error) {
            console.error("Error in loadHtml:", error);
        }
    };

    loadHtml("central-nav", navUrl);
    loadHtml("central-foot", footUrl);
};

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
