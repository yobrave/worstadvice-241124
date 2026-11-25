# Worst AI Advice entry pipeline: validate one-liner, emit to output dir.
import os, sys, json, shutil

MAXLEN = 140
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.txt")
BUILD = "wad4-worst-advice-r4"


def load():
    with open(SRC, encoding="utf-8") as fh:
        return fh.read().strip()


def emit(text):
    out = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out, exist_ok=True)
    shutil.copyfile(SRC, os.path.join(out, "entry.txt"))


text = load()
if not 1 <= len(text) <= MAXLEN:
    sys.exit("gate reject: %d chars" % len(text))
emit(text)
print(json.dumps({"ok": True, "build": BUILD, "size": len(text), "cap": MAXLEN}))
