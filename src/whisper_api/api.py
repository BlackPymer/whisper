from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .models import ErrorResponse, HealthResponse, TranscriptionResponse
from .service import whisper_service

app = FastAPI(
    title=settings.app_name,
    description="Local Whisper speech-to-text API using OpenAI Whisper models",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    return HealthResponse(
        status="healthy",
        whisper_model=settings.whisper_model,
    )


@app.post(
    "/transcribe",
    response_model=TranscriptionResponse,
    responses={
        400: {"model": ErrorResponse},
        413: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def transcribe_audio(
    audio_file: UploadFile = File(..., description="Audio file to transcribe"),
) -> TranscriptionResponse:
    try:
        return await whisper_service.transcribe_audio(audio_file)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error during transcription: {str(e)}",
        ) from e
