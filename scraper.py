from playwright.sync_api import sync_playwright
import time
import random

def scrape_events(city):
    """
    Scrape events from BookMyShow using Playwright.
    """
    print(f"Scraping events for {city} using Playwright...")
    events = []
    
    # Map city names to BMS URL slugs if necessary
    city_map = {
        "mumbai": "mumbai",
        "bengaluru": "bengaluru",
        "delhi-ncr": "ncr", 
        "pune": "pune"
    }
    
    city_slug = city_map.get(city.lower(), city.lower())
    url = f"https://in.bookmyshow.com/explore/events-{city_slug}"
    
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            page = context.new_page()
            
            print(f"Navigating to {url}...")
            page.goto(url, timeout=60000)
            
            # Wait for event cards to load
            try:
                page.wait_for_selector('div.sc-7o7nez-0', timeout=10000) # Common class for event cards, might change
            except:
                print("Timeout waiting for specific selector, trying generic list...")
            
            # Scroll down to load more items
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)
            
            # Select all event cards
            event_links = page.query_selector_all('a[href*="/events/"]')
            print(f"Found {len(event_links)} potential event links.")
            
            count = 0
            seen_urls = set()
            
            for link in event_links:
                if count >= 10: break # Limit to 10 events for speed
                
                href = link.get_attribute('href')
                full_url = href if href.startswith('http') else f"https://in.bookmyshow.com{href}"
                
                if full_url in seen_urls: continue
                seen_urls.add(full_url)
                
                # Extract text content from the card
                text_content = link.inner_text().split('\n')
                
                # Let's clean up text
                clean_lines = [line.strip() for line in text_content if line.strip()]
                
                if not clean_lines: continue
                
                name = clean_lines[0] if len(clean_lines) > 0 else "Unknown Event"
                category = "Event"
                venue = "Unknown Venue"
                date_str = "Upcoming"
                
                if len(clean_lines) > 1:
                    category = clean_lines[1]
                
                if len(clean_lines) > 2:
                    venue = clean_lines[-1]

                events.append({
                    "name": name,
                    "date": date_str,
                    "venue": venue,
                    "city": city,
                    "category": category,
                    "url": full_url,
                    "status": "Active"
                })
                count += 1
            
            browser.close()
            
        except Exception as e:
            print(f"Playwright Error: {e}")
            
    return events
