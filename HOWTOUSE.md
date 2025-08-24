# How to Use Whisper API

This guide explains how to use the local Whisper speech-to-text API.

## Server Information

- **Base URL**: `http://localhost:9000`
- **Port**: `9000`
- **Protocol**: HTTP/1.1
- **Content-Type**: `application/json` (responses), `multipart/form-data` (file uploads)

## Starting the Server

### Option 1: Using the local script
```bash
./run_local.sh
```

### Option 2: Using Make
```bash
make run
```

### Option 3: Manual start
```bash
export PATH="$(pwd)/bin:$PATH" && uv run python3 run_server.py
```

The server will start and be available at `http://localhost:9000`.

## API Endpoints

### 1. Health Check

**Endpoint**: `GET /health`

**Description**: Check if the API is running and get server information.

**Request**:
```bash
curl -X GET "http://localhost:9000/health"
```

**Response** (200 OK):
```json
{
  "status": "healthy",
  "whisper_model": "base"
}
```

**Response Fields**:
- `status` (string): Health status of the API
- `whisper_model` (string): Currently loaded Whisper model size

---

### 2. Speech-to-Text Transcription

**Endpoint**: `POST /transcribe`

**Description**: Upload an audio file and get the transcribed text.

**Request**:
```bash
curl -X POST "http://localhost:9000/transcribe" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "audio_file=@path/to/your/audio.wav"
```

**Form Data**:
- `audio_file` (file, required): Audio file to transcribe

**Supported Audio Formats**:
- WAV (`.wav`) - `audio/wav`
- MP3 (`.mp3`) - `audio/mpeg`, `audio/mp3`
- MP4 (`.mp4`) - `audio/mp4`
- M4A (`.m4a`) - `audio/m4a`
- FLAC (`.flac`) - `audio/flac`
- OGG (`.ogg`) - `audio/ogg`, `application/ogg`
- WebM (`.webm`) - `audio/webm`

**File Limits**:
- Maximum file size: 25MB
- Processing time varies by model and audio length

**Success Response** (200 OK):
```json
{
  "text": "Hello, this is a sample transcription of your audio file.",
  "language": "en"
}
```

**Response Fields**:
- `text` (string): Transcribed text from the audio file
- `language` (string, optional): Detected language code (e.g., "en", "es", "fr")

**Error Responses**:

**400 Bad Request** - Invalid file format:
```json
{
  "detail": "Unsupported audio format. Allowed formats: audio/wav, audio/mpeg, audio/mp3, audio/mp4, audio/m4a, audio/flac, audio/ogg, audio/webm"
}
```

**400 Bad Request** - Missing content type:
```json
{
  "detail": "Content type is required"
}
```

**413 Payload Too Large** - File too large:
```json
{
  "detail": "File too large. Maximum size: 25.0MB"
}
```

**422 Unprocessable Entity** - Missing file:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "audio_file"],
      "msg": "Field required",
      "input": null
    }
  ]
}
```

**500 Internal Server Error** - Processing error:
```json
{
  "detail": "Internal server error during transcription: [error details]"
}
```

## Usage Examples

### Python Example
```python
import requests

# Health check
response = requests.get("http://localhost:9000/health")
print(response.json())

# Transcribe audio file
with open("audio.wav", "rb") as f:
    files = {"audio_file": f}
    response = requests.post("http://localhost:9000/transcribe", files=files)
    result = response.json()
    print(f"Transcribed text: {result['text']}")
    print(f"Language: {result['language']}")
```

### JavaScript/Node.js Example
```javascript
const FormData = require('form-data');
const fs = require('fs');
const fetch = require('node-fetch');

async function transcribeAudio() {
  const form = new FormData();
  form.append('audio_file', fs.createReadStream('audio.wav'));
  
  const response = await fetch('http://localhost:9000/transcribe', {
    method: 'POST',
    body: form
  });
  
  const result = await response.json();
  console.log('Transcribed text:', result.text);
  console.log('Language:', result.language);
}

transcribeAudio();
```

### cURL Examples

**Basic transcription**:
```bash
curl -X POST "http://localhost:9000/transcribe" \
  -F "audio_file=@recording.mp3"
```

**With verbose output**:
```bash
curl -v -X POST "http://localhost:9000/transcribe" \
  -H "accept: application/json" \
  -F "audio_file=@speech.wav"
```

**Save response to file**:
```bash
curl -X POST "http://localhost:9000/transcribe" \
  -F "audio_file=@audio.flac" \
  -o transcription.json
```

## Interactive API Documentation

Once the server is running, you can access interactive documentation:

- **Swagger UI**: http://localhost:9000/docs
- **ReDoc**: http://localhost:9000/redoc

These interfaces allow you to:
- Test endpoints directly in the browser
- View detailed request/response schemas
- Download OpenAPI specification

## Configuration

You can customize the API behavior by creating a `.env` file:

```bash
# Copy example configuration
cp env.example .env

# Edit configuration
nano .env
```

**Available settings**:
- `WHISPER_MODEL`: Model size (`tiny`, `base`, `small`, `medium`, `large`)
- `PORT`: Server port (default: 9000)
- `HOST`: Server host (default: 0.0.0.0)
- `MAX_FILE_SIZE`: Maximum upload size in bytes

## Whisper Models

| Model    | Size   | Speed    | Accuracy  | Memory | Use Case |
|----------|--------|----------|-----------|---------|----------|
| `tiny`   | 39MB   | Fastest  | Basic     | ~1GB   | Quick drafts |
| `base`   | 74MB   | Fast     | Good      | ~1GB   | General use |
| `small`  | 244MB  | Medium   | Better    | ~2GB   | Quality transcripts |
| `medium` | 769MB  | Slow     | Very Good | ~5GB   | Professional use |
| `large`  | 1550MB | Slowest  | Best      | ~10GB  | Highest accuracy |

## Troubleshooting

### Server won't start
- Check if port 9000 is available: `lsof -i :9000`
- Verify dependencies: `uv sync --group dev`
- Check logs for error messages

### Transcription fails
- Verify audio file format is supported
- Check file size (must be < 25MB)
- Ensure audio file is not corrupted
- Try with a different audio format

### Performance issues
- Use smaller Whisper model (`tiny` or `base`)
- Reduce audio file length
- Check system memory usage
- Consider using GPU acceleration (if available)

### Connection refused
- Ensure server is running: `curl http://localhost:9000/health`
- Check firewall settings
- Verify correct port (9000)

## Security Notes

- This API runs locally without authentication
- Do not expose port 9000 to the internet without proper security
- Audio files are temporarily stored during processing and then deleted
- No data is sent to external services 