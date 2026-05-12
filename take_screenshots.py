import os
from playwright.sync_api import sync_playwright

# Ensure we use an absolute path for local file
file_path = f"file://{os.path.abspath('index.html')}"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.set_viewport_size({"width": 1280, "height": 800})
    
    print("Loading index.html...")
    page.goto(file_path)
    
    # Wait for the content to be visible
    page.wait_for_selector('.article')
    
    # Take screenshot of the main page
    print("Capturing main page screenshot...")
    page.screenshot(path="screenshot_main.png", full_page=True)
    
    # Click the first article to open the modal
    print("Opening modal...")
    page.click('.article:nth-child(1)')
    
    # Wait for the modal content to be visible and animation to settle
    page.wait_for_selector('.modal-content')
    page.wait_for_timeout(500) # Give it half a second for any rendering/animations
    
    # Take screenshot with modal open (don't need full page here as modal is fixed)
    print("Capturing modal screenshot...")
    page.screenshot(path="screenshot_modal.png")
    
    browser.close()
    print("Screenshots captured successfully!")
