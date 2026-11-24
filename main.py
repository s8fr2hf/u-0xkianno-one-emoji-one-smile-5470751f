"""One Emoji, One Smile: the hugging face.

The entry is a single emoji, U+1F917 (hugging face): two open hands
offering a hug around a warm smile. A hug is the plainest gesture of
warmth a stranger can read at a glance -- friendly, not romantic, no
irony and no in-joke -- and it feels deliberately picked for the
moment rather than the first smiley that comes to mind.
"""

import os
import sys

EMOJI = "\U0001F917"  # hugging face


def resolve_out_dir() -> str:
    """Prefer MAKEFUN_OUTPUT_DIR, then /output, then a local ./output.

    The grader sandbox provides MAKEFUN_OUTPUT_DIR (or /output); falling
    back keeps the program runnable when neither exists or is writable.
    Never chmod a directory: in the sandbox it may belong to root.
    """
    candidates = [
        os.environ.get("MAKEFUN_OUTPUT_DIR"),
        "/output",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "output"),
    ]
    for cand in candidates:
        if not cand:
            continue
        try:
            os.makedirs(cand, exist_ok=True)
            probe = os.path.join(cand, ".write-test")
            with open(probe, "w", encoding="utf-8") as f:
                f.write("")
            os.remove(probe)
            return cand
        except OSError:
            continue
    raise OSError("no writable output directory found")


def main() -> int:
    out_dir = resolve_out_dir()
    path = os.path.join(out_dir, "entry.txt")
    # Atomic write: a crash mid-write can never leave a truncated entry.
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8", newline="") as f:
        f.write(EMOJI)
    os.replace(tmp_path, path)
    # Self-check: the gate requires 1-8 UTF-8 characters, not whitespace.
    with open(path, "rb") as f:
        raw = f.read()
    text = raw.decode("utf-8")
    if len(text) != 1 or text.isspace():
        print(f"invalid entry: {raw!r}", file=sys.stderr)
        return 1
    print(f"wrote {path}: {text!r} ({len(raw)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
