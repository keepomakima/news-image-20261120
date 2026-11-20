#!/usr/bin/env python3
"""news-image-20261120 v2 entry point.

Copies the v2 front page (entry.png, 1024x1024, "ONE WORLD, ONE DAY"
for Friday 20 November 2026) into the harness output directory and
proves the copy is byte-identical to the source before exiting.
25 stories on the page: 1 lead (Kyiv) + 4 photo panels (Akvan,
Shenzhen, COP31, AI rout) + 20 one-line briefs.

Pure Python 3.13 standard library; no network, no third-party
packages. Deterministic: the same entry.png bytes are produced on
every run, so the emitted file's sha256 never changes.
"""
import hashlib
import os
import sys
from pathlib import Path


def pick_output_folder():
    """Harness output dir, or /output when the variable is unset."""
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    if not chosen:
        chosen = "/output"
    return Path(chosen)


def fingerprint(blob):
    return hashlib.sha256(blob).hexdigest()


def emit_entry():
    here = Path(__file__).resolve().parent
    source_path = here / "entry.png"
    payload = source_path.read_bytes()
    print(f"source: {source_path} ({len(payload)} bytes, "
          f"sha256 {fingerprint(payload)})")

    target_dir = pick_output_folder()
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / "entry.png"
    target_path.write_bytes(payload)

    echoed = target_path.read_bytes()
    if echoed != payload:
        print(f"ERROR: {target_path} does not match {source_path}",
              file=sys.stderr)
        return 1
    print(f"emitted: {target_path} ({len(echoed)} bytes, "
          f"sha256 {fingerprint(echoed)}) — verified identical")
    return 0


if __name__ == "__main__":
    sys.exit(emit_entry())
