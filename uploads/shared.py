# uploads/shared.py

import asyncio

async def get_actual_playwright_page(browser_context):
    """
    Tries to extract a usable Playwright Page object from a browser_use BrowserContext.
    """
    for method_name in ['get_current_page', 'get_page', 'page', 'active_page']:
        if hasattr(browser_context, method_name):
            try:
                attr = getattr(browser_context, method_name)
                page = await attr() if asyncio.iscoroutinefunction(attr) else attr()
                if hasattr(page, 'locator') and hasattr(page, 'set_input_files'):
                    print(f"[DEBUG] Got page via browser_context.{method_name}")
                    return page
            except Exception as e:
                print(f"[WARN] Error with browser_context.{method_name}: {e}")

    if hasattr(browser_context, 'locator') and hasattr(browser_context, 'set_input_files'):
        print(f"[DEBUG] Treating browser_context itself as Page.")
        return browser_context

    if hasattr(browser_context, 'pages'):
        try:
            pages = browser_context.pages
            pages = await pages() if asyncio.iscoroutinefunction(pages) else pages
            for page in reversed(pages):
                if hasattr(page, 'locator'):
                    return page
        except Exception as e:
            print(f"[WARN] Error accessing browser_context.pages: {e}")

    print(f"[ERROR] Failed to resolve Playwright Page from browser_context.")
    return None
