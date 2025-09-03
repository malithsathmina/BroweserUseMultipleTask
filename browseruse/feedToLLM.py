import os
import glob
import json
import google.generativeai as genai
from dotenv import load_dotenv

# 1️⃣ Load API key from .env
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("❌ Gemini API key not found in .env file")

# 2️⃣ Configure Gemini
genai.configure(api_key=API_KEY)

# 3️⃣ Path to JSON folder
json_dir = r"C:\Users\malit\OneDrive\Desktop\OBO ai\BroweserUseMultipleTask\browseruse\element_data"

# 4️⃣ Find latest JSON file
list_of_files = glob.glob(os.path.join(json_dir, "*.json"))
if not list_of_files:
    print("⚠️ No JSON files found in the element_data folder.")
    exit()

latest_file = max(list_of_files, key=os.path.getctime)
print(f"\n📂 Latest step file: {latest_file}")

# 5️⃣ Load JSON content
with open(latest_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Preview
print("\n📝 Extracted Data (preview):")
#print(json.dumps(data, indent=2)[:500])

# 6️⃣ Create model (use gemini-2.0-flash)
model = genai.GenerativeModel("gemini-2.0-flash")

# 7️⃣ Prepare holistic prompt
prompt = f"""
You are given the extracted elements of a webpage in JSON format.
Each object represents a DOM element with its tag, text content, bounding box, visibility, etc.

Your task:
1. Summarize what this webpage looks like overall.
2. Explain the purpose of key elements (buttons, links, headings, forms).
3. Describe the general structure (header, navigation, main content, footer, etc).
4. Mention any call-to-action or special interactive elements.

Webpage Elements JSON:
{json.dumps(data, indent=2)[:15000]}  # limit to avoid exceeding context
"""

# 8️⃣ Get description
response = model.generate_content(prompt)

# 9️⃣ Output
print("\n🌐 Overall Page Description:")
print(response.text)
