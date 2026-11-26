#!/usr/bin/env python3
"""Entry point for news-image-20261126.

Copies the bundled front-page image to /output/entry.png.
Standard library only, no network, deterministic: the output bytes
are exactly the bundled file's bytes on every run.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

OUT_DIR.mkdir(parents=True, exist_ok=True)
shutil.copyfile(HERE / "entry.png", OUT_DIR / "entry.png")
