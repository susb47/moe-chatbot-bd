from google import genai
from google.genai import types
from app.core.config import settings

class GeminiService:
    def __init__(self):
        # Gracefully handle missing API keys so the server still starts
        try:
            if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != "dummy_key":
                self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
            else:
                self.client = genai.Client() # Tries to fall back to OS environment variables
        except Exception as e:
            print(f"⚠️ Warning: Gemini API client not initialized. {str(e)}")
            self.client = None

    SYSTEM_PROMPT = """
You are EduQ, the official bilingual AI assistant for the Ministry of Education (MoE), Bangladesh.
Your responsibilities:
1. Provide accurate, neutral, and policy-grounded information in Bengali or English based on the user's language.
2. Ground all answers strictly in official regulations, curriculum directives (NCTB), and education board rules.
3. If an answer is unknown, high-stakes, or personal-record-dependent, explicitly state "তথ্য পাওয়া যায়নি" (Information not found) or "Not found", and instruct the user to visit the relevant education board or ministry office.
4. Maintain an objective, professional administrative tone. Avoid speculative commentary on curriculum reforms.
5. Always cite official circulars, gazettes, or regulatory bodies where applicable.
"""

    async def generate_response(self, user_query: str, context: str = "") -> str:
        if not self.client:
            return "Error: Gemini API key is missing. Please add GEMINI_API_KEY to your .env file."

        prompt = user_query
        if context:
            prompt = f"Context Information:\n{context}\n\nUser Question: {user_query}"

        try:
            response = self.client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=self.SYSTEM_PROMPT,
                    temperature=0.2,
                    max_output_tokens=600,
                ),
            )
            return response.text.strip()
        except Exception as e:
            # Fallback for development if API is locked by a 403
            print(f"API Error Caught: {str(e)}")
            return f"[Dev Mode Mock Response] If the API was connected, EduQ would answer: '{user_query}' based on MoE policies."