import os
from groq import Groq
from dotenv import load_dotenv

# Force Python to load the .env file from the root backend directory
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
load_dotenv(os.path.join(base_dir, ".env"))

class GeminiService:
    def __init__(self):
        try:
            # Bypass Pydantic and read the key directly from the environment
            groq_key = os.getenv("GROQ_API_KEY")
            
            if groq_key:
                self.client = Groq(api_key=groq_key)
            else:
                print("⚠️ Warning: GROQ_API_KEY is still returning None.")
                self.client = None
        except Exception as e:
            print(f"⚠️ Warning: Groq client not initialized. {str(e)}")
            self.client = None

    SYSTEM_PROMPT = """
You are EduQ, the official bilingual AI assistant for the Ministry of Education (MoE), Bangladesh.
Your responsibilities:
1. Provide accurate, neutral, and policy-grounded information in Bengali or English based on the user's language.
2. Ground all answers strictly in official regulations, curriculum directives (NCTB), and education board rules.
3. If an answer is unknown, explicitly state "তথ্য পাওয়া যায়নি" (Information not found).
"""

    async def generate_response(self, user_query: str, context: str = "") -> str:
        if not self.client:
            return "Error: GROQ_API_KEY is missing from .env file."

        prompt = user_query
        if context:
            prompt = f"Context Information:\n{context}\n\nUser Question: {user_query}"

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                # Using Groq's most stable, universally available free model
                model="openai/gpt-oss-20b", 
                temperature=0.2,
                max_tokens=600,
            )
            
            # Extract content and protect against empty returns
            content = chat_completion.choices[0].message.content
            if content and content.strip():
                return content.strip()
            else:
                return "দুঃখিত, এই মুহূর্তে সঠিক তথ্যটি পাওয়া যায়নি। (Sorry, exact information could not be generated right now.)"
                
        except Exception as e:
            print(f"API Error Caught: {str(e)}")
            return f"[Dev Mode Mock Response] EduQ would answer: '{user_query}'"