import os
import pytest
from pathlib import Path
from ai_journal.recorder import AudioRecorder

@pytest.fixture
def audio_recorder():
    return AudioRecorder()

def test_recording_creates_audio_file(audio_recorder):
    output_path = Path.home() / "journal/test_audio.mp3"
    duration = 5  # seconds

    # Ensure the file does not exist before recording
    if output_path.exists():
        output_path.unlink()

    audio_recorder.record(output_path, duration)

    # Check if the audio file was created
    assert output_path.exists()

    # Cleanup
    output_path.unlink()

def test_recording_fails_with_invalid_duration(audio_recorder):
    output_path = Path.home() / "journal/test_audio.mp3"
    invalid_duration = -1  # Invalid duration

    with pytest.raises(Exception):
        audio_recorder.record(output_path, invalid_duration)

    # Ensure the file was not created
    assert not output_path.exists()