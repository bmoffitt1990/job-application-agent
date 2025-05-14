# AI Headhunter – OpenAI-Powered Job Application Agent

This project automates job applications on modern job boards like Rippling, using Playwright and OpenAI to fill out forms, upload resumes, and follow multi-step instructions.

---

## ✅ Features

- 🔍 Navigates to job URLs and clicks "Apply" automatically
- 📎 Uploads resume and cover letter using CSS/data attributes
- 🧠 Fills out personal information (name, email, phone, etc.)
- 🤖 Controlled via OpenAI (GPT-4o), using browser-use's `Agent` + `Controller`
- 🔌 Modular architecture for supporting additional job boards
- 🧱 Easily extendable with custom actions and prompts

---

## 📁 Project Structure

```
job-agent/
├── openai_agents/
│   └── rippling.py               # Agent for Rippling job applications
├── prompts/
│   └── apply.txt                 # Task prompt injected with variables
├── utils/
│   ├── config.py                 # Loads user data from .env or YAML
│   ├── actions/
│   │   ├── shared.py             # Shared upload helpers
│   │   └── rippling.py           # Rippling-specific upload logic
├── .env                          # OpenAI key + user details
├── README.md                     # This file
```

---

## ⚙️ Requirements

- Python 3.9+
- `browser-use`
- `playwright`
- `openai`
- `langchain`
- `python-dotenv`

Install dependencies:
```bash
pip install -r requirements.txt
playwright install
```

---

## 🚀 How to Run

From the project root, run the Rippling OpenAI agent like this:

```bash
python3 -m openai_agents.rippling
```

Make sure you have:
- A valid `.env` file with:
  - `OPENAI_API_KEY=...`
  - Your resume/cover letter paths and personal info
- A prompt at `prompts/apply.txt`

---

## 🧩 Coming Soon

- Lever, Greenhouse, Workday support
- Auto-generated cover letters
- State saving + retry queues
- Application history tracker

---

Built with ❤️ by Brandon