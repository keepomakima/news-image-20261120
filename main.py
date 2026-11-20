#!/usr/bin/env python3
"""news-image-20261120 entry: ship the finished front page.

The front page itself (entry.png, 1024x1024, built in this session by
build_frontpage.py from six AI-generated text-free panels plus
PIL-typeset headlines) is committed next to this program. Running this
program copies that exact image, byte for byte, to the output path the
kit expects. No network, no randomness, no drawing at run time: two
runs always produce identical bytes.
"""
import hashlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"


def publish() -> Path:
    target_dir = Path(__import__("os").environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "entry.png"
    payload = SOURCE.read_bytes()
    if len(payload) > 1_048_576:
        raise SystemExit(f"entry.png too large: {len(payload)} bytes")
    target.write_bytes(payload)
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    print(f"wrote {target} ({len(payload)} bytes, sha256 {digest})")
    return target


if __name__ == "__main__":
    publish()
    sys.exit(0)
