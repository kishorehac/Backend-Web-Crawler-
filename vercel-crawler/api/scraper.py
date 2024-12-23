import json
from playwright.async_api import async_playwright
from aiohttp import web

# Fetch dynamic content asynchronously using Playwright
async def fetch_dynamic_content(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto(url)
            # Wait for a specific element to load (adjust the selector as needed)
            await page.wait_for_selector('body', timeout=10000)  # Wait for body to load
            content = await page.content()
            await browser.close()
            return content
        except Exception as e:
            await browser.close()
            raise Exception(f"Error during Playwright content fetch: {e}")

# Vercel handler function
async def handler(request):
    # Extract URL from query parameters
    url = request.query.get('url', '')
    if not url:
        return web.Response(text='No URL provided', status=400)

    print(f"Received URL: {url}")  # Log the received URL

    try:
        # Fetch content asynchronously
        html = await fetch_dynamic_content(url)
        return web.Response(text=json.dumps({'content': html}), content_type='application/json')
    except Exception as e:
        # Return error response if something goes wrong
        error_message = str(e)
        print(f"Error: {error_message}")  # Log the error
        return web.Response(text=json.dumps({'error': error_message}), status=500, content_type='application/json')

# No need to manually start the server. Vercel will invoke the handler.
app = web.Application()
app.router.add_get('/api/scraper', handler)


