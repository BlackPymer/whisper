from pydantic import BaseModel, Field


class TranscriptionResponse(BaseModel):
    text: str = Field(..., description="Transcribed text from the audio file")
    language: str | None = Field(None, description="Detected language of the audio")
    confidence: float | None = Field(
        None, description="Confidence score of the transcription", ge=0.0, le=1.0
    )


class HealthResponse(BaseModel):
    status: str = Field(..., description="Health status of the API")
    whisper_model: str = Field(..., description="Currently loaded Whisper model")


class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Error message")
    error_code: str | None = Field(None, description="Error code for specific errors")
