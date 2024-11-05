import os
import pytest
from typer.testing import CliRunner
from ai_journal.cli import app

runner = CliRunner()

def test_record():
    result = runner.invoke(app, ["record", "--duration", "5", "--model", "medium.en", "--push", "False"])
    assert result.exit_code == 0
    assert "Journal entry completed successfully!" in result.output

def test_record_invalid_duration():
    result = runner.invoke(app, ["record", "--duration", "-1"])
    assert result.exit_code != 0
    assert "Error:" in result.output

def test_record_invalid_model():
    result = runner.invoke(app, ["record", "--model", "invalid_model"])
    assert result.exit_code != 0
    assert "Error:" in result.output