import logging
import tempfile
import time
from pathlib import Path
from typing import Any

import torch
import whisper
from fastapi import HTTPException, UploadFile

from .config import settings
from .models import TranscriptionResponse

# Configure logging for console output
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class WhisperService:
    def __init__(self) -> None:
        self.model: Any = None
        self.model_name = settings.whisper_model

    def load_model(self) -> None:
        if self.model is None:
            logger.info(f"Loading Whisper model: {self.model_name}")

            # Check device availability and force GPU usage
            if torch.cuda.is_available():
                device = "cuda"
                logger.info(f"CUDA available: {torch.cuda.get_device_name(0)}")
                logger.info(f"CUDA device count: {torch.cuda.device_count()}")
                logger.info(f"Using GPU for transcription")
            else:
                device = "cpu"
                logger.warning("CUDA not available, falling back to CPU")

            model_load_start = time.time()
            self.model = whisper.load_model(self.model_name, device=device)
            model_load_time = time.time() - model_load_start

            # Log which device the model is actually on
            actual_device = next(self.model.parameters()).device
            logger.info(f"Model loaded on device: {actual_device}")
            logger.info(f"Model loaded in {model_load_time:.2f} seconds")

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

                # Start timing the transcription
                transcription_start = time.time()
                logger.info(f"Starting transcription for file: {audio_file.filename}")

                result = self.model.transcribe(temp_file.name)

                # Calculate and log transcription time
                transcription_time = time.time() - transcription_start
                logger.info(
                    f"Transcription completed in {transcription_time:.2f} seconds"
                )

                # Log additional transcription details
                text_length = len(result["text"].strip())
                logger.info(f"Transcribed text length: {text_length} characters")
                if transcription_time > 0:
                    chars_per_second = text_length / transcription_time
                    logger.info(
                        f"Processing speed: {chars_per_second:.1f} characters/second"
                    )

                return TranscriptionResponse(
                    text=result["text"].strip(),
                    language=result.get("language"),
                    confidence=result.get("confidence"),
                )
            finally:
                Path(temp_file.name).unlink(missing_ok=True)


whisper_service = WhisperService()
