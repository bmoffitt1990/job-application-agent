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

    prompt = f"""You're a job application agent. Based on the following resume, suggest 3 different job titles that I should go after. Please consider my years of experience and knowing that I want to stay in the Tech sector. Here's the resume content:

    {resume_text}
    """

    response = model.generate_content(prompt)
    print(response.text)

    #await asyncio.gather(*[agent.run() for agent in agents])

if __name__ == '__main__':
    asyncio.run(main())

