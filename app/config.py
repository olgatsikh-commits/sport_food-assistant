import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GIGACHAT_KEY: str = os.getenv("GIGACHAT_KEY", "")
    GIGACHAT_BASE_URL: str = os.getenv("GIGACHAT_BASE_URL", "https://foundation-models.api.cloud.ru/v1")
    GIGACHAT_MODEL: str = os.getenv("GIGACHAT_MODEL", "GigaChat/GigaChat-3-Pro")
    APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))

    def validate(self):
        if not self.GIGACHAT_KEY:
            raise ValueError("GIGACHAT_KEY не задан.")

settings = Settings()