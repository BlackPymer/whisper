#!/usr/bin/env python3
"""
Demo script to test the Whisper API endpoints.
Make sure the server is running before executing this script.
"""


import requests

# API base URL
BASE_URL = "http://localhost:9000"


def test_health_endpoint():
    """Test the health endpoint."""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check passed!")
            print(f"   Status: {data['status']}")
            print(f"   Whisper Model: {data['whisper_model']}")
        else:
            print(f"❌ Health check failed with status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running on port 9000.")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    return True


def test_transcribe_endpoint():
    """Test the transcribe endpoint with invalid data."""
    print("\nTesting transcribe endpoint with invalid file...")
    try:
        # Test with invalid file (should return 400)
        files = {"audio_file": ("test.txt", b"invalid content", "text/plain")}
        response = requests.post(f"{BASE_URL}/transcribe", files=files)

        if response.status_code == 400:
            data = response.json()
            print(f"✅ Expected validation error: {data['detail']}")
        else:
            print(f"❌ Expected 400 but got {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")


def show_api_info():
    """Show API documentation links."""
    print("\n📖 API Documentation:")
    print(f"   Swagger UI: {BASE_URL}/docs")
    print(f"   ReDoc: {BASE_URL}/redoc")
    print("\n🎤 To transcribe an audio file, use:")
    print(f"   curl -X POST '{BASE_URL}/transcribe' \\")
    print("     -H 'accept: application/json' \\")
    print("     -H 'Content-Type: multipart/form-data' \\")
    print("     -F 'audio_file=@your_audio_file.wav'")


if __name__ == "__main__":
    print("🎯 Whisper API Demo")
    print("=" * 50)

    if test_health_endpoint():
        test_transcribe_endpoint()
        show_api_info()
        print(f"\n✨ Server is running successfully at {BASE_URL}")
    else:
        print("\n💡 Start the server with: ./run_local.sh")
        print("   Or use: make run")
