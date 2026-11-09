import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    GIGACHAT_KEY: str = os.getenv("GIGACHAT_KEY", "")
    GIGACHAT_SCOPE: str = os.getenv("GIGACHAT_SCOPE", "GIGACHAT_API_B2B")
    GIGACHAT_MODEL: str = os.getenv("GIGACHAT_MODEL", "GigaChat-2-Max")
    APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))

    def validate(self):
        if not self.GIGACHAT_KEY:
            raise ValueError(
                "GIGACHAT_KEY не задан. Установите переменную окружения "
                "или добавьте её в .env"
            )


settings = Settings()