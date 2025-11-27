# config.py
import os
from dotenv import load_dotenv

# Load environment variables if using .env, otherwise set manually below
load_dotenv()

# GOOGLE GEMINI API KEY
# Get this from https://aistudio.google.com/
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyC2zHa3cpd6y5aLIAap63A0g4_G3j2Avio")

if GOOGLE_API_KEY == "AIzaSyC2zHa3cpd6y5aLIAap63A0g4_G3j2Avio":
    print("WARNING: You need to set your Google API Key in config.py")
