# parser.py
# Handles sending text to Gemini and parsing response
import os
import json
from google import genai
from dotenv import load_dotenv

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

    # Pinned to gemini-2.5-flash — upgrade intentionally, not automatically
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    raw = response.text.strip()

    # Strip markdown code fences if Gemini adds them anyway
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    parsed = json.loads(raw)
    return parsed