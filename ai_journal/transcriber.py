from pathlib import Path
import whisper



class WhisperTranscriber:
    def transcribe(self, audio_path: Path, model_name: str) -> str:
        """Transcribe audio using Whisper"""
        model = whisper.load_model(model_name)
        result = model.transcribe(
            str(audio_path),
            language="English",
            fp16=False
        )
        return result["text"]