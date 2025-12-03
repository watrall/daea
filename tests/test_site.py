import pytest
from playwright.sync_api import Page, expect
import re

# Helper to get URL
def get_url(path):
    return f"http://localhost:8000/{path}"

def test_homepage_loads(page: Page):
    page.goto(get_url("index.html"))
    expect(page).to_have_title("Digital Atlas of Egyptian Archaeology")

def test_map_initializes(page: Page):
    page.goto(get_url("index.html"))
    
    # Close modal if it appears
    if page.locator("#welcome-modal").is_visible():
        page.click("#close-modal-btn")
        page.wait_for_timeout(500)

    # Wait for map to be visible
    try:
        # Check if map has initialized (Leaflet adds this class)
        expect(page.locator("#map")).to_have_class(re.compile(r"leaflet-container"))
        expect(page.locator("#map")).to_be_visible()
    except Exception:
        page.screenshot(path="map_failure.png")
        raise

def test_modal_appears_and_closes(page: Page):
    page.goto(get_url("index.html"))
    # Modal should be visible initially
    modal = page.locator("#welcome-modal")
    expect(modal).to_be_visible(timeout=5000)
    
    # Close it
    page.click("#close-modal-btn")
    expect(modal).not_to_be_visible()

def test_navigation_injection(page: Page):
    """Test that the centralized navbar is injected correctly."""
    page.goto(get_url("sites/mut-el-kharab.html"))
    
    # Check for navbar (Tailwind uses <nav>)
    nav = page.locator("nav").first
    expect(nav).to_be_visible(timeout=10000)
    
    # Check for specific link in the navbar
    expect(page.locator("nav a:has-text('Atlas')").first).to_be_visible()
    
    # Check that Projects link is GONE
    expect(page.locator("nav a:has-text('Projects')")).not_to_be_visible()

def test_typography_applied(page: Page):
    """Test that new font classes are applied."""
    page.goto(get_url("sites/mut-el-kharab.html"))
    
    # Check for font-display on headings
    expect(page.locator("h1").first).to_have_class(re.compile(r"font-display"))
    
    # Check for font-sans on body/content
    expect(page.locator("body")).to_have_class(re.compile(r"font-sans"))

def test_responsive_layout(page: Page):
    """Test that the layout adapts to mobile screens."""
    page.set_viewport_size({"width": 375, "height": 667})
    page.goto(get_url("sites/mut-el-kharab.html"))
    
    # Check for main content container
    expect(page.locator(".container").first).to_be_visible()
    
    # Check that Quick Facts is visible (it should stack)
    expect(page.locator("text=Quick Facts")).to_be_visible()

def test_resource_availability(page: Page):
    """Verify that critical resources are served correctly."""
    # Check nav-foot.js
    response = page.request.get(get_url("centralize-nav-foot/nav-foot.js"))
    expect(response).to_be_ok()
    
    # Check navbar.html
    response = page.request.get(get_url("centralize-nav-foot/navbar.html"))
    expect(response).to_be_ok()

def test_full_map_functionality(page: Page):
    """Test the full flow: Map -> Click Marker -> Side Panel -> Detail Page."""
    
    # Capture console logs
    console_logs = []
    page.on("console", lambda msg: console_logs.append(msg.text))

    try:
        page.goto(get_url("index.html"))
        
        # Close modal first
        if page.locator("#welcome-modal").is_visible():
            page.click("#close-modal-btn")
        
        # Wait for markers
        page.wait_for_selector(".leaflet-marker-icon", timeout=10000)
        
        # Click a marker (using the first one found)
        page.locator(".leaflet-marker-icon").first.click(force=True)
        
        # Check side panel opens (translate-x-0 means open)
        side_panel = page.locator("#side-panel")
        expect(side_panel).to_have_class(re.compile(r"translate-x-0"))
        
        # Check content in side panel
        expect(page.locator("#panel-title")).not_to_be_empty()
        
        # Click 'Read More'
        with page.expect_navigation():
            page.click("#panel-link")
            
        # Verify we are on the detail page
        expect(page).not_to_have_url(re.compile(r"index.html"))
        
        # Verify interface elements on the new page
        expect(page.locator("nav").first).to_be_visible(timeout=10000)
        expect(page.locator("footer")).to_be_visible(timeout=10000)
        
        # Verify new layout (Tailwind classes)
        expect(page.locator(".bg-white").first).to_be_visible()
        expect(page.locator("h1")).to_be_visible()
        
    except Exception as e:
        print("\n=== Browser Console Logs ===")
        for log in console_logs:
            print(log)
        print("============================")
        print("\n=== Page Content ===")
        print(page.content())
        print("====================")
        raise e
