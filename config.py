# config.py
import os
from dotenv import load_dotenv

# Load environment variables if using .env, otherwise set manually below
load_dotenv()

# GOOGLE GEMINI API KEY
# Get this from https://aistudio.google.com/
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "GOOGLE_API_KEY=AIzaSyCGX3-daUblGSZJdTrboskrw5GoEnNnqtw")

if GOOGLE_API_KEY == "GOOGLE_API_KEY=AIzaSyCGX3-daUblGSZJdTrboskrw5GoEnNnqtw":
    print("WARNING: You need to set your Google API Key in config.py")
