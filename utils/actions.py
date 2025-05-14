import asyncio # Make sure asyncio is imported if you use iscoroutinefunction
from pathlib import Path
from browser_use import ActionResult
# If BrowserContext needs to be imported for type hinting, ensure the path is correct
# from browser_use.browser.context import BrowserContext

async def _get_actual_playwright_page(browser_context):
    """
    Helper function to try and retrieve the actual Playwright Page object
    from the browser_use BrowserContext.
    """
    """
    Helper function to try and retrieve the actual Playwright Page object
    from the browser_use BrowserContext.
    This simplified version tries common Playwright access patterns.
    """
    # Type hint for clarity, assuming browser_context might be a Playwright BrowserContext or Page
    # from playwright.async_api import Page, BrowserContext as PlaywrightBrowserContext

    # Case 0: Check for a browser-use specific method like 'get_current_page()' or 'get_page()'
    # This is speculative, based on common library patterns.
    for method_name in ['get_current_page', 'get_page', 'page', 'active_page']:
        if hasattr(browser_context, method_name):
            try:
                attr = getattr(browser_context, method_name)
                page_candidate = None
                if callable(attr):
                    page_candidate = await attr() if asyncio.iscoroutinefunction(attr) else attr()
                else:
                    page_candidate = attr
                
                if hasattr(page_candidate, 'locator') and hasattr(page_candidate, 'set_input_files'):
                    print(f"[DEBUG] Retrieved page using browser_context.{method_name}.")
                    return page_candidate
            except Exception as e:
                print(f"[WARN] Error calling or using browser_context.{method_name}: {e}")

    # Case 1: browser_context itself is already a Playwright Page
    if hasattr(browser_context, 'locator') and hasattr(browser_context, 'set_input_files'):
        print(f"[DEBUG] Assuming browser_context (type: {type(browser_context)}) is a Playwright Page.")
        return browser_context

    # Case 2: browser_context is a Playwright BrowserContext, try to get its pages
    if hasattr(browser_context, 'pages'):
        try:
            pages_list = browser_context.pages
            if callable(pages_list): # If .pages is a method
                 pages_list = await pages_list() if asyncio.iscoroutinefunction(pages_list) else pages_list()

            if isinstance(pages_list, list) and pages_list:
                # Iterate from the last page to find the first valid one (most likely active)
                for i in range(len(pages_list) - 1, -1, -1):
                    potential_page = pages_list[i]
                    if hasattr(potential_page, 'locator') and hasattr(potential_page, 'set_input_files'):
                        print(f"[DEBUG] Retrieved page using browser_context.pages (index {i}).")
                        return potential_page
                print(f"[WARN] 'browser_context.pages' list is empty or contains no valid Playwright Pages.")
            elif hasattr(pages_list, 'locator'): # If .pages itself was the page object (less common for a list name)
                 print(f"[DEBUG] Retrieved page using browser_context.pages as a direct page object.")
                 return pages_list

        except Exception as e:
            print(f"[WARN] Error accessing or using browser_context.pages: {e}")
    
    # Case 3: Try browser_context.active_page (specific to browser-use perhaps)
    if hasattr(browser_context, 'active_page'):
        try:
            active_page_attr = browser_context.active_page
            page_object = None
            if callable(active_page_attr):
                page_object = await active_page_attr() if asyncio.iscoroutinefunction(active_page_attr) else active_page_attr()
            else:
                page_object = active_page_attr
            
            if hasattr(page_object, 'locator') and hasattr(page_object, 'set_input_files'):
                print(f"[DEBUG] Retrieved page using browser_context.active_page.")
                return page_object
        except Exception as e:
            print(f"[WARN] Error accessing browser_context.active_page: {e}")

    print(f"[ERROR] CRITICAL: Simplified _get_actual_playwright_page could not retrieve a valid Playwright Page object from BrowserContext (type: {type(browser_context)}).")
    return None


async def upload_resume_rippling(browser, file_path: str): # 'browser' is BrowserContext
    path = str((Path.cwd() / file_path).absolute())
    if not Path(path).exists():
        return ActionResult(error=f"Resume file not found at {path}")

    actual_playwright_page = await _get_actual_playwright_page(browser)

    if actual_playwright_page is None:
        return ActionResult(error="Failed to get Playwright Page from BrowserContext for resume upload.")

    try:
        await actual_playwright_page.screenshot(path="debug_rippling_resume_before_locate.png", full_page=True)

        resume_locator = actual_playwright_page.locator('[data-testid="input-resume"]')
        try:
            await resume_locator.wait_for(state="attached", timeout=15000)
        except Exception as e_wait:
            await actual_playwright_page.screenshot(path="debug_rippling_resume_wait_failed.png", full_page=True)
            return ActionResult(error=f"Timeout or error waiting for resume input [data-testid='input-resume']: {str(e_wait)}")

        await resume_locator.set_input_files(path, timeout=10000)
        await actual_playwright_page.screenshot(path="debug_rippling_resume_after_upload_attempt.png", full_page=True)

        return ActionResult(extracted_content="Resume uploaded using Rippling selector.")
    except Exception as e:
        error_message = f"General error during resume upload: {str(e)}"
        # Check if actual_playwright_page is not None before trying to screenshot
        if actual_playwright_page and hasattr(actual_playwright_page, 'screenshot'):
             await actual_playwright_page.screenshot(path="debug_rippling_resume_general_error.png", full_page=True)
        return ActionResult(error=f"Error uploading resume: {error_message}")


async def upload_cover_letter_rippling(browser, file_path: str): # 'browser' is BrowserContext
    path = str((Path.cwd() / file_path).absolute())

    if not Path(path).exists():
        return ActionResult(error=f"Cover letter file not found at {path}")

    actual_playwright_page = await _get_actual_playwright_page(browser)

    if actual_playwright_page is None:
        return ActionResult(error="Failed to get Playwright Page from BrowserContext for cover letter upload.")

    try:
        await actual_playwright_page.screenshot(path="debug_rippling_cover_before_locate.png", full_page=True)

        cover_letter_locator = actual_playwright_page.locator('[data-testid="input-cover_letter"]')
        try:
            await cover_letter_locator.wait_for(state="attached", timeout=15000)
        except Exception as e_wait:
            await actual_playwright_page.screenshot(path="debug_rippling_cover_wait_failed.png", full_page=True)
            return ActionResult(error=f"Timeout or error waiting for cover letter input [data-testid='input-cover_letter']: {str(e_wait)}")

        await cover_letter_locator.set_input_files(path, timeout=10000)
        await actual_playwright_page.screenshot(path="debug_rippling_cover_after_upload_attempt.png", full_page=True)

        return ActionResult(extracted_content="Cover letter uploaded using Rippling selector.")
    except Exception as e:
        error_message = f"General error during cover letter upload: {str(e)}"
        if actual_playwright_page and hasattr(actual_playwright_page, 'screenshot'):
             await actual_playwright_page.screenshot(path="debug_rippling_cover_general_error.png", full_page=True)
        return ActionResult(error=f"Error uploading cover letter: {error_message}")
