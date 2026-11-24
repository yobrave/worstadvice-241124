"""Entry builder for Worst AI Advice: The 48-Hour Tight Line Open.

Loads the one-line advice from the repo, replays the gate rules
(1..140 chars, one line, not blank) and ships it to the output dir.
"""
import json
import os
import pathlib

CONFIG = {
    "entry_file": "entry.txt",
    "max_chars": 140,
    "encoding": "utf-8",
}

ENTRY = "Running low on storage? Delete your backups — you have not needed them yet, and past performance suggests that trend will continue."


def lint(text):
    body = text.strip()
    if not body:
        return False, "blank"
    if "\n" in body or "\r" in body:
        return False, "multiline"
    if len(body) > CONFIG["max_chars"]:
        return False, "over_limit"
    return True, "valid"


def main():
    home = pathlib.Path(__file__).resolve().parent
    stored = (home / CONFIG["entry_file"]).read_text(encoding=CONFIG["encoding"])
    if stored.strip() != ENTRY:
        raise SystemExit("entry drift: file and builder disagree")
    verdict, reason = lint(ENTRY)
    if not verdict:
        raise SystemExit(f"gate failed: {reason}")
    out_root = pathlib.Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_root.mkdir(parents=True, exist_ok=True)
    receipt = out_root / "entry.txt"
    receipt.write_text(ENTRY + "\n", encoding=CONFIG["encoding"])
    wire_size = len(receipt.read_bytes())
    print(json.dumps({"destination": str(receipt), "chars": len(ENTRY), "bytes": wire_size, "gate": reason}))


if __name__ == "__main__":
    main()
