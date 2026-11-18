#!/usr/bin/env python3
"""Copy entry.png to the output directory.

Reads MAKEFUN_OUTPUT_DIR when set, otherwise /output. No network access,
standard library only, deterministic: the output is a byte-for-byte copy of
the entry.png shipped beside this file.
"""

import os
import shutil
from pathlib import Path


def main():
    here = Path(__file__).resolve().parent
    src = here / "entry.png"
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, out_dir / "entry.png")


if __name__ == "__main__":
    main()
