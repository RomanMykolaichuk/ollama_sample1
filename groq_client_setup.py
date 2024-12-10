import os
from dotenv import load_dotenv
from groq import Groq


def getGroqClient():
    # Load environment variables from .env file
    load_dotenv()
    # Retrieve API key from environment variable
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        raise ValueError("No API Key found in environment variables")
    else: print("Ok")
    client = Groq(api_key=api_key)
    return client

