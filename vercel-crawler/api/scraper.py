import json
import random
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright
from aiohttp import ClientSession

def fetch_dynamic_content(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(3000)  # Allow content to load
        content = page.content()
        browser.close()
        return content

def handler(request):
    url = request.args.get('url', '')
    if not url:
        return 'No URL provided', 400
    
    try:
        html = fetch_dynamic_content(url)
        return json.dumps({'content': html})
    except Exception as e:
        return json.dumps({'error': str(e)}), 500
