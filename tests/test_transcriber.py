import pytest
from pathlib import Path
from ai_journal.transcriber import WhisperTranscriber

@pytest.fixture
def transcriber():
    return WhisperTranscriber()

def test_transcribe_valid_audio(transcriber):
    audio_path = Path("tests/test_audio.mp3")  # Replace with a valid test audio file path
    model_name = "medium.en"
    
    result = transcriber.transcribe(audio_path, model_name)
    
    assert isinstance(result, str)
    assert len(result) > 0  # Ensure that transcription is not empty

def test_transcribe_invalid_audio(transcriber):
    audio_path = Path("tests/invalid_audio.mp3")  # Replace with an invalid test audio file path
    model_name = "medium.en"
    
    with pytest.raises(Exception):
        transcriber.transcribe(audio_path, model_name)