import os
from datetime import datetime
from pathlib import Path

import typer
from rich.console import Console
from rich.progress import Progress

from ai_journal.recorder import AudioRecorder
from ai_journal.transcriber import WhisperTranscriber

app = typer.Typer()
console = Console()


@app.command()
def record(
    model: str = typer.Option("base", help="Whisper model to use")
):
    """Record and transcribe a journal entry"""
    console.print(f"[cyan]Recording journal entry using model: {model}")
    try:
        # Setup paths
        journal_dir = Path.home() / "journal"
        journal_dir.mkdir(exist_ok=True)

        date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_path = journal_dir / f"{date_str}.wav"

        console.print("[green]Recording...!")
        # Record audio
        recorder = AudioRecorder()
        recorder.record(audio_path, lambda: None)  # Simplified progress callback

        console.print("[green]Recording complete!")

        # Transcribe
        console.print("[cyan]Transcribing...")
        transcriber = WhisperTranscriber()
        text = transcriber.transcribe(audio_path, model)

        # Save transcription
        text_path = journal_dir / f"{date_str}.txt"
        text_path.write_text(text)

        # Cleanup audio
        # audio_path.unlink()

        console.print("[green]Journal entry completed successfully!")

        if os.name == "posix":  # macOS notification
            os.system(
                'osascript -e \'display notification "Transcription Complete!" with title "AI Journal"\''
            )

    except Exception as e:
        console.print(f"[red]Error: {str(e)}")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()