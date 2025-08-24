import tempfile
from pathlib import Path
from typing import Any

import whisper
from fastapi import HTTPException, UploadFile

from .config import settings
from .models import TranscriptionResponse


class WhisperService:
    def __init__(self) -> None:
        self.model: Any = None
        self.model_name = settings.whisper_model

    def load_model(self) -> None:
        if self.model is None:
            self.model = whisper.load_model(self.model_name)

    async def transcribe_audio(self, audio_file: UploadFile) -> TranscriptionResponse:
        if not audio_file.content_type:
            raise HTTPException(
                status_code=400,
                detail="Content type is required",
            )

        if audio_file.content_type not in settings.allowed_audio_types:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported audio format. Allowed formats: {', '.join(settings.allowed_audio_types)}",
            )

        if audio_file.size and audio_file.size > settings.max_file_size:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size: {settings.max_file_size / (1024 * 1024):.1f}MB",
            )

        self.load_model()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".tmp") as temp_file:
            try:
                content = await audio_file.read()
                temp_file.write(content)
                temp_file.flush()

                result = self.model.transcribe(temp_file.name)

                return TranscriptionResponse(
                    text=result["text"].strip(),
                    language=result.get("language"),
                    confidence=result.get("confidence"),
                )
            finally:
                Path(temp_file.name).unlink(missing_ok=True)


whisper_service = WhisperService()
