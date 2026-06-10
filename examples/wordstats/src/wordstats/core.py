"""Pure text-statistics functions."""

import re
from collections import Counter

_WORD_RE = re.compile(r"\w+(?:'\w+)*")


def tokenize(text: str) -> list[str]:
    """Split text into lowercase word tokens, keeping internal apostrophes."""
    return _WORD_RE.findall(text.lower())


def word_count(text: str) -> int:
    """Count word tokens in text."""
    return len(tokenize(text))


def top_words(text: str, n: int) -> list[tuple[str, int]]:
    """Return the n most frequent words with counts, ties broken alphabetically.

    Raises:
        ValueError: If n is not positive.
    """
    if n <= 0:
        raise ValueError("n must be positive")
    counts = Counter(tokenize(text))
    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return ranked[:n]
