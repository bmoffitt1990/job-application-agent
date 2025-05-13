import asyncio
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from pathlib import Path

from browser_use import Agent, Controller
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext
from langchain_openai import ChatOpenAI
from utils.config import load_config
from utils.actions import upload_file

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError("Missing OPENAI_API_KEY in .env")

model = ChatOpenAI(
    model="gpt-4o",  # or "gpt-3.5-turbo"
    api_key=OPENAI_API_KEY
)

# Load user config
config = load_config()

# Set up controller
controller = Controller()

# Register file upload actions
@controller.action("Upload resume to element - use this for the resume upload field")
async def upload_cv(index: int, browser: BrowserContext):
    return await upload_file(index, browser, config["resume_path"], "resume")

@controller.action("Upload cover letter to element - use this for the cover letter upload field")
async def upload_cover_letter(index: int, browser: BrowserContext):
    return await upload_file(index, browser, config["cover_letter_path"], "cover letter")


from browser_use import ActionResult

@controller.action("Extract job description text")
async def extract_job_description(browser):
    html = await browser.get_page_content()
    return ActionResult(extracted_content=html, include_in_memory=True)

browser = Browser(
    config=BrowserConfig(
        browser_binary_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        disable_security=True,
    )
)

def load_prompt(filename: str, **kwargs) -> str:
    path = Path("prompts") / filename
    if not path.exists():
        raise FileNotFoundError(f"Prompt file '{filename}' not found.")
    raw_prompt = path.read_text()
    return raw_prompt.format(**kwargs)

async def main():
    config = load_config()
    resume_path = Path.cwd() / config["resume_path"]
    cover_letter_path = Path.cwd() / config["cover_letter_path"]
    # resume_text = read_cv(resume_path)
    # cover_letter_text = read_cv(cover_letter_path)

    prompt = load_prompt(
        "apply.txt",
        resume_path=config["resume_path"],
        cover_letter_path=["cover_letter_path"],
        first_name=config["first_name"],
        last_name=config["last_name"],
        email=config["email"],
        job_url=config["job_url"],
        linkedin_link=config["linkedin_link"],
        github_link=config["github_link"],
        current_company=config["current_company"],
        location=config["location"],
        experience=config["experience"],
        education=config["education"],
        gender=config["gender"],
        age=config["age"],
        race=config["race"],
        are_you_disabled=config["are_you_disabled"],
        are_you_veteran=config["are_you_veteran"],
        are_you_hispanic_or_latino=config["are_you_hispanic_or_latino"],
    )

    prompt = load_prompt(
        "apply.txt",
        resume=resume_text,
        name="Brandon Moffitt",
        email="brandon.james.moffitt@gmail.com",
        job_url="https://ats.rippling.com/rippling/jobs/bda12f6a-6afc-45af-8e6a-b0056facf15c"
    )

    agent = Agent(
        task=prompt,
        llm=model,
        controller=controller,
        browser=browser,
    )

    await agent.run()

if __name__ == '__main__':
    asyncio.run(main())

#python job_agent_openai.py