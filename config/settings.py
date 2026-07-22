import os
from dotenv import load_dotenv
from crewai import LLM


# Load the .env file into the environment

load_dotenv()

#Read values from the environment
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "openai/gpt-4o-mini")


#The LLM object CrewAI agents will use.
llm = LLM(
    model=MODEL_NAME,                   
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL,        
)