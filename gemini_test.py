import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#models = genai.list_models()
#for m in models:
#    print(m.name, "→", m.supported_generation_methods)

model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
#model = genai.GenerativeModel("gemini-pro")

response = model.generate_content("What are 3 great ML internships to apply for?")
print(response.text)
