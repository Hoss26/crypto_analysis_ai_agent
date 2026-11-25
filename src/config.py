import os

from dotenv import load_dotenv
load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_kEY")
FREECRYPTO_TOKEN = os.getenv("FREECRYPTO_TOKEN")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")