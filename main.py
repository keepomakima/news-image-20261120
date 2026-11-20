#!/usr/bin/env python3
"""news-image-20261120 v3 entrypoint.

Copies the front-page image (entry.png, built in-session by
build_frontpage_v3.py) to the output directory and verifies the copy is
byte-identical to the source. Standard library only.
"""
import hashlib
import os
import shutil
import sys


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    src_hash = sha256(src)
    dst_hash = sha256(dst)
    if src_hash != dst_hash:
        print("ERROR: copied bytes differ from source", file=sys.stderr)
        print("source %s" % src_hash, file=sys.stderr)
        print("copy   %s" % dst_hash, file=sys.stderr)
        return 1
    print("copied %s -> %s (%d bytes) sha256=%s"
          % (src, dst, os.path.getsize(dst), dst_hash))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
