"""Tests for the opencode HTML transcript extractor."""

import base64
import json
import subprocess
import sys
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "extract_opencode_transcript.py"


def _write_export(path: Path) -> None:
    session = {
        "header": {"version": 1},
        "leafId": "assistant-1",
        "systemPrompt": "test prompt",
        "tools": [],
        "entries": [
            {
                "type": "model_change",
                "id": "model-1",
                "provider": "opencode",
                "modelId": "test-model",
            },
            {
                "type": "message",
                "id": "user-1",
                "message": {
                    "role": "user",
                    "content": [{"type": "text", "text": "Add a feature."}],
                },
            },
            {
                "type": "message",
                "id": "assistant-1",
                "message": {
                    "role": "assistant",
                    "content": [
                        {"type": "thinking", "thinking": "hidden reasoning"},
                        {"type": "text", "text": "I will inspect the project."},
                        {
                            "type": "toolCall",
                            "id": "call-1",
                            "name": "read",
                            "arguments": {"path": "src/app.py"},
                        },
                    ],
                },
            },
            {
                "type": "message",
                "id": "result-1",
                "message": {
                    "role": "toolResult",
                    "toolName": "read",
                    "isError": False,
                    "content": [{"type": "text", "text": "print('hello')"}],
                },
            },
        ],
    }
    encoded = base64.b64encode(json.dumps(session).encode()).decode()
    path.write_text(
        f'<html><script id="session-data" type="application/json">{encoded}</script></html>',
        encoding="utf-8",
    )


def test_extracts_audit_focused_markdown(tmp_path: Path) -> None:
    source = tmp_path / "transcript.html"
    output = tmp_path / "transcript.md"
    _write_export(source)

    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(source), "--output", str(output)],
        capture_output=True,
        check=False,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    rendered = output.read_text(encoding="utf-8")
    assert "Provider: `opencode`" in rendered
    assert "Model: `test-model`" in rendered
    assert "## User\n\nAdd a feature." in rendered
    assert "## Assistant\n\nI will inspect the project." in rendered
    assert '### Tool: `read`\n\n```json\n{\n  "path": "src/app.py"' in rendered
    assert "### Tool result: `read`" in rendered
    assert "hidden reasoning" not in rendered


def test_rejects_html_without_session_data(tmp_path: Path) -> None:
    source = tmp_path / "invalid.html"
    source.write_text("<html></html>", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(source)],
        capture_output=True,
        check=False,
        text=True,
    )

    assert result.returncode != 0
    assert "session-data" in result.stderr
