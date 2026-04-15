import os
import re
from sentence_transformers import SentenceTransformer, util
import textstat
from google import genai
from google.genai import types
from src.utils import get_logger, retry_api_call

logger = get_logger("evaluator")

# Initialize SentenceTransformer globally to save load time per call
# Suppress torch warnings about huggingface token
os.environ["TOKENIZERS_PARALLELISM"] = "false"
try:
    st_model = SentenceTransformer('all-MiniLM-L6-v2')
except Exception as e:
    logger.warning(f"Failed to load sentence_transformers: {e}. Fact recall will fail.")
    st_model = None

def split_into_sentences(text: str) -> list[str]:
    # Very basic sentence splitting.
    sentences = re.split(r'(?<=[.!?]) +', text.replace('\n', ' '))
    return [s.strip() for s in sentences if s.strip()]

def fact_recall_score(generated_email: str, facts: list[str]) -> float:
    """Metric 1: Fact Recall Score utilizing Sentence-transformers"""
    if st_model is None:
        logger.error("SentenceTransformer model is not loaded.")
        return 0.0

    email_sentences = split_into_sentences(generated_email)
    if not email_sentences:
        return 0.0

    email_embeddings = st_model.encode(email_sentences)
    recalled = 0
    threshold = 0.45

    for fact in facts:
        fact_embedding = st_model.encode(fact)
        similarities = util.cos_sim(fact_embedding, email_embeddings)
        if float(similarities.max()) > threshold:
            recalled += 1
            
    return round((recalled / len(facts)) * 100, 2)

@retry_api_call
def _call_judge_gemini(prompt: str) -> str:
    from src.generator import _client, setup_client
    if not _client:
        setup_client()
        
    response = _client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.0,
            max_output_tokens=150
        )
    )
    return response.text

def tone_alignment_score(generated_email: str, requested_tone: str) -> float:
    """Metric 2: Tone Alignment Score using LLM-as-a-Judge"""
    judge_prompt = f"""You are a tone analysis expert. Given the requested tone and the email below,
rate how well the email achieves the requested tone on a scale of 1 to 10.

Requested Tone: {requested_tone}
Email: {generated_email}

Respond in this exact format:
SCORE: [number]
REASON: [one sentence]"""

    try:
        response_text = _call_judge_gemini(judge_prompt)
        match = re.search(r'SCORE:\s*(\d+)', response_text)
        if match:
            score = float(match.group(1))
            # Ensure score is between 1 and 10
            score = max(1, min(10, score))
            return round((score / 10) * 100, 2)
        else:
            logger.warning(f"Could not parse score from judge response: {response_text}")
            return 0.0
    except Exception as e:
        logger.error(f"Error during tone alignment judging: {e}")
        return 0.0

def fluency_conciseness_score(generated_email: str, human_reference: str) -> float:
    """Metric 3: Fluency & Conciseness Score"""
    # A) Fluency
    flesch = textstat.flesch_reading_ease(generated_email)
    fluency = min(100, max(0, flesch + 30))  # shift to penalize very hard text
    
    # B) Conciseness
    gen_words = len(generated_email.split())
    ref_words = len(human_reference.split())
    ratio = gen_words / ref_words if ref_words > 0 else 1.0
    
    conciseness = max(0, 100 - abs(ratio - 1.0) * 150)
    
    return round((fluency + conciseness) / 2, 2)

def composite_score(fact_recall: float, tone_alignment: float, fluency_conciseness: float) -> float:
    """Calculates weighted composite score."""
    return round(
        (fact_recall * 0.40) + (tone_alignment * 0.35) + (fluency_conciseness * 0.25),
        2
    )
