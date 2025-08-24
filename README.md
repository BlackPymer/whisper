# Whisper Speech-to-Text API

A local, free speech-to-text API built with FastAPI and OpenAI's Whisper models. This service runs entirely on your machine without requiring any external API calls or payments.

## Features

- 🆓 **Completely free** - Uses local Whisper models
- 🚀 **Fast API** - Built with FastAPI for high performance
- 🎵 **Multiple audio formats** - Supports WAV, MP3, MP4, M4A, FLAC, OGG, WebM
- 🔧 **Configurable** - Multiple Whisper model sizes available
- 🐍 **Modern Python** - Built with Python 3.13, type hints, and strict linting
- 📊 **API Documentation** - Auto-generated OpenAPI/Swagger docs

## Quick Start

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) for dependency management

### Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd whisper
```

2. Install dependencies:
```bash
make dev-install
```

3. The project includes a local ffmpeg binary (no system installation required!)

4. Run the server:
```bash
./run_local.sh
```
or
```bash
make run
```

The API will be available at `http://localhost:9000`

### API Usage

#### Health Check
```bash
curl http://localhost:9000/health
```

#### Transcribe Audio
```bash
curl -X POST "http://localhost:9000/transcribe" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "audio_file=@your_audio_file.wav"
```

#### Response Format
```json
{
  "text": "This is the transcribed text from your audio file.",
  "language": "en"
}
```

## Configuration

Copy `env.example` to `.env` and modify as needed:

```bash
cp env.example .env
```

Available settings:
- `WHISPER_MODEL`: Model size (`tiny`, `base`, `small`, `medium`, `large`)
- `PORT`: Server port (default: 9000)
- `HOST`: Server host (default: 0.0.0.0)
- `MAX_FILE_SIZE`: Maximum audio file size in bytes

### Whisper Models

| Model  | Size | Speed | Accuracy |
|--------|------|-------|----------|
| tiny   | 39MB | Fastest | Lowest |
| base   | 74MB | Fast | Good |
| small  | 244MB | Medium | Better |
| medium | 769MB | Slow | Very Good |
| large  | 1550MB | Slowest | Best |

## Development

### Available Commands

```bash
make dev-install    # Install with development dependencies
make run           # Run the server
make test          # Run tests
make lint          # Run linting (ruff + pyright)
make format        # Format code
make check         # Run all checks (format, lint, test)
make clean         # Clean cache files
```

### Project Structure

```
whisper/
├── src/whisper_api/
│   ├── __init__.py
│   ├── api.py          # FastAPI application and routes
│   ├── config.py       # Configuration settings
│   ├── main.py         # Entry point
│   ├── models.py       # Pydantic models
│   └── service.py      # Whisper service logic
├── tests/
│   ├── __init__.py
│   └── test_api.py     # API tests
├── run_server.py       # Simple server runner
├── pyproject.toml      # Project configuration
├── Makefile           # Development commands
└── README.md
```

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:9000/docs`
- ReDoc: `http://localhost:9000/redoc`

## Supported Audio Formats

- WAV (audio/wav)
- MP3 (audio/mpeg, audio/mp3)
- MP4 (audio/mp4)
- M4A (audio/m4a)
- FLAC (audio/flac)
- OGG (audio/ogg)
- WebM (audio/webm)

## Requirements

- CPU: Any modern processor (GPU acceleration available with CUDA)
- RAM: Varies by model (1GB+ recommended for base model)
- Storage: 100MB+ for model files
- Network: Only for initial model download

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes following the code style (ruff + pyright)
4. Run `make check` to ensure all tests pass
5. Submit a pull request 