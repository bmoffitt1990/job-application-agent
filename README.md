# 🤖 Gemini Job Application Agent

A Python tool that reads your resume, analyzes it with Google’s Gemini model, and suggests relevant machine learning internships. This is the foundation for a fully automated job search assistant.

---

## 🔧 Features

- 🧠 Uses Google's **Gemini 1.5 Pro** to analyze your resume  
- 📄 Reads resume content from a local `.pdf`  
- 💡 Generates personalized internship suggestions  
- 🔜 Extendable: Integrate with browser automation for form filling and job board scraping using `browser-use`  

---

## 📁 Project Structure

```
.
├── .env                  # API keys and secrets (not tracked by Git)
├── Brandon_Moffitt.pdf   # Your resume (ignored by Git)
├── gemini_test.py        # Simple script to verify Gemini integration
├── job_agent.py          # Legacy or alternate job agent version
├── job_agent_gemini.py   # Main Gemini-powered agent script
├── requirements.txt      # Project dependencies
├── venv/                 # Virtual environment (ignored by Git)
```

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/job-application-agent.git
cd job-application-agent
```

### 2. Set up your virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Add your `.env` file

Create a `.env` file in the root with your Gemini API key:

```
GOOGLE_API_KEY=your-google-cloud-api-key
```

> 🔐 This file is already `.gitignore`'d.

### 4. Add your resume

Place your resume as `resume.pdf` in the project root, or change the filename in `job_agent_gemini.py`.

---

## 🧪 Run It

```bash
python job_agent_gemini.py
```

You’ll get:
- ✅ Your resume read and parsed
- 💡 ML internship suggestions powered by Gemini

---

## 📌 Roadmap Ideas

- ✅ Save internship leads to a CSV  
- 🔄 Automatically scrape job boards (via `browser-use`)  
- 📝 Generate cover letters  
- 📬 Auto-apply and track applications  

---

## 📄 License

MIT License
