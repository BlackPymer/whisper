from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Whisper Speech-to-Text API"
    host: str = "0.0.0.0"
    port: int = 9000
    whisper_model: Literal["tiny", "base", "small", "medium", "large"] = "medium"
    max_file_size: int = 25 * 1024 * 1024
    allowed_audio_types: set[str] = {
        "audio/wav",
        "audio/mpeg",
        "audio/mp3",
        "audio/mp4",
        "audio/m4a",
        "audio/flac",
        "audio/ogg",
        "application/ogg",
        "audio/webm",
    }

    model_config = {"env_file": ".env"}


settings = Settings()
