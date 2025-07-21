import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# Configuration: Add more authorities as needed
AUTHORITIES = [
    {
        'name': 'FAA',
        'country': 'USA',
        'base_url': 'https://www.faa.gov/regulations_policies',
        'docs_page': 'https://www.faa.gov/regulations_policies',
        'doc_link_selector': 'a[href$=".pdf"]',  # CSS selector for PDF links
    },
    # Add more authorities here
]

# Add a sample dynamic authority
AUTHORITIES.append({
    'name': 'Sample Dynamic',
    'country': 'SampleLand',
    'base_url': 'https://example-dynamic.com',
    'docs_page': 'https://example-dynamic.com/docs',
    'doc_link_selector': 'a[href$=".pdf"]',
    'dynamic': True,  # Mark as dynamic
})

OUTPUT_DIR = 'documents'


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def fetch_and_store_documents(authority):
    print(f"Scraping {authority['name']} ({authority['country']})...")
    country_dir = os.path.join(OUTPUT_DIR, authority['country'])
    ensure_dir(country_dir)
    try:
        if authority.get('dynamic'):
            # Use Selenium for dynamic sites
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            driver = webdriver.Chrome(options=options)
            driver.get(authority['docs_page'])
            time.sleep(3)  # Wait for JS to load
            links = driver.find_elements(By.CSS_SELECTOR, authority['doc_link_selector'])
            for link in links:
                doc_url = link.get_attribute('href')
                doc_name = doc_url.split('/')[-1]
                doc_path = os.path.join(country_dir, doc_name)
                if not os.path.exists(doc_path):
                    print(f"  Downloading {doc_name}...")
                    try:
                        doc_resp = requests.get(doc_url)
                        with open(doc_path, 'wb') as f:
                            f.write(doc_resp.content)
                    except Exception as e:
                        logging.error(f"Failed to download {doc_url}: {e}")
                else:
                    print(f"  Skipping {doc_name}, already downloaded.")
            driver.quit()
        else:
            # Use requests+BeautifulSoup for static sites
            response = requests.get(authority['docs_page'])
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.select(authority['doc_link_selector'])
            for link in links:
                doc_url = urljoin(authority['base_url'], link['href'])
                doc_name = link['href'].split('/')[-1]
                doc_path = os.path.join(country_dir, doc_name)
                if not os.path.exists(doc_path):
                    print(f"  Downloading {doc_name}...")
                    try:
                        doc_resp = requests.get(doc_url)
                        with open(doc_path, 'wb') as f:
                            f.write(doc_resp.content)
                    except Exception as e:
                        logging.error(f"Failed to download {doc_url}: {e}")
                else:
                    print(f"  Skipping {doc_name}, already downloaded.")
    except Exception as e:
        logging.error(f"Failed to scrape {authority['name']} ({authority['country']}): {e}")


def main():
    # Setup logging
    logging.basicConfig(filename='scraper.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

    for authority in AUTHORITIES:
        fetch_and_store_documents(authority)

if __name__ == '__main__':
    main()