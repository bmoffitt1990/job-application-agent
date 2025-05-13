from pathlib import Path
from browser_use import ActionResult

async def upload_file(index: int, browser, file_path: str, label: str):
    path = str((Path.cwd() / file_path).absolute())

    dom_el = await browser.get_dom_element_by_index(index)
    if dom_el is None:
        return ActionResult(error=f'No element found at index {index} for {label}')

    file_upload_dom_el = dom_el.get_file_upload_element()
    if file_upload_dom_el is None:
        return ActionResult(error=f'No file upload element found at index {index} for {label}')

    file_upload_el = await browser.get_locate_element(file_upload_dom_el)
    if file_upload_el is None:
        return ActionResult(error=f'No file upload element found at index {index} for {label}')

    try:
        await file_upload_el.set_input_files(path)
        return ActionResult(extracted_content=f'Successfully uploaded {label} to index {index}')
    except Exception as e:
        return ActionResult(error=f'Failed to upload {label}: {str(e)}')
