from pathlib import Path

import pytest

from wordstats.cli import main


@pytest.fixture
def sample_file(tmp_path: Path, sample_text: str) -> Path:
    path = tmp_path / "sample.txt"
    path.write_text(sample_text, encoding="utf-8")
    return path


def test_summary_on_stdout(sample_file: Path, capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = main([str(sample_file), "--top", "2"])
    assert exit_code == 0
    out = capsys.readouterr().out
    assert "words: 12" in out
    assert "the (3)" in out


def test_missing_file_fails_cleanly(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = main([str(tmp_path / "nope.txt")])
    assert exit_code == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "nope.txt" in captured.err


def test_verbose_emits_debug_diagnostics_to_stderr(
    sample_file: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    main([str(sample_file), "--verbose"])
    assert "DEBUG" in capsys.readouterr().err


def test_default_quiet_on_stderr(sample_file: Path, capsys: pytest.CaptureFixture[str]) -> None:
    main([str(sample_file)])
    assert "DEBUG" not in capsys.readouterr().err
