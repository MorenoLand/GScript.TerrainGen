# Cross-platform terrain generator that reproduces Graal's `.gmap` and level files

TerrainGenerator builds Graal terrain maps from a map seed and settings, previews the result, and
saves the `.gmap` plus optional `.nw` level files. It reimplements the original 2003 generator's
deterministic terrain pipeline in C++20 with a raylib interface, so the generated map data matches
the original byte for byte.

## Build

Requires CMake 3.20 or newer and a C++20 compiler.

```sh
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release --parallel
```

The executable is written to `bin/TerrainGenerator.exe` on Windows and `bin/TerrainGenerator` on
Linux. raylib and tinyfiledialogs are fetched by CMake.

## Run

```sh
bin/TerrainGenerator
```

Set a seed and generator options, then use **Generate World**. The save button writes the `.gmap`;
with **Generate Graal levels** enabled it also writes one `.nw` file per level. The zoom controls
show individual level detail, where terrain vertices can be edited.

For batch use:

```sh
bin/TerrainGenerator input.gmap output.gmap --generate
```

## Tests

```sh
ctest --test-dir build -C Release --output-on-failure
bin/TerrainGenerator --self-test
```

`tests/terrain_parity.py` regenerates `tests/reference/myworld.gmap` and compares it byte for byte.
`ctest` runs it when Python is available.

`tests/zoom_parity.py` checks the zoom projection constants against the recomp renderer
`f_0044d848`; `ctest` runs it when Python is available.

## Format and pipeline

`docs/terrain-generation.md` documents the seed stream, control grid, border expansion, level
generation, height overrides, preview shading, and the `.gmap` layout.

The serializer writes CRLF line endings and the original's trailing blank line; both are part of
the format. The reference map hashes to
`1E1E23AD013D8F10B746D094F79B3B97BDE69144FBCECAB693316A06B1423C22`.
