import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

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

OUTPUT_DIR = 'documents'


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def fetch_and_store_documents(authority):
    print(f"Scraping {authority['name']} ({authority['country']})...")
    response = requests.get(authority['docs_page'])
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.select(authority['doc_link_selector'])

    country_dir = os.path.join(OUTPUT_DIR, authority['country'])
    ensure_dir(country_dir)

    for link in links:
        doc_url = urljoin(authority['base_url'], link['href'])
        doc_name = link['href'].split('/')[-1]
        doc_path = os.path.join(country_dir, doc_name)
        if not os.path.exists(doc_path):
            print(f"  Downloading {doc_name}...")
            doc_resp = requests.get(doc_url)
            with open(doc_path, 'wb') as f:
                f.write(doc_resp.content)
        else:
            print(f"  Skipping {doc_name}, already downloaded.")


def main():
    for authority in AUTHORITIES:
        fetch_and_store_documents(authority)

if __name__ == '__main__':
    main()