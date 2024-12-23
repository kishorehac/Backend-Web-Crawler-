from aiohttp import web
import json
from playwright.async_api import async_playwright

async def fetch_dynamic_content(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_timeout(3000)
        content = await page.content()
        await browser.close()
        return content

async def handler(request):
    url = request.query.get('url', '')
    if not url:
        return web.Response(text='No URL provided', status=400)

    try:
        html = await fetch_dynamic_content(url)
        return web.Response(text=json.dumps({'content': html}), content_type='application/json')
    except Exception as e:
        return web.Response(text=json.dumps({'error': str(e)}), status=500, content_type='application/json')

app = web.Application()
app.router.add_get('/api/scraper', handler)

