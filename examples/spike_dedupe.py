# /// script
# requires-python = ">=3.13"
# ///
"""THROWAWAY SPIKE — do not merge, do not import.

Question probed: is stdlib difflib.SequenceMatcher good enough to flag
near-duplicate changelog lines, or do we need rapidfuzz?
Verdict recorded below after running; delete this file once decided.
"""

from difflib import SequenceMatcher

LINES = [
    "Fixed crash when config file is missing",
    "Fix crash when the config file is missing.",
    "Added --verbose flag to CLI",
    "Bumped ruff to 0.15",
    "Add --verbose flag to the CLI",
]


def main() -> None:
    for i, a in enumerate(LINES):
        for b in LINES[i + 1 :]:
            ratio = SequenceMatcher(None, a.lower(), b.lower()).ratio()
            if ratio > 0.7:
                print(f"{ratio:.2f}  {a!r} ~ {b!r}")


if __name__ == "__main__":
    main()

# VERDICT: difflib catches obvious near-dupes at ratio>0.85; word-order swaps
# score lower (~0.7). Good enough for changelog use; rapidfuzz unnecessary.
