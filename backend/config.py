import os
from pathlib import Path
from dotenv import load_dotenv

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Load local .env for development; host-provided environment variables are used in deployment.
def reload_config():
    global DATABASE_PATH, APIFY_API_TOKEN, APIFY_LINKEDIN_ACTOR_ID, APIFY_INSTAGRAM_ACTOR_ID
    global LLM_PROVIDER, OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY, CORS_ORIGINS
    load_dotenv(BASE_DIR / ".env", override=False)
    DATABASE_PATH = os.getenv("DATABASE_PATH", str(DATA_DIR / "agentic_dating.db"))
    APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN", "")
    APIFY_LINKEDIN_ACTOR_ID = os.getenv("APIFY_LINKEDIN_ACTOR_ID", "curious_coder/linkedin-profile-scraper")
    APIFY_INSTAGRAM_ACTOR_ID = os.getenv("APIFY_INSTAGRAM_ACTOR_ID", "apify/instagram-profile-scraper")
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "deterministic")  # deterministic | openai | anthropic | gemini
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    CORS_ORIGINS = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://localhost:8000"
        ).split(",")
        if origin.strip()
    ]

reload_config()
