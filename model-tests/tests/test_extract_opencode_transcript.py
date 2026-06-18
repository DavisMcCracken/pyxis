"""Tests for the opencode HTML transcript extractor."""

import base64
import importlib.util
import json
from pathlib import Path

import pytest
from hypothesis import given
from hypothesis import strategies as st

SCRIPT = Path(__file__).parents[1] / "scripts" / "extract_opencode_transcript.py"

_spec = importlib.util.spec_from_file_location("extract_opencode_transcript", SCRIPT)
assert _spec is not None and _spec.loader is not None
extract = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(extract)


def _session() -> dict[str, object]:
    return {
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


def _write_export(path: Path, session: dict[str, object] | None = None) -> None:
    encoded = base64.b64encode(json.dumps(session or _session()).encode()).decode()
    path.write_text(
        f'<html><script id="session-data" type="application/json">{encoded}</script></html>',
        encoding="utf-8",
    )


def _assert_audit_content(rendered: str) -> None:
    assert "Provider: `opencode`" in rendered
    assert "Model: `test-model`" in rendered
    assert "## User\n\nAdd a feature." in rendered
    assert "## Assistant\n\nI will inspect the project." in rendered
    assert '### Tool: `read`\n\n```json\n{\n  "path": "src/app.py"' in rendered
    assert "### Tool result: `read`" in rendered
    assert "hidden reasoning" not in rendered


def test_extracts_audit_focused_markdown_to_file(tmp_path: Path) -> None:
    source = tmp_path / "transcript.html"
    output = tmp_path / "transcript.md"
    _write_export(source)

    assert extract.main([str(source), "--output", str(output)]) == 0
    _assert_audit_content(output.read_text(encoding="utf-8"))


def test_extracts_audit_focused_markdown_to_stdout(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "transcript.html"
    _write_export(source)

    assert extract.main([str(source)]) == 0
    captured = capsys.readouterr()
    _assert_audit_content(captured.out)


def test_rejects_html_without_session_data(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    source = tmp_path / "invalid.html"
    source.write_text("<html></html>", encoding="utf-8")

    with caplog.at_level("ERROR"):
        assert extract.main([str(source)]) == 1
    assert "session-data" in caplog.text


def test_rejects_missing_source(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    missing = tmp_path / "does-not-exist.html"

    with caplog.at_level("ERROR"):
        assert extract.main([str(missing)]) == 1
    assert caplog.text


@given(
    payload=st.text(
        alphabet=st.characters(codec="utf-8", exclude_categories=("Cs",)),
        max_size=64,
    )
)
def test_session_data_payload_never_crashes(
    tmp_path_factory: pytest.TempPathFactory, payload: str
) -> None:
    """Arbitrary session-data payloads parse to a dict or raise ValueError, never crash."""
    source = tmp_path_factory.mktemp("fuzz") / "transcript.html"
    source.write_text(
        f'<html><script id="session-data">{payload}</script></html>',
        encoding="utf-8",
    )
    try:
        result = extract.load_session_data(source)
    except ValueError:
        return
    assert isinstance(result, dict)
