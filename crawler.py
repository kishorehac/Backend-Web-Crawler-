import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import random
from playwright.async_api import async_playwright

# Fetch dynamic content for JavaScript-rendered pages
async def fetch_dynamic_content(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, timeout=60000)

        # Handle infinite scrolling (example for 3 scrolls)
        for _ in range(3):
            await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            await page.wait_for_timeout(2000)  # Wait for content to load

        content = await page.content()
        await browser.close()
        return content

# Fetch links from a webpage
async def fetch_links(session, url, visited):
    headers = {
        'User-Agent': random.choice([
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0',
        ]),
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
    }

    try:
        async with session.get(url, headers=headers, timeout=10) as response:
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                links = set()
                for a_tag in soup.find_all('a', href=True):
                    href = a_tag['href']
                    full_url = urljoin(url, href)
                    if full_url not in visited and urlparse(full_url).netloc == urlparse(url).netloc:
                        links.add(full_url)
                return links
            else:
                print(f"Failed to fetch {url}: Status Code {response.status}")
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return set()

# Crawl a domain for product links
async def crawl_domain(session, domain, visited, data):
    print(f"Visiting: {domain}")
    links = []
    try:
        response = await fetch_dynamic_content(domain)
        if response:
            soup = BeautifulSoup(response, 'html.parser')
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                full_url = urljoin(domain, href)
                if any(pattern in href for pattern in ['/dp/', '/itm/', '/product/', '/p/', '/prod/', '?id=', 'sku=']):
                    links.append(full_url)
            print(f"Found {len(links)} product links on {domain}")
        else:
            print(f"No valid content on {domain}")
        data[domain] = list(set(links))
    except Exception as e:
        print(f"Error while processing {domain}: {str(e)}")

# Main function to handle multiple domains
async def main(domains):
    visited = set()
    data = {}

    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [crawl_domain(session, domain, visited, data) for domain in domains]
        await asyncio.gather(*tasks)

    with open('ecommerce_product_urls.json', 'w') as f:
        json.dump(data, f, indent=2)
    print("Data saved to ecommerce_product_urls.json")

if __name__ == "__main__":
    domains = [
        'https://www.amazon.com',
        'https://www.ebay.com',
        'https://www.walmart.com',
        'https://www.target.com',
        'https://www.bestbuy.com',
        'https://www.flipkart.com',
        'https://www.alibaba.com',
        'https://www.newegg.com',
        'https://www.etsy.com',
        'https://www.myntra.com'
    ]
    asyncio.run(main(domains))
