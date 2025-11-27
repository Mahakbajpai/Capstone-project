# config.py
import os
from dotenv import load_dotenv

# Load environment variables if using .env, otherwise set manually below
load_dotenv()

# GOOGLE GEMINI API KEY
# Get this from https://aistudio.google.com/
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "YOUR_ACTUAL_API_KEY_HERE")

if GOOGLE_API_KEY == "YOUR_ACTUAL_API_KEY_HERE":
    print("WARNING: You need to set your Google API Key in config.py")
