import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Anthropic (Claude)
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    
    # Free Tier Providers (Google Gemini & Groq)
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "") or os.getenv("GOOGLE_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    LLM_MODEL: str = os.getenv("LLM_MODEL", "auto")

    # Search Configuration (DuckDuckGo is built-in free fallback, Tavily is optional)
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")

    # Database Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./contentmaker.db")

    # Agent Configuration
    MAX_REVISION_LOOPS: int = int(os.getenv("MAX_REVISION_LOOPS", "3"))
    CRITIC_MIN_OVERALL_SCORE: float = float(os.getenv("CRITIC_MIN_OVERALL_SCORE", "4.0"))
    CRITIC_MIN_INDIVIDUAL_SCORE: float = float(os.getenv("CRITIC_MIN_INDIVIDUAL_SCORE", "3.0"))

    # Server Configuration
    PORT: int = int(os.getenv("PORT", "8000"))
    HOST: str = os.getenv("HOST", "0.0.0.0")

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
