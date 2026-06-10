import pytest


@pytest.fixture
def sample_text() -> str:
    return "The quick brown fox jumps over the lazy dog. The dog sleeps."
