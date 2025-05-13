## Not working

import asyncio
import os
from dotenv import load_dotenv
import google.generativeai as genai
from PyPDF2 import PdfReader
from pathlib import Path

from browser_use import Agent, Controller
from browser_use.browser.browser import Browser, BrowserConfig

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise ValueError("Missing GOOGLE_API_KEY in .env")

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

def read_cv(file_path: Path) -> str:
    if not file_path.exists():
        raise FileNotFoundError(f"Resume not found at {file_path}")

    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    print(f"[DEBUG] Loaded resume with {len(text)} characters")
    return text

controller = Controller()

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

ground_task = (
    "You are a professional job finder. "
    "1. Read my cv with read_cv. "
    "2. Find machine learning internships and save them to a file. "
    "Search at company:"
)

tasks = [
    ground_task + "\n" + "Google",
    # Add more companies here
]

async def main():
    cv_path = Path.cwd() / "Brandon_Moffitt.pdf"
    resume_text = read_cv(cv_path)

    job_url = "https://careers.google.com/jobs/results/123456-job-title-placeholder"  # <-- replace with a real one

    prompt = f"""
    You're a job application assistant. First, read my resume below:

    [RESUME]
    {resume_text}

    Then, visit this job posting:
    {job_url}

    Extract the job description, and tell me:
    - How well I fit. Be honest! Do not be afraid to say I don't fit.
    - What skills I should highlight.
    - Whether I should apply
    """

    agent = Agent(
        task=prompt,
        llm=model,
        controller=controller,
        browser=browser,
    )

    await agent.run()

if __name__ == '__main__':
    asyncio.run(main())

