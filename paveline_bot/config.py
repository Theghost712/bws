import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")


def env_bool(name: str, default: bool = False) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def env_list(name: str, default: List[str] = None) -> List[str]:
    value = os.environ.get(name)
    if not value:
        return list(default or [])
    return [item.strip() for item in value.split(",") if item.strip()]


# Bot identity
BOT_NAME = os.environ.get("BOT_NAME", "Paveline Bot")
BOT_USERNAME = os.environ.get("BOT_USERNAME", "paveline_bot")

# Telegram
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")

# Admin
ADMIN_IDS = [int(x) for x in env_list("ADMIN_IDS", []) if x.isdigit()]

# AI
AI_PROVIDER = os.environ.get("AI_PROVIDER", "ollama").lower()  # gemini|groq|openrouter|ollama|fallback

# API keys
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")

# AI model names
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.1-8b-instant")
OPENROUTER_MODEL = os.environ.get("OPENROUTER_MODEL", "google/gemini-2.5-flash")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2")

# Ollama
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")

# Scheduling
SEND_TIME = os.environ.get("SEND_TIME", "07:00")  # HH:MM
TIMEZONE = os.environ.get("TIMEZONE", "Africa/Dar_es_Salaam")

# Database
DB_URL = os.environ.get("DB_URL", f"sqlite:///{BASE_DIR / 'paveline.db'}")

# Email
SMTP_HOST = os.environ.get("SMTP_HOST", "")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASS = os.environ.get("SMTP_PASS", "")
SMTP_FROM = os.environ.get("SMTP_FROM", "paveline@example.com")
SMTP_USE_TLS = env_bool("SMTP_USE_TLS", True)

# Dry run
DRY_RUN = env_bool("DRY_RUN", False)

# Output dirs
OUTPUT_DIR = BASE_DIR / "output"
FONTS_DIR = BASE_DIR / "fonts"
ASSETS_DIR = BASE_DIR / "assets"
PROMPTS_DIR = BASE_DIR / "prompts"

OUTPUT_DIR.mkdir(exist_ok=True)
FONTS_DIR.mkdir(exist_ok=True)
ASSETS_DIR.mkdir(exist_ok=True)
PROMPTS_DIR.mkdir(exist_ok=True)

# Card settings
CARD_POST_SIZE = (1080, 1080)
CARD_STORY_SIZE = (1080, 1920)
DEFAULT_CARD_DESIGN = "modern"
