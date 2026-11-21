#!/usr/bin/env python3
"""news-image-20261120 v4 entrypoint: copy entry.png to the output dir.

Stdlib only, no network, deterministic. The image is pre-rendered; this
program only copies it byte for byte and verifies the copy.
"""
import hashlib
import os
import shutil
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    with open(SRC, "rb") as fh:
        src_bytes = fh.read()
    with open(dst, "rb") as fh:
        dst_bytes = fh.read()
    assert src_bytes == dst_bytes, "copied bytes differ from entry.png"
    print("wrote %s (%d bytes) sha256=%s" % (
        dst, len(dst_bytes), hashlib.sha256(dst_bytes).hexdigest()))


if __name__ == "__main__":
    main()
