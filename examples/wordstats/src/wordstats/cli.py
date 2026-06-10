"""Command-line interface for wordstats."""

import argparse
import logging
import sys
from pathlib import Path

from wordstats.core import top_words, word_count

logger = logging.getLogger(__name__)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="wordstats", description="Word statistics for a text file."
    )
    parser.add_argument("file", type=Path, help="Path to a UTF-8 text file.")
    parser.add_argument("--top", type=int, default=5, help="How many frequent words to show.")
    parser.add_argument("--verbose", action="store_true", help="Enable DEBUG logging.")
    return parser


def _configure_logging(verbose: bool) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        stream=sys.stderr,
        format="%(levelname)s %(name)s: %(message)s",
        force=True,
    )


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    _configure_logging(verbose=args.verbose)
    logger.debug("reading %s", args.file)
    try:
        text = args.file.read_text(encoding="utf-8")
    except OSError as exc:
        logger.error("cannot read %s: %s", args.file, exc)
        return 1
    logger.debug("computing stats (top=%d)", args.top)
    print(f"words: {word_count(text)}")
    for word, count in top_words(text, args.top):
        print(f"{word} ({count})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
