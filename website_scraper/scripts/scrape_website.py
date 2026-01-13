"""Fetches details of a website using Playwright. | Inputs: website_url | Outputs: page_title, page_content"""

import os
from playwright.sync_api import sync_playwright

def scrape_website(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        try:
            print(f"Navigating to {url}...")
            page.goto(url)
            page_title = page.title()
            # collecting first 1000 chars of content for brevity in demo
            page_content = page.content()[:5000] 
            print(f"Successfully scraped: {page_title}")
            return page_title, page_content
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            raise e
        finally:
            browser.close()

if __name__ == "__main__":
    try:
        # Assuming 'website_url' is injected into the global scope by the workflow runner
        # or acting as a fallback for local testing
        if 'website_url' not in globals():
            # For testing purposes if run standalone
            input_url = "https://hub8.ai"
        else:
            input_url = website_url # type: ignore

        if not input_url:
            raise ValueError("website_url variable not found")

        title, content = scrape_website(input_url)
        
        # Setting outputs
        page_title = title
        page_content = content

        print(page_title)
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise e
