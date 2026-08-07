# config/settings.py

import os
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "openai/gpt-4o-mini")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# ── FAIL FAST: CHECK REQUIRED KEYS AT STARTUP ───────────────────
missing = []
if not OPENROUTER_API_KEY:
    missing.append("OPENROUTER_API_KEY")
if not SUPABASE_URL:
    missing.append("SUPABASE_URL")
if not SUPABASE_KEY:
    missing.append("SUPABASE_KEY")

if missing:
    raise EnvironmentError(
        f"\n\n❌ Missing required environment variables:\n"
        f"   {', '.join(missing)}\n\n"
        f"Please check your .env file and make sure all keys are set.\n"
    )

llm = LLM(
    model=MODEL_NAME,
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL,
)