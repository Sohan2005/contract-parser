# parser.py
# Handles sending text to Gemini and parsing response
import os
import json
from google import genai
from google.genai import errors as genai_errors
from dotenv import load_dotenv
from app.errors import AIParsingError

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """
You are a contract analysis engine. Your job is to extract key entities from legal contracts.

You must ALWAYS respond with valid JSON and nothing else.
Do not include any explanation, markdown, or code fences.
Do not write ```json or ``` anywhere in your response.
Your entire response must be a single valid JSON object.

Extract the following fields:

{
    "contract_type": "string - type of contract e.g. Service Agreement, NDA, Supply Contract",
    "parties": [
        {
            "name": "string - company or person name",
            "role": "string - their role e.g. first party, second party, client, vendor"
        }
    ],
    "effective_date": "string - the date the contract starts, or null if not found",
    "expiry_date": "string - the date the contract ends, or null if not found",
    "dollar_amounts": [
        {
            "amount": "string - the monetary value",
            "description": "string - what this amount refers to"
        }
    ],
    "key_obligations": [
        "string - list the most important obligations from the contract"
    ],
    "termination_clause": "string - summary of termination terms, or null if not found",
    "governing_law": "string - which country or state law governs this contract, or null if not found"
}

If a field is not found in the contract, use null for single values or [] for arrays.
"""

def analyze_contract(text: str) -> dict:
    prompt = f"""
{SYSTEM_PROMPT}

Contract text to analyze:
{text}
"""

    try:
        # Pinned to gemini-2.5-flash — upgrade intentionally, not automatically
        # Check for new models at: aistudio.google.com
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            raise AIParsingError(
                "AI service rate limit reached. Please wait a moment and try again."
            )
        elif "API_KEY" in error_msg or "401" in error_msg:
            raise AIParsingError(
                "Invalid API key. Please check your configuration."
            )
        else:
            raise AIParsingError(
                f"AI service error: {error_msg}"
            )

    raw = response.text.strip()

    # Strip markdown code fences if Gemini adds them anyway
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    try:
        parsed = json.loads(raw)
        return parsed
    except json.JSONDecodeError:
        raise AIParsingError(
            "AI returned an unexpected response format. Please try again."
        )