#!/usr/bin/env python3
"""news-image-20261120 v4 entrypoint: copy entry.png to the output dir.

Stdlib only, no network, deterministic. The image is pre-rendered by
build_frontpage_v4.py; this program only copies it byte for byte and
verifies the copy, then checks the competition's 1 MiB image cap.

The output directory is $MAKEFUN_OUTPUT_DIR when set, else /output.
"""

import hashlib
import os
import shutil

# The pre-rendered front page, shipped next to this file.
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# Competition cap from RULES.txt: the image must fit in 1 MiB.
MAX_BYTES = 1024 * 1024


def resolve_output_dir():
    """Return the directory the image must be written to."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    return out_dir


def read_bytes(path):
    """Read a file fully and return its bytes."""
    with open(path, "rb") as fh:
        return fh.read()


def copy_and_verify(src, dst):
    """Copy src to dst and prove the copy is byte-identical."""
    shutil.copyfile(src, dst)
    src_bytes = read_bytes(src)
    dst_bytes = read_bytes(dst)
    if src_bytes != dst_bytes:
        raise AssertionError("copied bytes differ from %s" % src)
    return dst_bytes


def check_cap(data):
    """Fail if the image exceeds the competition's 1 MiB cap."""
    if len(data) > MAX_BYTES:
        raise AssertionError(
            "entry.png is %d bytes, over the 1 MiB cap" % len(data))


def main():
    out_dir = resolve_output_dir()
    dst = os.path.join(out_dir, "entry.png")
    data = copy_and_verify(SRC, dst)
    check_cap(data)
    digest = hashlib.sha256(data).hexdigest()
    print("wrote %s (%d bytes) sha256=%s" % (dst, len(data), digest))


if __name__ == "__main__":
    main()
