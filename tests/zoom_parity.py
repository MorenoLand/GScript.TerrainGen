#!/usr/bin/env python3
"""Check the remake zoom constants against the recomp renderer f_0044d848."""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCE = ROOT / "src" / "terrain_editor_ui.cpp"

# f_0044d848: [0x452700]=20, origin=round([0x4526d4]/[0x4526e8])+20.
# .data: [0x4526d4]=65.0, [0x4526e8]=3.0; Panel1.Left=480.
MAP_MARGIN = 20
PANEL_LEFT = 480
EXPECTED_ORIGIN = round(65.0 / 3.0) + MAP_MARGIN
EXPECTED_WIDTH = PANEL_LEFT - MAP_MARGIN * 2
EXPECTED_HEIGHT = PANEL_LEFT - EXPECTED_ORIGIN * 2
EXPECTED_TOP = EXPECTED_ORIGIN + 30
EXPECTED_DIVISOR = 1.0


def main():
    text = SOURCE.read_text(encoding="utf-8")
    values = {name: int(value) for name, value in re.findall(r"\b(zoom_left|zoom_grid_width|zoom_grid_height|zoom_top|terrain_width|terrain_height|terrain_top)\s*=\s*(\d+)", text)}
    checks = {
        "zoom_left": (values.get("zoom_left"), MAP_MARGIN),
        "zoom_grid_width": (values.get("zoom_grid_width"), EXPECTED_WIDTH),
        "zoom_grid_height": (values.get("zoom_grid_height"), EXPECTED_HEIGHT),
        "zoom_top": (values.get("zoom_top"), EXPECTED_TOP),
        "terrain_width": (values.get("terrain_width"), EXPECTED_WIDTH),
        "terrain_height": (values.get("terrain_height"), EXPECTED_HEIGHT),
        "terrain_top": (values.get("terrain_top"), EXPECTED_TOP),
    }
    for name, (actual, expected) in checks.items():
        if actual != expected:
            print("zoom parity: fail %s %s != %s" % (name, actual, expected))
            return 1
    if "height_divisor=1.0f" not in text:
        print("zoom parity: fail height_divisor")
        return 1
    if "(std::min)(4,pw-ox)" not in text or "vw*8" not in text:
        print("zoom parity: fail 4x4/8x8 grid")
        return 1
    if "Color{128,0,0,255}" not in text or "yy+=2.0f" not in text:
        print("zoom parity: fail maroon dot grid")
        return 1
    print("zoom parity: pass origin=%d width=%d height=%d divisor=%g" % (EXPECTED_ORIGIN, EXPECTED_WIDTH, EXPECTED_HEIGHT, EXPECTED_DIVISOR))
    return 0


if __name__ == "__main__":
    sys.exit(main())
