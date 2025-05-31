import requests # Import the requests library
from bs4 import BeautifulSoup
import time
import random



def scrape_amazon(search_term, max_products=25, max_pages=10):
    

    base_url = f"https://www.amazon.in/s?k={search_term.replace(' ', '+')}"
    results = []

    # Remove try/finally block related to driver management
    # try:
    for page in range(1, max_pages + 1):
        url = base_url + f"&page={page}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        } # Add a User-Agent header to mimic a browser
        
        print(f"Fetching page {page}: {url}") # Added for debugging
        response = requests.get(url, headers=headers) # Use requests to fetch the page
        
        if response.status_code != 200:
            print(f"Failed to fetch page {page}. Status code: {response.status_code}")
            continue # Skip to the next page if fetching fails

        time.sleep(random.uniform(3, 6))  # delay between requests

        soup = BeautifulSoup(response.content, "html.parser") # Parse response content
        products = soup.select('div.s-main-slot div[data-component-type="s-search-result"]')

        for product in products:
            if len(results) >= max_products: # Check if we have enough products
                print(f"Scraped {max_products} products, stopping.")
                break # Stop collecting products
            try:
                link_tag = product.select_one('a.a-link-normal.s-link-style.a-text-normal')
                name_tag = link_tag.select_one('h2 span') if link_tag else None
                price_tag = product.select_one('span.a-price-whole')
                image_tag = product.select_one('img.s-image')
                rating_tag = product.select_one('span.a-icon-alt')

                results.append({
                    'name': name_tag.text.strip() if name_tag else 'N/A',
                    'price': price_tag.text.strip() if price_tag else 'N/A',
                    'link': "https://www.amazon.in" + link_tag['href'] if link_tag and link_tag['href'].startswith('/') else (link_tag['href'] if link_tag else '#'), # Handle relative/absolute links
                    'image': image_tag['src'] if image_tag else '',
                    'rating': rating_tag.text.strip() if rating_tag else 'No rating',
                })
            except Exception as e:
                print(f"Skipping a product due to error: {e}")

        # Optional: Add delay between pages
        time.sleep(random.uniform(2, 4))

        if len(results) >= max_products: # Check again after processing the page
            print(f"Reached {max_products} products after processing page {page}.")
            break # Stop fetching pages

    # Remove driver quit
    # finally:
        # pass
        
    return results
