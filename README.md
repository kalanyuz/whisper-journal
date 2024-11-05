# Whisper Journal

Whisper Journal is an AI-powered audio journaling application that utilizes the Whisper model for transcription. This project allows users to record audio journal entries and automatically transcribe them into text files.

## Features

- Record audio entries with customizable duration.
- Transcribe audio using the Whisper model.
- Automatically save transcriptions as text files.
- Optionally commit and push entries to a Git repository.

## Installation

To install the project, you can use Poetry. First, ensure you have Poetry installed, then run:

```bash
poetry install
```

Alternatively, you can install the dependencies using pip:

```bash
pip install -r requirements.txt
```

## Usage

To record a journal entry, use the command line interface:

```bash
poetry run python -m ai_journal.cli
```

- `--model`: Whisper model to use for transcription (default is "medium.en").

## Testing

To run the tests, use:

```bash
poetry run pytest
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.