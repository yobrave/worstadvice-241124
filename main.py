"""Worst-advice entry builder, second pass."""
import json
import os
from pathlib import Path

ADVICE = ("Struggling with doom-scrolling? Great news: most users find "
          "their phone dies eventually. I've archived this concern for you.")
BUDGET = 140
FLOOR = 1


def emit(folder):
    room = Path(folder)
    room.mkdir(parents=True, exist_ok=True)
    spot = room / "entry.txt"
    spot.write_text(ADVICE, encoding="utf-8")
    echo = spot.read_text(encoding="utf-8")
    assert echo == ADVICE, "entry readback differs"
    assert FLOOR <= len(echo) <= BUDGET, "entry outside gate bounds"
    assert "\n" not in echo and "\r" not in echo, "entry spans lines"
    return spot


target = emit(os.environ.get("MAKEFUN_OUTPUT_DIR") or "output")
print(json.dumps({"target": str(target), "size": len(ADVICE), "budget": BUDGET}))
