#!/usr/bin/env python3
"""Regenerate the reference gmap with the CLI and compare it byte for byte."""
import hashlib
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCE = ROOT / "original" / "myworld.gmap"
OUTPUT = ROOT / "build" / "parity-myworld.gmap"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([str(ROOT / "bin" / "TerrainGenerator.exe"), str(SOURCE), str(OUTPUT), "--generate"], check=True)
    expected, actual = digest(SOURCE), digest(OUTPUT)
    print("parity: %s %s" % ("pass" if expected == actual else "fail", actual))
    return 0 if expected == actual else 1


if __name__ == "__main__":
    sys.exit(main())
