import asyncio
from playwright.async_api import async_playwright
import json
import urllib.parse

TARGET_URL = "https://resultadospreccongreso2026.registraduria.gov.co/resultados/0/0700001010005000001/0/?s=resultados-votes"

async def main():
    print(f"Iniciando sniffer en: {TARGET_URL}")
    found_endpoints = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Using the exact User-Agent from the user's instructions
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            extra_http_headers={
                "Accept": "application/json, text/plain, */*",
                "Origin": "https://resultadospreccongreso2026.registraduria.gov.co"
            },
            ignore_https_errors=True
        )
        page = await context.new_page()

        page.on("request", lambda request: check_request(request, found_endpoints))

        try:
            print("Cargando pagina (esperando red idle)...")
            await page.goto(TARGET_URL, wait_until="networkidle", timeout=20000)
            await page.wait_for_timeout(5000)
        except Exception as e:
            print(f"Error cargando la pagina: {e}")

        await browser.close()
        
        print("\n=== RESULTADOS DE LA INTERCEPCION ===")
        if not found_endpoints:
            print("No se encontraron peticiones a archivos .json o de datos.")
        else:
            print("Endpoints JSON descubiertos:")
            for ep in set(found_endpoints):
                print(f" -> {ep}")

def check_request(request, endpoints_list):
    url = request.url
    if url.endswith(('.png', '.jpg', '.jpeg', '.svg', '.css', '.woff', '.woff2', '.js')):
        return
    if '.json' in url or request.resource_type in ['fetch', 'xhr']:
        endpoints_list.append(url)
        print(f"  [XHR/Fetch] {request.method} {urllib.parse.unquote(url)}")

if __name__ == "__main__":
    asyncio.run(main())
