from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from bs4 import BeautifulSoup
import time
import random


def scrape_amazon(driver, search_term, max_pages=3):
    # The driver is now passed as an argument, so we don't initialize it here
    # options = Options()
    # options.add_argument("--headless")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--disable-gpu")
    
    # # Specify the path to ChromeDriver executable (common path on Linux servers)
    # chrome_driver_path = "/usr/bin/chromedriver"
    # service = ChromeService(executable_path=chrome_driver_path)

    # driver = webdriver.Chrome(service=service, options=options)

    base_url = f"https://www.amazon.in/s?k={search_term.replace(' ', '+')}"
    results = []

    try:
        for page in range(1, max_pages + 1):
            url = base_url + f"&page={page}"
            driver.get(url)

            time.sleep(random.uniform(3, 6))  # delay to mimic human browsing

            soup = BeautifulSoup(driver.page_source, "html.parser")
            products = soup.select('div.s-main-slot div[data-component-type="s-search-result"]')

            for product in products:
                try:
                    link_tag = product.select_one('a.a-link-normal.s-link-style.a-text-normal')
                    name_tag = link_tag.select_one('h2 span') if link_tag else None
                    price_tag = product.select_one('span.a-price-whole')
                    image_tag = product.select_one('img.s-image')
                    rating_tag = product.select_one('span.a-icon-alt')

                    results.append({
                        'name': name_tag.text.strip() if name_tag else 'N/A',
                        'price': price_tag.text.strip() if price_tag else 'N/A',
                        'link': "https://www.amazon.in" + link_tag['href'] if link_tag else '#',
                        'image': image_tag['src'] if image_tag else '',
                        'rating': rating_tag.text.strip() if rating_tag else 'No rating',
                    })
                except Exception as e:
                    print(f"Skipping a product due to error: {e}")

            # Optional: Add delay between pages
            time.sleep(random.uniform(2, 4))

    finally:
        # We don't quit the driver here as it's managed by Streamlit's singleton
        # driver.quit()
        pass # Keep the finally block but do nothing with the driver
        
    return results
