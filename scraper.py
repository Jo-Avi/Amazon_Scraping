from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import random


def scrape_amazon(search_term, max_pages=3):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    base_url = f"https://www.amazon.in/s?k={search_term.replace(' ', '+')}"
    results = []

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

    driver.quit()
    return results
