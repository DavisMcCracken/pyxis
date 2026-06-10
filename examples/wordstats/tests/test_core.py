from collections import Counter

import pytest
from hypothesis import given
from hypothesis import strategies as st

from wordstats.core import tokenize, top_words, word_count


class TestTokenize:
    @pytest.mark.parametrize(
        ("text", "expected"),
        [
            ("Hello world", ["hello", "world"]),
            ("", []),
            ("One", ["one"]),
            ("don't stop", ["don't", "stop"]),
            ("Tabs\tand\nnewlines", ["tabs", "and", "newlines"]),
            ("punct, only!!!", ["punct", "only"]),
            ("123 numbers 456", ["123", "numbers", "456"]),
        ],
    )
    def test_examples(self, text: str, expected: list[str]) -> None:
        assert tokenize(text) == expected

    @given(st.text())
    def test_tokens_lowercase_and_nonempty(self, text: str) -> None:
        for token in tokenize(text):
            assert token
            assert token == token.lower()


class TestWordCount:
    def test_sample(self, sample_text: str) -> None:
        assert word_count(sample_text) == 12

    @given(st.text())
    def test_equals_token_count(self, text: str) -> None:
        assert word_count(text) == len(tokenize(text))


class TestTopWords:
    def test_orders_by_count_then_alphabetically(self) -> None:
        assert top_words("b b a a c", 3) == [("a", 2), ("b", 2), ("c", 1)]

    def test_n_larger_than_vocab(self) -> None:
        assert top_words("a b a", 10) == [("a", 2), ("b", 1)]

    @pytest.mark.parametrize("n", [0, -1])
    def test_nonpositive_n_raises(self, n: int) -> None:
        with pytest.raises(ValueError, match="n must be positive"):
            top_words("a", n)

    @given(st.text(), st.integers(min_value=1, max_value=50))
    def test_counts_consistent_with_tokenize(self, text: str, n: int) -> None:
        counts = Counter(tokenize(text))
        result = top_words(text, n)
        assert len(result) <= n
        for word, count in result:
            assert counts[word] == count
        result_counts = [count for _, count in result]
        assert result_counts == sorted(result_counts, reverse=True)
