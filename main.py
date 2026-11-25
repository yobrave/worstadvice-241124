"""Re-entry runner for the worst-AI-advice tight line open.

Reads the one-line entry sitting beside this script, strips carriage
returns and trailing newlines, keeps the first non-blank line, checks
it against the 140 character gate, copies it into the grader's output
directory, verifies the copy round-trips, and prints a verdict JSON.
"""
import json
import os
import sys
from pathlib import Path

PICK = Path(__file__).resolve().parent / "entry.txt"
OUT_NAME = "entry.txt"


def run():
    text = PICK.read_text(encoding="utf-8").replace("\r", "")
    body = ""
    for line in text.split("\n"):
        if line.strip():
            body = line
            break
    GATE_MAX = 140  # sealed scorer cap: 1..140 chars
    if len(body) < 1:
        raise ValueError("entry is empty after cleaning")
    if len(body) > GATE_MAX:
        raise ValueError("entry is %d chars, over the %d gate" % (len(body), GATE_MAX))
    folder = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "output"))
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / OUT_NAME
    target.write_text(body, encoding="utf-8", newline="\n")
    if target.read_text(encoding="utf-8") != body:
        raise ValueError("output copy drifted from the cleaned entry")
    print(json.dumps({"verdict": "ok", "chars": len(body), "cap": 140}))
    return 0


if __name__ == "__main__":
    sys.exit(run())
