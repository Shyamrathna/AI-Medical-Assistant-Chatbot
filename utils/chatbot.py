from groq import Groq
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# System prompt
SYSTEM_PROMPT = """
You are an AI Medical Assistant.

Rules:
- Provide general health advice only
- Do NOT diagnose diseases
- Suggest consulting a doctor when needed
- Keep answers simple and safe
"""

def get_response(messages):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"⚠️ Error: {str(e)}"