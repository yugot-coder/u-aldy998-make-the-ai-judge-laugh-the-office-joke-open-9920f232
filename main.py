#!/usr/bin/env python3
"""Make the AI Judge Laugh: the Office Joke Open.

Writes a single one-line office joke (131 characters) to /output/entry.txt.
Standard library only; deterministic; no trailing newline.
"""

import os

JOKE = (
    "The printer only jams when I'm already late, so I scheduled "
    "\u201cprinter time\u201d on my calendar \u2014 it's now the only "
    "meeting I never miss."
)

OUTPUT_PATH = "/output/entry.txt"


def main() -> None:
    text = JOKE
    # Gate: /output/entry.txt must be UTF-8 text of 1-200 characters,
    # not only whitespace. Count every character, newline included
    # (this text has none).
    if not 1 <= len(text) <= 200:
        raise SystemExit(
            "entry must be 1-200 characters, got %d" % len(text)
        )
    if not text.strip():
        raise SystemExit("entry must not be only whitespace")
    text.encode("utf-8")  # fail loudly if not valid UTF-8
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(text)


if __name__ == "__main__":
    main()
