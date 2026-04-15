import os
from google import genai
from google.genai import types
from src.utils import get_logger, retry_api_call
from dotenv import load_dotenv

logger = get_logger("generator")

SYSTEM_PROMPT = """
You are a Senior Business Communication Expert with 15 years of experience writing 
professional emails across industries including finance, tech, consulting, and HR.
You are known for:
- Perfect tone calibration (formal to casual, urgent to empathetic)
- Seamlessly weaving in key facts without sounding like a list
- Writing emails that are concise yet complete — never padded, never missing anything
- Strong, purposeful subject lines and clear calls to action

Your task: Generate a professional email given an intent, a set of key facts, and a 
desired tone.

ALWAYS follow this reasoning process before writing:
1. THINK: Identify the core goal of this email. What action or response does it seek?
2. PLAN: Decide the optimal structure (greeting → context → facts → ask → close).
3. WRITE: Draft the email, ensuring every key fact is included naturally.
4. CHECK: Confirm the tone matches exactly, all facts are present, and the email 
   is polished.

Return ONLY the final email. No preamble, no explanation, no markdown fences.
The output must be a ready-to-send email with Subject line, body, and sign-off.
"""

FEW_SHOT_EXAMPLE = """
--- EXAMPLE ---
INTENT: Follow up after a product demo to a potential client
KEY FACTS:
- Demo happened on June 5th
- Client showed interest in the analytics dashboard feature
- Pricing starts at $299/month with a 14-day free trial available
- Next step: schedule a 30-minute Q&A call
TONE: Professional but warm

OUTPUT:
Subject: Following Up on Yesterday's Demo — Next Steps

Hi [Client Name],

Thank you for taking the time to join us for the demo on June 5th. It was great 
walking you through the platform, and I noticed your interest in the analytics 
dashboard — it really is one of our most powerful features.

I wanted to follow up and share that our plans start at $299/month, and we do offer 
a 14-day free trial so you can explore the full feature set at no commitment.

I'd love to set up a quick 30-minute Q&A call at your convenience to answer any 
remaining questions. Would sometime next week work for you?

Looking forward to hearing from you.

Best regards,
[Your Name]
--- END EXAMPLE ---
"""

USER_PROMPT_TEMPLATE = """
Now generate an email for the following:

INTENT: {intent}
KEY FACTS:
{facts}
TONE: {tone}
"""

_client = None

def setup_client():
    """Initializes Google GenAI Configs"""
    global _client
    if _client is not None:
        return
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set in .env")
    _client = genai.Client(api_key=api_key)

def build_user_prompt(intent: str, facts: list[str], tone: str) -> str:
    facts_str = "\n".join(f"- {f}" for f in facts)
    return USER_PROMPT_TEMPLATE.format(intent=intent, facts=facts_str, tone=tone)

@retry_api_call
def generate_email_gemini(intent: str, facts: list[str], tone: str, model_name: str = "gemini-2.5-pro") -> str:
    """Generates email using the specified Gemini model."""
    try:
        global _client
        if not _client:
            setup_client()
            
        user_message = build_user_prompt(intent, facts, tone)
        
        response = _client.models.generate_content(
            model=model_name,
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT + FEW_SHOT_EXAMPLE,
                max_output_tokens=800,
                temperature=0.3
            )
        )
        
        # Strip potential markdown fences just in case
        text = response.text.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines[-1].startswith("```"):
                lines = lines[:-1]
            text = "\n".join(lines).strip()
            
        return text
    except Exception as e:
        logger.error(f"Error generating email with {model_name}: {e}")
        raise

def generate_email(intent: str, facts: list[str], tone: str, provider: str = "gemini-2.5-pro") -> str:
    """Router function to interact with provider"""
    return generate_email_gemini(intent, facts, tone, model_name=provider)
