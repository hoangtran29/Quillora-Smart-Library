from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Quillora"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    GEMINI_API_KEY: str = ""
    FAL_API_KEY: str = ""

    LLM_MODEL: str = "gemini-2.0-flash"
    VOICE_MODEL: str = "gemini-2.5-flash-native-audio-preview-12-2025"

    EMBEDDING_MODEL: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    TOP_K: int = 4

    # Auth
    AUTH_SECRET: str = "quillora-dev-secret-change-me"
    AUTH_TOKEN_TTL: int = 60 * 60 * 24 * 7  # 7 days

    # Auth0 (Microsoft OAuth)
    AUTH0_DOMAIN: str = ""
    AUTH0_CLIENT_ID: str = ""
    AUTH0_CLIENT_SECRET: str = ""
    AUTH0_CALLBACK_URL: str = "http://localhost:8000/api/auth/microsoft/callback"

    ROOT_DIR: Path = Path(__file__).resolve().parent.parent
    DATA_DIR: Path = Path(__file__).resolve().parent.parent / "data"
    WEB_DIR: Path = Path(__file__).resolve().parent.parent / "web"

    # Path to the cloned PTIT textbook repo (used to serve PDFs for seed books).
    PTIT_REPO: Path = Path(__file__).resolve().parent.parent.parent / "Giao-Trinh-PTIT"

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


settings = Settings()
settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
(settings.DATA_DIR / "sample_books").mkdir(parents=True, exist_ok=True)
(settings.DATA_DIR / "generated").mkdir(parents=True, exist_ok=True)
(settings.DATA_DIR / "uploads").mkdir(parents=True, exist_ok=True)
