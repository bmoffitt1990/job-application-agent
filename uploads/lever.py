# uploads/lever.py

from pathlib import Path
from browser_use import ActionResult
from uploads.shared import get_actual_playwright_page

async def upload_resume_lever(browser, file_path: str):
    path = str((Path.cwd() / file_path).absolute())
    if not Path(path).exists():
        return ActionResult(error=f"Resume file not found at {path}")

    page = await get_actual_playwright_page(browser)
    if page is None:
        return ActionResult(error="Couldn't resolve Playwright page from browser context.")

    try:
        locator = page.locator('[data-qa="input-resume"]')
        await locator.wait_for(state="attached", timeout=15000)
        await locator.set_input_files(path, timeout=10000)
        return ActionResult(extracted_content="Resume uploaded using lever selector.")
    except Exception as e:
        return ActionResult(error=f"Error uploading resume: {str(e)}")


async def upload_cover_letter_lever(browser, txt_path: str, pdf_path: str):
    txt_full_path = str((Path.cwd() / txt_path).absolute())
    pdf_full_path = str((Path.cwd() / pdf_path).absolute())

    if not Path(txt_full_path).exists():
        return ActionResult(error=f"Cover letter file not found at {txt_full_path}")
    if not Path(pdf_full_path).exists():
        return ActionResult(error=f"Cover letter file not found at {pdf_full_path}")

    page = await get_actual_playwright_page(browser)
    if page is None:
        return ActionResult(error="Couldn't resolve Playwright page from browser context.")

    # Step 1: Try to paste text into Lever's textarea
    try:
        textarea = page.locator('#additional-information')
        await textarea.wait_for(state="visible", timeout=5000)

        text = Path(txt_full_path).read_text()
        await textarea.fill(text)
        return ActionResult(extracted_content="Cover letter pasted into Additional Information field.")
    except Exception as e_textarea:
        print(f"[DEBUG] Could not paste into #additional-information textarea: {e_textarea}")

    # Step 2: Fallback to uploading cover letter file
    try:
        upload_input = page.locator('[data-qa="input-cover_letter"]')
        await upload_input.wait_for(state="attached", timeout=10000)
        await upload_input.set_input_files(pdf_full_path, timeout=10000)
        return ActionResult(extracted_content="Cover letter uploaded using Lever file input.")
    except Exception as e_upload:
        return ActionResult(error=f"Both paste and upload methods failed: {e_upload}")

