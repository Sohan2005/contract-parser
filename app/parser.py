# parser.py
# Handles sending text to Gemini and parsing response
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_contract(text: str) -> str:
    prompt = f"""
    Analyze this contract and extract key information.
    
    Contract text:
    {text}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text