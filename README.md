# E-commerce URL Crawler

## Project Overview
This project is a **Python-based web crawler** designed to extract product URLs from multiple e-commerce websites. The crawler leverages **aiohttp** for asynchronous HTTP requests, **Playwright** for fetching dynamically loaded content, and **BeautifulSoup** for parsing HTML.

---

## Approach
### 1. URL Discovery
- The crawler identifies product pages by matching specific URL patterns found across e-commerce websites, such as:
  - `/dp/`
  - `/itm/`
  - `/product/`
  - `/p/`
  - `/prod/`
  - Query parameters like `?id=` and `sku=`
- These patterns allow the crawler to intelligently detect product pages on various platforms.

### 2. Scalability
- The crawler supports large websites with deep link hierarchies.
- Uses **asynchronous requests (aiohttp)** to fetch multiple pages concurrently, reducing time spent on I/O operations.
- Designed for scalability to handle hundreds of domains and large datasets efficiently.

### 3. Performance
- Utilizes **asyncio** and **aiohttp** for concurrent tasks, improving speed for large-scale crawls.
- Incorporates **Playwright** to fetch dynamically loaded content rendered by JavaScript, ensuring no data is missed.

### 4. Robustness
- Handles dynamic content (e.g., infinite scroll) using **Playwright**.
- Gracefully manages edge cases such as:
  - Network errors
  - Invalid pages
  - Content rendering issues
- Flexible product URL patterns can be extended for additional e-commerce platforms.

---

## How to Run
### 1. Clone this repository:
```bash
git clone https://github.com/Kishorehack/ecommerce-url-crawler.git
```

### 2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

### 3. Run the crawler:
```bash
python crawler.py
```

- The product URLs will be saved in the **`ecommerce_product_urls.json`** file.

---

## Technologies Used
- **asyncio** - For asynchronous execution
- **aiohttp** - For non-blocking HTTP requests
- **BeautifulSoup** - For parsing HTML content
- **Playwright** - For handling dynamic content (JavaScript-rendered pages)

---

## Folder Structure
```
ecommerce-url-crawler/
├── README.md
├── crawler/
│   ├── __init__.py
│   ├── crawler.py
│   ├── utils.py
│   ├── patterns.py
├── tests/
│   ├── test_crawler.py
│   ├── test_utils.py
├── requirements.txt
├── LICENSE
└── docs/
    ├── approach.md
    ├── architecture-diagram.png
