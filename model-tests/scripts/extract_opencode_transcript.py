# /// script
# requires-python = ">=3.12"
# ///
"""Extract an audit-focused Markdown transcript from an opencode HTML export.

The expected input is an opencode `transcript.html` export. The embedded
`<script id="session-data">` element holds a base64-encoded JSON payload whose
shape (as of the opencode exports this targets) is::

    {
      "entries": [
        {"type": "model_change", "provider": "...", "modelId": "..."},
        {"type": "message", "message": {"role": "user",
            "content": [{"type": "text", "text": "..."}]}},
        {"type": "message", "message": {"role": "assistant",
            "content": [{"type": "text", "text": "..."},
                        {"type": "toolCall", "name": "...",
                         "arguments": {...}}]}},
        {"type": "message", "message": {"role": "toolResult",
            "toolName": "...", "isError": false,
            "content": [{"type": "text", "text": "..."}]}}
      ]
    }

If opencode changes this schema, the renderer silently skips unrecognized
blocks; update the parsing below and the test fixture together.
"""

import argparse
import base64
import binascii
import json
import logging
import sys
from html.parser import HTMLParser
from pathlib import Path

logger = logging.getLogger(__name__)


type JsonValue = None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]


class _SessionDataParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._inside_session_data = False
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "script":
            return
        attributes = dict(attrs)
        self._inside_session_data = attributes.get("id") == "session-data"

    def handle_endtag(self, tag: str) -> None:
        if tag == "script":
            self._inside_session_data = False

    def handle_data(self, data: str) -> None:
        if self._inside_session_data:
            self.parts.append(data)


def _object(value: JsonValue, context: str) -> dict[str, JsonValue]:
    if not isinstance(value, dict):
        raise ValueError(f"expected object for {context}")
    return value


def _items(value: JsonValue, context: str) -> list[JsonValue]:
    if not isinstance(value, list):
        raise ValueError(f"expected list for {context}")
    return value


def _text(value: JsonValue) -> str | None:
    return value if isinstance(value, str) else None


def load_session_data(source: Path) -> dict[str, JsonValue]:
    """Load the embedded session payload from an opencode HTML export."""
    parser = _SessionDataParser()
    parser.feed(source.read_text(encoding="utf-8"))
    encoded = "".join(parser.parts).strip()
    if not encoded:
        raise ValueError("HTML export does not contain a session-data script")

    try:
        payload = base64.b64decode(encoded, validate=True).decode("utf-8")
        parsed: JsonValue = json.loads(payload)
    except (binascii.Error, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("session-data payload is not valid base64-encoded JSON") from exc
    return _object(parsed, "session-data")


def _append_text_block(lines: list[str], heading: str, value: JsonValue) -> None:
    content = _text(value)
    if content and content.strip():
        lines.extend([heading, "", content.strip(), ""])


def _render_tool_call(lines: list[str], block: dict[str, JsonValue]) -> None:
    name = _text(block.get("name")) or "unknown"
    arguments = block.get("arguments")
    lines.extend(
        [
            f"### Tool: `{name}`",
            "",
            "```json",
            json.dumps(arguments, indent=2, ensure_ascii=False),
            "```",
            "",
        ]
    )


def render_markdown(session: dict[str, JsonValue]) -> str:
    """Render user, assistant, and tool events without hidden reasoning."""
    entries = _items(session.get("entries"), "entries")
    provider = "unknown"
    model = "unknown"

    for raw_entry in entries:
        entry = _object(raw_entry, "entry")
        if entry.get("type") == "model_change":
            provider = _text(entry.get("provider")) or provider
            model = _text(entry.get("modelId")) or model
            break

    lines = [
        "# Extracted opencode transcript",
        "",
        f"Provider: `{provider}`",
        f"Model: `{model}`",
        "",
    ]

    for raw_entry in entries:
        entry = _object(raw_entry, "entry")
        if entry.get("type") != "message":
            continue
        message = _object(entry.get("message"), "message")
        role = _text(message.get("role"))
        content = _items(message.get("content"), "message content")

        if role == "user":
            for raw_block in content:
                block = _object(raw_block, "user content")
                if block.get("type") == "text":
                    _append_text_block(lines, "## User", block.get("text"))
        elif role == "assistant":
            for raw_block in content:
                block = _object(raw_block, "assistant content")
                if block.get("type") == "text":
                    _append_text_block(lines, "## Assistant", block.get("text"))
                elif block.get("type") == "toolCall":
                    _render_tool_call(lines, block)
        elif role == "toolResult":
            name = _text(message.get("toolName")) or "unknown"
            status = " (error)" if message.get("isError") is True else ""
            for raw_block in content:
                block = _object(raw_block, "tool result content")
                if block.get("type") == "text":
                    _append_text_block(
                        lines,
                        f"### Tool result: `{name}`{status}",
                        block.get("text"),
                    )

    return "\n".join(lines).rstrip() + "\n"


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="opencode transcript.html export")
    parser.add_argument("--output", type=Path, help="write Markdown to this path")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="enable debug logging to stderr",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the transcript extraction CLI."""
    args = _build_parser().parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
        stream=sys.stderr,
    )
    try:
        logger.debug("loading session data from %s", args.source)
        rendered = render_markdown(load_session_data(args.source))
        if args.output is None:
            sys.stdout.write(rendered)
        else:
            args.output.write_text(rendered, encoding="utf-8")
            logger.debug("wrote %d characters to %s", len(rendered), args.output)
    except (OSError, ValueError) as exc:
        logger.error("%s", exc)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
