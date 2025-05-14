# uploads/rippling.py

from pathlib import Path
from browser_use import ActionResult
from uploads.shared import get_actual_playwright_page

async def upload_resume_rippling(browser, file_path: str):
    path = str((Path.cwd() / file_path).absolute())
    if not Path(path).exists():
        return ActionResult(error=f"Resume file not found at {path}")

    page = await get_actual_playwright_page(browser)
    if page is None:
        return ActionResult(error="Couldn't resolve Playwright page from browser context.")

    try:
        locator = page.locator('[data-testid="input-resume"]')
        await locator.wait_for(state="attached", timeout=15000)
        await locator.set_input_files(path, timeout=10000)
        return ActionResult(extracted_content="Resume uploaded using Rippling selector.")
    except Exception as e:
        return ActionResult(error=f"Error uploading resume: {str(e)}")


async def upload_cover_letter_rippling(browser, file_path: str):
    path = str((Path.cwd() / file_path).absolute())
    if not Path(path).exists():
        return ActionResult(error=f"Cover letter file not found at {path}")

    page = await get_actual_playwright_page(browser)
    if page is None:
        return ActionResult(error="Couldn't resolve Playwright page from browser context.")

    try:
        locator = page.locator('[data-testid="input-cover_letter"]')
        await locator.wait_for(state="attached", timeout=15000)
        await locator.set_input_files(path, timeout=10000)
        return ActionResult(extracted_content="Cover letter uploaded using Rippling selector.")
    except Exception as e:
        return ActionResult(error=f"Error uploading cover letter: {str(e)}")
