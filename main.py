"""Office joke entry: print one fixed joke line to /output/entry.txt.

The program holds a single pre-written office joke as a constant and
writes it out verbatim. Before writing, it sanity-checks the text
(length within the allowed window, not blank, encodable as UTF-8) so
a bad constant fails loudly instead of producing an invalid entry.
Only the Python standard library is used, and the output is fully
deterministic: same bytes on every run, no trailing newline.
"""

import hashlib
import os
import sys

# The joke itself. Kept as one plain string so what is checked below
# is exactly what lands on disk.
JOKE = (
    "The printer only jams when I'm already late, so I scheduled "
    "\u201cprinter time\u201d on my calendar \u2014 it's now the only "
    "meeting I never miss."
)

OUTPUT_PATH = "/output/entry.txt"
MIN_CHARS = 1
MAX_CHARS = 200


def validate(text):
    """Return an error message if text is not a legal entry, else None."""
    if not MIN_CHARS <= len(text) <= MAX_CHARS:
        return "entry must be %d-%d characters, got %d" % (
            MIN_CHARS,
            MAX_CHARS,
            len(text),
        )
    if not text.strip():
        return "entry must not be whitespace only"
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        return "entry is not encodable as UTF-8: %s" % exc
    return None


def main():
    problem = validate(JOKE)
    if problem is not None:
        raise SystemExit(problem)

    out_dir = os.path.dirname(OUTPUT_PATH)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    # newline="" keeps the file free of any platform line-ending
    # translation; the joke is written with no trailing newline.
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as handle:
        handle.write(JOKE)

    # Read-back verification: the bytes on disk must hash to exactly
    # the joke's sha256 digest; fail loudly on any drift.
    with open(OUTPUT_PATH, "rb") as handle:
        written = handle.read()
    if hashlib.sha256(written).digest() != hashlib.sha256(
        JOKE.encode("utf-8")
    ).digest():
        raise SystemExit("read-back mismatch: written bytes differ")
    return 0


if __name__ == "__main__":
    sys.exit(main())
