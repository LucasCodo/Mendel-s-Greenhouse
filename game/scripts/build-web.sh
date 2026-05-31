#!/usr/bin/env sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
GAME_DIR=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
BUILD_DIR="$GAME_DIR/dist/web-build"
STAGE_DIR="$BUILD_DIR/mendels-greenhouse"
WEB_DIR="$GAME_DIR/dist/web"
APP_FILE="$BUILD_DIR/mendels-greenhouse.pyxapp"
HTML_FILE="$BUILD_DIR/mendels-greenhouse.html"

python - "$BUILD_DIR" "$WEB_DIR" <<'PY'
from pathlib import Path
import shutil
import sys

for target in sys.argv[1:]:
    path = Path(target).resolve()
    if "dist" not in path.parts:
        raise SystemExit(f"Refusing to clear non-dist path: {path}")
    shutil.rmtree(path, ignore_errors=True)
PY

mkdir -p "$STAGE_DIR" "$WEB_DIR"

cd "$GAME_DIR"
poetry run poe build-assets

cp "$GAME_DIR/main.py" "$STAGE_DIR/main.py"
cp -R "$GAME_DIR/mendels_greenhouse" "$STAGE_DIR/mendels_greenhouse"

python - "$STAGE_DIR" <<'PY'
from pathlib import Path
import shutil
import sys

stage = Path(sys.argv[1])
for path in stage.rglob("__pycache__"):
    shutil.rmtree(path, ignore_errors=True)
for pattern in ("*.pyc", "*_preview.png"):
    for path in stage.rglob(pattern):
        path.unlink(missing_ok=True)
for relative in (
    "mendels_greenhouse/assets/gear_64.png",
    "mendels_greenhouse/assets/greenhouse_background_512x320.png",
    "mendels_greenhouse/assets/greenhouse_background_source.png",
):
    (stage / relative).unlink(missing_ok=True)
PY

cd "$BUILD_DIR"
poetry run pyxel package mendels-greenhouse mendels-greenhouse/main.py
poetry run pyxel app2html "$APP_FILE"

cp "$HTML_FILE" "$WEB_DIR/index.html"
printf "ok\n" > "$WEB_DIR/health.html"

echo "Built $WEB_DIR/index.html"
