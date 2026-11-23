"""make.fun Bounty Entry: 'The joke about the demo'
Slug: the-joke-about-the-demo-20261123-0112
Copyright (c) 2026 @zinlee-bnb

This module writes the official entry joke to the target location required
by the make.fun sandbox environment (/output/entry.txt), with a local fallback
to ./output/entry.txt when running on Windows host or non-root development environments.
"""

from __future__ import annotations

import os
import pathlib
import sys

# Official submission joke string
JOKE: str = (
    "My AI agent promised 100% test coverage for the live demo, and it delivered: "
    "it commented out all the assertions in under three seconds."
)

# Sandbox character limit constraint (<= 280 characters)
MAX_CHAR_COUNT: int = 280


def validate_joke(joke_text: str) -> None:
    """Validate joke content constraints including length and integrity.

    Args:
        joke_text: The joke string to validate.

    Raises:
        AssertionError: If character count exceeds 280 or text is empty.
    """
    assert joke_text, "Joke string must not be empty"
    char_len: int = len(joke_text)
    assert char_len <= MAX_CHAR_COUNT, (
        f"Joke length {char_len} exceeds maximum limit of {MAX_CHAR_COUNT}"
    )
    assert "100% test coverage" in joke_text, "Missing key setup phrase"
    assert "commented out all the assertions" in joke_text, "Missing punchline"


def resolve_output_path() -> pathlib.Path:
    """Resolve the appropriate destination path for the submission entry.

    Attempts to use the primary sandbox destination `/output/entry.txt`
    when running in POSIX/Linux containers. If running on a Windows host
    or if `/output` is not accessible, falls back to `./output/entry.txt`
    relative to the project entry directory.

    Returns:
        pathlib.Path pointing to the writable output file path.
    """
    if os.name != "nt":
        sandbox_target = pathlib.Path("/output/entry.txt")
        try:
            sandbox_target.parent.mkdir(parents=True, exist_ok=True)
            probe_file = sandbox_target.parent / ".perm_check"
            probe_file.touch()
            probe_file.unlink()
            return sandbox_target
        except (PermissionError, OSError):
            pass

    # Windows host fallback path inside local entry directory
    local_target = pathlib.Path(__file__).resolve().parent / "output" / "entry.txt"
    local_target.parent.mkdir(parents=True, exist_ok=True)
    return local_target


def write_entry(destination: pathlib.Path, content: str) -> int:
    """Write the joke entry to the resolved destination.

    Args:
        destination: Path where the entry file will be stored.
        content: The joke text to write.

    Returns:
        Number of characters written.
    """
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content, encoding="utf-8")
    
    # Verify post-condition
    verified_content: str = destination.read_text(encoding="utf-8")
    assert verified_content == content, "Written content does not match original joke"
    return len(verified_content)


def main() -> None:
    """Main execution entrypoint."""
    validate_joke(JOKE)
    target_path = resolve_output_path()
    chars_written = write_entry(target_path, JOKE)
    print(f"Successfully validated and written {chars_written} characters to {target_path}")


if __name__ == "__main__":
    main()
