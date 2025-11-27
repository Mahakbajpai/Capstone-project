# config.py
import os

# I removed the "GOOGLE_API_KEY=" part from inside the quotes.
# It should just be the raw code starting with AIza.
GOOGLE_API_KEY = "AIzaSyCGX3-daUblGSZJdTrboskrw5GoEnNnqtw"

if GOOGLE_API_KEY == "YOUR_ACTUAL_API_KEY_HERE":
    print("WARNING: You need to set your Google API Key in config.py")
