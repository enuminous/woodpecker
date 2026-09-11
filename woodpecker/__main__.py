from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from .core import evaluate


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="woodpecker",
        description="EFMW Zoo Animal #48 candidate — Take it out. Run it again."
    )
    parser.add_argument("case", type=Path, help="JSON case file")
    parser.add_argument("--pretty", action="store_true", help="pretty-print output JSON")
    args = parser.parse_args()

    raw = args.case.read_bytes()
    case = json.loads(raw.decode("utf-8"))
    result = evaluate(case).to_dict()
    result["input_sha256"] = hashlib.sha256(raw).hexdigest()

    print(json.dumps(result, indent=2 if args.pretty else None, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
