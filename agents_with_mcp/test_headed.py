from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        args=['--no-sandbox', '--disable-setuid-sandbox']
    )
    page = browser.new_page()
    page.goto("https://example.com")
    print("Page title:", page.title())
    import time
    time.sleep(3)
    browser.close()
