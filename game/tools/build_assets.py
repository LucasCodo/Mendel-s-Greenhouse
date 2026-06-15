"""Build Pyxel resources for Mendel's Greenhouse."""

import sys
from dataclasses import dataclass
from pathlib import Path

import pyxel

from mendels_greenhouse.scenes.main_game import HEIGHT, WIDTH
from mendels_greenhouse.ui.palette import PROJECT_PALETTE, PyxelColor

ASSETS_DIR = (
    Path(__file__).resolve().parents[1] / "mendels_greenhouse" / "assets"
)
PYXRES_PATH = ASSETS_DIR / "mendels_greenhouse.pyxres"
FONT_PATH = ASSETS_DIR / "mendel_5x7.bdf"
POD_SHADOW_START_ROW = 18
POD_HIGHLIGHT_END_ROW = 13
MIN_INTERIOR_LINE_WIDTH = 2
PLANT_SPRITE_W = 56
PLANT_SPRITE_H = 44
ICON_SIZE = 64

PLANT_SPRITES = {
    ("yellow", "smooth"): (0, 0),
    ("yellow", "wrinkled"): (64, 0),
    ("green", "smooth"): (128, 0),
    ("green", "wrinkled"): (192, 0),
}
SPECIES_PLANT_SPRITES = {
    "Snapdragon": (0, 192),
    "Corn": (64, 192),
    "Tomato": (128, 192),
    "Orchid": (192, 192),
}

ICONS = {
    "guide": (0, 64),
    "garden": (64, 64),
    "shop": (128, 64),
    "settings": (192, 64),
    "coin": (0, 128),
    "seed": (64, 128),
    "contract": (128, 128),
}


@dataclass(frozen=True)
class SeedStyle:
    """Visual colors and texture for a seed cluster."""

    color: int
    shadow: int
    texture: str


@dataclass(frozen=True)
class PodStyle:
    """Visual style for a pea pod."""

    shadow: int
    base: int
    highlight: int
    seed: SeedStyle


GLYPHS = {
    " ": ["00000"] * 7,
    "!": ["00100", "00100", "00100", "00100", "00100", "00000", "00100"],
    "'": ["00100", "00100", "01000", "00000", "00000", "00000", "00000"],
    "%": ["11001", "11010", "00100", "01000", "10110", "00110", "00000"],
    "(": ["00010", "00100", "01000", "01000", "01000", "00100", "00010"],
    ")": ["01000", "00100", "00010", "00010", "00010", "00100", "01000"],
    "*": ["00000", "10101", "01110", "11111", "01110", "10101", "00000"],
    "+": ["00000", "00100", "00100", "11111", "00100", "00100", "00000"],
    ",": ["00000", "00000", "00000", "00000", "00110", "00100", "01000"],
    "-": ["00000", "00000", "00000", "11110", "00000", "00000", "00000"],
    "/": ["00001", "00010", "00010", "00100", "01000", "01000", "10000"],
    ":": ["00000", "00100", "00100", "00000", "00100", "00100", "00000"],
    "<": ["00010", "00100", "01000", "10000", "01000", "00100", "00010"],
    "=": ["00000", "00000", "11111", "00000", "11111", "00000", "00000"],
    ">": ["01000", "00100", "00010", "00001", "00010", "00100", "01000"],
    "?": ["01110", "10001", "00001", "00010", "00100", "00000", "00100"],
    ".": ["00000", "00000", "00000", "00000", "00000", "01100", "01100"],
    "0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    "2": ["01110", "10001", "00001", "00010", "00100", "01000", "11111"],
    "3": ["11110", "00001", "00001", "01110", "00001", "00001", "11110"],
    "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    "5": ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    "6": ["00110", "01000", "10000", "11110", "10001", "10001", "01110"],
    "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    "9": ["01110", "10001", "10001", "01111", "00001", "00010", "11100"],
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "C": ["01111", "10000", "10000", "10000", "10000", "10000", "01111"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    "G": ["01111", "10000", "10000", "10011", "10001", "10001", "01111"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "I": ["01110", "00100", "00100", "00100", "00100", "00100", "01110"],
    "J": ["00111", "00010", "00010", "00010", "10010", "10010", "01100"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "Q": ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    "V": ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    "W": ["10001", "10001", "10001", "10101", "10101", "10101", "01010"],
    "X": ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    "Z": ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    "a": ["00000", "00000", "01110", "00001", "01111", "10001", "01111"],
    "b": ["10000", "10000", "10110", "11001", "10001", "10001", "11110"],
    "c": ["00000", "00000", "01111", "10000", "10000", "10000", "01111"],
    "d": ["00001", "00001", "01101", "10011", "10001", "10001", "01111"],
    "e": ["00000", "00000", "01110", "10001", "11111", "10000", "01111"],
    "f": ["00110", "01001", "01000", "11100", "01000", "01000", "01000"],
    "g": ["00000", "00000", "01111", "10001", "01111", "00001", "01110"],
    "h": ["10000", "10000", "10110", "11001", "10001", "10001", "10001"],
    "i": ["00100", "00000", "01100", "00100", "00100", "00100", "01110"],
    "j": ["00010", "00000", "00110", "00010", "00010", "10010", "01100"],
    "k": ["10000", "10000", "10010", "10100", "11000", "10100", "10010"],
    "l": ["01100", "00100", "00100", "00100", "00100", "00100", "01110"],
    "m": ["00000", "00000", "11010", "10101", "10101", "10101", "10101"],
    "n": ["00000", "00000", "10110", "11001", "10001", "10001", "10001"],
    "o": ["00000", "00000", "01110", "10001", "10001", "10001", "01110"],
    "p": ["00000", "00000", "11110", "10001", "11110", "10000", "10000"],
    "q": ["00000", "00000", "01111", "10001", "01111", "00001", "00001"],
    "r": ["00000", "00000", "10110", "11001", "10000", "10000", "10000"],
    "s": ["00000", "00000", "01111", "10000", "01110", "00001", "11110"],
    "t": ["01000", "01000", "11100", "01000", "01000", "01001", "00110"],
    "u": ["00000", "00000", "10001", "10001", "10001", "10011", "01101"],
    "v": ["00000", "00000", "10001", "10001", "10001", "01010", "00100"],
    "w": ["00000", "00000", "10001", "10001", "10101", "10101", "01010"],
    "x": ["00000", "00000", "10001", "01010", "00100", "01010", "10001"],
    "y": ["00000", "00000", "10001", "10001", "01111", "00001", "01110"],
    "z": ["00000", "00000", "11111", "00010", "00100", "01000", "11111"],
}


def main() -> None:
    """Generate the Pyxel resource file and companion font."""
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    _write_bdf_font()
    pyxel.init(WIDTH, HEIGHT)
    pyxel.colors[:] = PROJECT_PALETTE
    _draw_image_bank()
    _build_audio()
    pyxel.save(str(PYXRES_PATH))
    sys.stdout.write(f"built {PYXRES_PATH}\n")
    sys.stdout.write(f"built {FONT_PATH}\n")


def _draw_image_bank() -> None:
    pyxel.images[0].cls(0)
    _draw_plant_variants()
    _draw_species_variants()
    _draw_icons()


def _draw_plant_variants() -> None:
    for traits, (u, v) in PLANT_SPRITES.items():
        color, texture = traits
        _draw_plant_sprite(u, v, color, texture)


def _draw_species_variants() -> None:
    for species, (u, v) in SPECIES_PLANT_SPRITES.items():
        pyxel.images[0].rect(u, v, 64, 64, 0)
        if species == "Snapdragon":
            _snapdragon_sprite(u, v)
        elif species == "Corn":
            _corn_sprite(u, v)
        elif species == "Tomato":
            _tomato_sprite(u, v)
        else:
            _orchid_sprite(u, v)


def _draw_plant_sprite(u: int, v: int, color: str, texture: str) -> None:
    image = pyxel.images[0]
    image.rect(u, v, 64, 64, 0)
    seed_col = (
        PyxelColor.PEA_YELLOW if color == "yellow" else PyxelColor.PEA_GREEN
    )
    seed_shadow = (
        PyxelColor.TERRACOTTA if color == "yellow" else PyxelColor.POD_SHADOW
    )
    seed_style = SeedStyle(seed_col, seed_shadow, texture)
    pod_style = PodStyle(
        PyxelColor.POD_SHADOW,
        PyxelColor.POD_BASE,
        PyxelColor.POD_HIGHLIGHT,
        seed_style,
    )
    _pod(image, u + 2, v + 4, pod_style)


def _snapdragon_sprite(u: int, v: int) -> None:
    image = pyxel.images[0]
    _pot(image, u + 21, v + 47)
    _stem(image, u + 32, v + 18)
    _leaf_cluster(image, u + 29, v + 37, flip=True)
    _leaf_cluster(image, u + 34, v + 31, flip=False)
    _flower(image, u + 32, v + 18, PyxelColor.TOMATO_RED)
    image.circ(u + 25, v + 23, 5, PyxelColor.SPRITE_OUTLINE)
    image.circ(u + 25, v + 23, 4, PyxelColor.PINK_FLOWER)
    image.circ(u + 40, v + 24, 5, PyxelColor.SPRITE_OUTLINE)
    image.circ(u + 40, v + 24, 4, PyxelColor.PINK_FLOWER)


def _corn_sprite(u: int, v: int) -> None:
    image = pyxel.images[0]
    _pot(image, u + 21, v + 47)
    image.rect(u + 29, v + 8, 7, 42, PyxelColor.SPRITE_OUTLINE)
    image.rect(u + 31, v + 9, 3, 40, PyxelColor.CORN_HUSK)
    for y in [16, 24, 32, 40]:
        image.tri(
            u + 31,
            v + y,
            u + 11,
            v + y + 11,
            u + 30,
            v + y + 4,
            PyxelColor.LEAF_GREEN,
        )
        image.tri(
            u + 34,
            v + y - 2,
            u + 53,
            v + y + 8,
            u + 35,
            v + y + 3,
            PyxelColor.LEAF_HIGHLIGHT,
        )
    image.rect(u + 27, v + 19, 11, 20, PyxelColor.SPRITE_OUTLINE)
    image.rect(u + 29, v + 21, 7, 16, PyxelColor.CORN_YELLOW)
    for row in range(22, 36, 4):
        image.line(u + 30, v + row, u + 35, v + row, PyxelColor.TERRACOTTA)


def _tomato_sprite(u: int, v: int) -> None:
    image = pyxel.images[0]
    _pot(image, u + 21, v + 47)
    _stem(image, u + 32, v + 20)
    for x, y in [(23, 26), (40, 24), (31, 17)]:
        image.line(u + 32, v + 31, u + x, v + y, PyxelColor.POD_SHADOW)
        image.circ(u + x, v + y, 7, PyxelColor.SPRITE_OUTLINE)
        image.circ(u + x, v + y, 5, PyxelColor.TOMATO_RED_BRIGHT)
        image.pset(u + x - 2, v + y - 3, PyxelColor.PARCHMENT_LIGHT)
    _leaf_cluster(image, u + 29, v + 39, flip=True)
    _leaf_cluster(image, u + 35, v + 34, flip=False)


def _orchid_sprite(u: int, v: int) -> None:
    image = pyxel.images[0]
    _pot(image, u + 21, v + 47)
    _stem(image, u + 32, v + 20)
    image.line(u + 32, v + 24, u + 45, v + 12, PyxelColor.POD_SHADOW)
    image.line(u + 32, v + 27, u + 19, v + 14, PyxelColor.POD_SHADOW)
    _orchid_flower(image, u + 45, v + 12)
    _orchid_flower(image, u + 19, v + 14)
    _leaf_cluster(image, u + 28, v + 40, flip=True)
    _leaf_cluster(image, u + 35, v + 36, flip=False)


def _orchid_flower(image: pyxel.Image, x: int, y: int) -> None:
    image.circ(x, y - 5, 5, PyxelColor.SPRITE_OUTLINE)
    image.circ(x - 6, y, 5, PyxelColor.SPRITE_OUTLINE)
    image.circ(x + 6, y, 5, PyxelColor.SPRITE_OUTLINE)
    image.circ(x, y + 5, 5, PyxelColor.SPRITE_OUTLINE)
    image.circ(x, y - 5, 3, PyxelColor.ORCHID_VIOLET)
    image.circ(x - 5, y, 3, PyxelColor.ORCHID_VIOLET)
    image.circ(x + 5, y, 3, PyxelColor.ORCHID_VIOLET)
    image.circ(x, y + 4, 3, PyxelColor.PINK_FLOWER)
    image.circ(x, y, 2, PyxelColor.ACCENT)


def _leaf_cluster(image: pyxel.Image, x: int, y: int, *, flip: bool) -> None:
    direction = -1 if flip else 1
    origin = x - 9 if flip else x
    image.elli(origin, y - 4, 16, 9, PyxelColor.GREENHOUSE_BG)
    image.elli(origin + 1, y - 3, 14, 7, PyxelColor.PEA_GREEN)
    image.line(x, y, x + direction * 11, y - 2, PyxelColor.ACCENT)
    image.pset(x + direction * 4, y - 3, PyxelColor.ACCENT)


def _pot(image: pyxel.Image, x: int, y: int) -> None:
    image.rect(x + 2, y + 1, 18, 5, PyxelColor.FRAME)
    image.rect(x + 4, y + 5, 14, 3, PyxelColor.FRAME)
    image.rect(x + 5, y + 8, 12, 7, PyxelColor.FRAME)
    image.rect(x + 3, y + 2, 16, 3, PyxelColor.POT)
    image.rect(x + 5, y + 6, 12, 2, PyxelColor.POT)
    image.rect(x + 6, y + 8, 10, 6, PyxelColor.POT)
    image.line(x + 5, y + 3, x + 17, y + 3, PyxelColor.ACCENT)
    image.line(x + 16, y + 9, x + 16, y + 13, PyxelColor.FRAME)


def _stem(image: pyxel.Image, x: int, y: int) -> None:
    image.rect(x - 2, y, 5, 30, PyxelColor.GREENHOUSE_BG)
    image.rect(x - 1, y, 3, 30, PyxelColor.PEA_GREEN)
    image.line(x + 2, y + 3, x + 2, y + 29, PyxelColor.GREENHOUSE_BG)


def _pod(
    image: pyxel.Image,
    x: int,
    y: int,
    style: PodStyle,
) -> None:
    outline = PyxelColor.SPRITE_OUTLINE

    # Diagonal pod silhouette, tapered from lower-left to upper-right.
    rows = [
        (40, 4, 3),
        (37, 5, 7),
        (34, 6, 11),
        (31, 7, 15),
        (28, 8, 19),
        (25, 9, 23),
        (22, 10, 27),
        (20, 11, 29),
        (18, 12, 31),
        (16, 13, 33),
        (14, 14, 33),
        (13, 15, 33),
        (12, 16, 33),
        (11, 17, 31),
        (10, 18, 29),
        (9, 19, 27),
        (8, 20, 25),
        (7, 21, 23),
        (7, 22, 19),
        (7, 23, 15),
        (8, 24, 11),
        (9, 25, 7),
        (10, 26, 3),
    ]
    for start, row, width in rows:
        col = style.shadow if row >= POD_SHADOW_START_ROW else style.base
        image.line(x + start, y + row, x + start + width, y + row, outline)
        if width > MIN_INTERIOR_LINE_WIDTH:
            image.line(
                x + start + 1,
                y + row,
                x + start + width - 1,
                y + row,
                col,
            )

    inner_rows = [
        (37, 7, 7),
        (33, 8, 13),
        (29, 9, 19),
        (26, 10, 23),
        (23, 11, 25),
        (20, 12, 27),
        (18, 13, 29),
        (16, 14, 29),
        (15, 15, 29),
        (14, 16, 27),
        (13, 17, 25),
        (12, 18, 23),
        (11, 19, 21),
        (10, 20, 19),
        (10, 21, 15),
        (10, 22, 11),
        (11, 23, 7),
    ]
    for start, row, width in inner_rows:
        col = style.highlight if row <= POD_HIGHLIGHT_END_ROW else style.base
        image.line(x + start, y + row, x + start + width, y + row, col)

    image.line(x + 16, y + 20, x + 43, y + 8, style.highlight)
    image.line(x + 12, y + 23, x + 36, y + 17, style.shadow)
    image.line(x + 42, y + 5, x + 50, y - 3, outline)
    image.line(x + 43, y + 5, x + 51, y - 3, style.highlight)
    image.line(x + 10, y + 25, x + 1, y + 35, outline)
    image.line(x + 11, y + 25, x + 2, y + 35, style.shadow)

    for sx, sy in [(36, 12), (27, 17), (18, 22)]:
        _seed(image, x + sx, y + sy, style.seed)


def _flower(image: pyxel.Image, x: int, y: int, flower_col: int) -> None:
    image.circ(x, y - 6, 5, PyxelColor.GREENHOUSE_BG)
    image.circ(x - 7, y - 2, 5, PyxelColor.GREENHOUSE_BG)
    image.circ(x + 7, y - 2, 5, PyxelColor.GREENHOUSE_BG)
    image.circ(x, y + 4, 5, PyxelColor.GREENHOUSE_BG)
    image.circ(x, y - 6, 4, flower_col)
    image.circ(x - 6, y - 2, 4, flower_col)
    image.circ(x + 6, y - 2, 4, flower_col)
    image.circ(x, y + 3, 4, flower_col)
    image.circ(x, y, 2, PyxelColor.ACCENT)
    image.pset(x - 1, y - 5, PyxelColor.FIELD)
    image.pset(x - 5, y - 2, PyxelColor.FIELD)
    image.pset(x + 2, y + 3, PyxelColor.FRAME)


def _seed(
    image: pyxel.Image,
    x: int,
    y: int,
    style: SeedStyle,
) -> None:
    outline = PyxelColor.SPRITE_OUTLINE
    if style.texture == "wrinkled":
        image.circ(x, y, 5, outline)
        image.circ(x, y, 4, style.color)
        image.pset(x - 4, y, style.shadow)
        image.pset(x + 4, y - 1, style.shadow)
        image.pset(x - 2, y - 4, style.shadow)
        image.line(x - 3, y, x + 3, y + 1, style.shadow)
        image.line(x - 2, y + 2, x + 2, y - 2, style.shadow)
        image.pset(x - 1, y - 2, PyxelColor.FIELD)
        return

    image.circ(x, y, 5, outline)
    image.circ(x, y, 4, style.color)
    image.circ(x - 1, y - 1, 2, PyxelColor.FIELD)
    image.pset(x + 3, y + 2, style.shadow)
    image.pset(x + 2, y + 3, style.shadow)


def _draw_icons() -> None:
    for name, (u, v) in ICONS.items():
        pyxel.images[0].rect(u, v, ICON_SIZE, ICON_SIZE, 0)
        getattr(_IconPainter(u, v), name)()


def _build_audio() -> None:
    pyxel.sounds[0].set("c3", "p", "4", "n", 8)
    pyxel.sounds[1].set("e3g3", "t", "55", "n", 10)
    pyxel.sounds[2].set("c3e3g3c4", "s", "3345", "nnff", 12)
    pyxel.sounds[3].set("g3c4e4g4", "t", "3456", "nnff", 10)
    pyxel.sounds[4].set("c2c2", "n", "32", "nf", 6)

    # Redesigned G major track: warm, cheerful, slow, relaxing
    # Track 0: Melody (Plucked bell/music-box style)
    track0_parts = [
        "T108 @1 @ENV1{100,2,24} O4 L4 V100",
        # Section A (8 bars)
        "b2 >d4 <b4  a4 g2 r4  >c2 e4 c4  <b4 a2 r4",
        "a2 >c4 <a4  b4 >d2 r4  g2 b4 a4   g2. r4",
        # Section A' (8 bars)
        "b2 >d4 <b4  a4 g2 r4  >c2 e4 c4  <b4 a2 r4",
        "a2 >c4 <a4  b4 >d2 r4  >d4 c4 <b4 a4  g2. r4",
        # Section B (16 bars)
        "g2 a4 b4   b4 a2 r4  a2 b4 >c4  c4 <b2 r4",
        "b2 >c4 d4   d4 c2 r4  <b4 a4 b4 >c4  d2. r4",
        ">d2 e4 d4  c4 <b2 r4  >c2 d4 c4  <b4 a2 r4",
        "b2 >c4 <b4  a4 g2 r4  a4 b4 >c4 <a4  g2. r4",
    ]
    pyxel.sounds[5].mml(" ".join(track0_parts))

    # Track 1: Accompaniment (Soft Triangle arpeggios)
    track1_parts = [
        "T108 @0 @ENV1{64,4,32} O3 L8 V80",
        # Section A (8 bars)
        "[g8 b8 >d8 <b8]2  [g8 b8 >d8 <b8]2",
        "[c8 e8 g8 e8]2   [c8 e8 g8 e8]2",
        "[d8 f+8 a8 f+8]2 [d8 f+8 a8 f+8]2",
        "[g8 b8 >d8 <b8]2  [g8 b8 >d8 <b8]2",
        # Section A' (8 bars)
        "[g8 b8 >d8 <b8]2  [g8 b8 >d8 <b8]2",
        "[c8 e8 g8 e8]2   [c8 e8 g8 e8]2",
        "[d8 f+8 a8 f+8]2 [d8 f+8 a8 f+8]2",
        "[g8 b8 >d8 <b8]2  [g8 b8 >d8 <b8]2",
        # Section B (16 bars)
        "[e8 g8 b8 g8]2   [e8 g8 b8 g8]2",
        "[b8 >d8 f+8 d8]2 [b8 >d8 f+8 d8]2",
        "[c8 e8 g8 e8]2   [c8 e8 g8 e8]2",
        "[d8 f+8 a8 f+8]2 [d8 f+8 a8 f+8]2",
        "[b8 >d8 f+8 d8]2 [b8 >d8 f+8 d8]2",
        "[c8 e8 g8 e8]2   [c8 e8 g8 e8]2",
        "[g8 b8 >d8 <b8]2  [g8 b8 >d8 <b8]2",
        "[d8 f+8 c8 f+8]2 [g8 b8 >d8 <b8]2",
    ]
    pyxel.sounds[6].mml(" ".join(track1_parts))

    # Track 2: Bassline (Deep Triangle grounding notes)
    track2_parts = [
        "T108 @0 O2 L1 V90",
        # Section A (8 bars)
        "g1 g1 c1 c1 d1 d1 g1 g1",
        # Section A' (8 bars)
        "g1 g1 c1 c1 d1 d1 d1 g1",
        # Section B (16 bars)
        "e1 e1 b1 b1 c1 c1 d1 d1",
        "b1 b1 c1 c1 g1 g1 d1 g1",
    ]
    pyxel.sounds[7].mml(" ".join(track2_parts))

    pyxel.musics[0].set([5], [6], [7])


def _write_bdf_font() -> None:
    lines = [
        "STARTFONT 2.1",
        "FONT -mendels-greenhouse-medium-r-normal--8-80-75-75-c-60-iso10646-1",
        "SIZE 8 75 75",
        "FONTBOUNDINGBOX 6 8 0 -1",
        "STARTPROPERTIES 2",
        "FONT_ASCENT 7",
        "FONT_DESCENT 1",
        "ENDPROPERTIES",
        f"CHARS {len(GLYPHS)}",
    ]
    for char, rows in GLYPHS.items():
        codepoint = ord(char)
        lines.extend(
            [
                f"STARTCHAR U+{codepoint:04X}",
                f"ENCODING {codepoint}",
                "SWIDTH 500 0",
                "DWIDTH 6 0",
                "BBX 5 7 0 0",
                "BITMAP",
            ],
        )
        lines.extend(f"{int(row, 2) << 3:02X}" for row in rows)
        lines.append("ENDCHAR")
    lines.append("ENDFONT")
    FONT_PATH.write_text("\n".join(lines) + "\n", encoding="ascii")


class _IconPainter:
    def __init__(self, u: int, v: int) -> None:
        self.u = u
        self.v = v
        self.image = pyxel.images[0]

    def guide(self) -> None:
        outline = PyxelColor.SPRITE_OUTLINE
        paper = PyxelColor.PARCHMENT_LIGHT
        page_shadow = PyxelColor.PARCHMENT_BASE
        red = PyxelColor.TOMATO_RED

        self.image.rect(self.u + 13, self.v + 15, 38, 34, outline)
        self.image.rect(self.u + 16, self.v + 18, 15, 27, paper)
        self.image.rect(self.u + 33, self.v + 18, 15, 27, paper)
        self.image.line(
            self.u + 32, self.v + 17, self.u + 32, self.v + 47, outline
        )
        self.image.rect(self.u + 18, self.v + 20, 10, 3, red)
        self.image.rect(self.u + 36, self.v + 20, 8, 3, red)
        for row in [27, 32, 37]:
            self.image.line(
                self.u + 19,
                self.v + row,
                self.u + 28,
                self.v + row,
                PyxelColor.DARK_WOOD,
            )
            self.image.line(
                self.u + 36,
                self.v + row,
                self.u + 45,
                self.v + row,
                PyxelColor.DARK_WOOD,
            )
        self.image.line(
            self.u + 17, self.v + 44, self.u + 30, self.v + 47, page_shadow
        )
        self.image.line(
            self.u + 34, self.v + 47, self.u + 48, self.v + 44, page_shadow
        )

    def garden(self) -> None:
        outline = PyxelColor.SPRITE_OUTLINE
        pot = PyxelColor.TERRACOTTA
        pot_shadow = PyxelColor.DARK_WOOD

        self.image.rect(self.u + 19, self.v + 38, 27, 6, outline)
        self.image.rect(self.u + 22, self.v + 43, 21, 10, outline)
        self.image.rect(self.u + 20, self.v + 39, 25, 4, pot)
        self.image.rect(self.u + 24, self.v + 43, 17, 8, pot)
        self.image.line(
            self.u + 25, self.v + 49, self.u + 40, self.v + 49, pot_shadow
        )
        self.image.rect(self.u + 28, self.v + 35, 9, 5, PyxelColor.SOIL_DARK)
        self.image.line(
            self.u + 32,
            self.v + 37,
            self.u + 32,
            self.v + 19,
            PyxelColor.POD_SHADOW,
        )
        self.image.elli(self.u + 20, self.v + 20, 18, 11, outline)
        self.image.elli(self.u + 21, self.v + 21, 16, 9, PyxelColor.POD_BASE)
        self.image.elli(self.u + 33, self.v + 15, 21, 12, outline)
        self.image.elli(self.u + 34, self.v + 16, 19, 10, PyxelColor.POD_BASE)
        self.image.elli(self.u + 27, self.v + 7, 22, 14, outline)
        self.image.elli(
            self.u + 28, self.v + 8, 20, 12, PyxelColor.POD_HIGHLIGHT
        )
        self.image.line(
            self.u + 31,
            self.v + 10,
            self.u + 38,
            self.v + 18,
            PyxelColor.PARCHMENT_LIGHT,
        )

    def shop(self) -> None:
        outline = PyxelColor.SPRITE_OUTLINE
        paper = PyxelColor.PARCHMENT_BASE
        red = PyxelColor.TOMATO_RED
        blue = PyxelColor.BLUE_GLASS

        self.image.rect(self.u + 14, self.v + 29, 37, 25, outline)
        self.image.rect(self.u + 17, self.v + 32, 31, 19, paper)
        self.image.rect(self.u + 18, self.v + 34, 12, 13, blue)
        self.image.rect(
            self.u + 35, self.v + 34, 10, 13, PyxelColor.PARCHMENT_LIGHT
        )
        self.image.rect(self.u + 12, self.v + 18, 41, 12, outline)
        for index, x in enumerate([14, 22, 30, 38, 46]):
            color = red if index % 2 == 0 else PyxelColor.PARCHMENT_LIGHT
            self.image.rect(self.u + x, self.v + 20, 7, 8, color)
        self.image.line(
            self.u + 16,
            self.v + 50,
            self.u + 48,
            self.v + 50,
            PyxelColor.DARK_WOOD,
        )
        self.image.pset(self.u + 40, self.v + 43, PyxelColor.SEED_GOLD)

    def settings(self) -> None:
        outline = PyxelColor.SPRITE_OUTLINE
        metal = PyxelColor.METAL_LIGHT
        shadow = PyxelColor.METAL_DARK
        highlight = PyxelColor.GLASS_HIGHLIGHT

        for x, y, w, h in [
            (29, 7, 7, 13),
            (29, 44, 7, 13),
            (7, 29, 13, 7),
            (44, 29, 13, 7),
            (13, 13, 10, 10),
            (41, 13, 10, 10),
            (13, 41, 10, 10),
            (41, 41, 10, 10),
        ]:
            self.image.rect(self.u + x, self.v + y, w, h, outline)
            self.image.rect(
                self.u + x + 2, self.v + y + 2, w - 4, h - 4, metal
            )
        self.image.circ(self.u + 32, self.v + 32, 23, outline)
        self.image.circ(self.u + 32, self.v + 32, 20, metal)
        self.image.circ(self.u + 32, self.v + 32, 12, shadow)
        self.image.circ(self.u + 32, self.v + 32, 7, 0)
        self.image.circb(self.u + 32, self.v + 32, 8, outline)
        self.image.line(
            self.u + 20, self.v + 19, self.u + 27, self.v + 15, highlight
        )
        self.image.line(
            self.u + 43, self.v + 42, self.u + 38, self.v + 47, shadow
        )

    def coin(self) -> None:
        self.image.circ(
            self.u + 32, self.v + 32, 20, PyxelColor.SPRITE_OUTLINE
        )
        self.image.circ(self.u + 32, self.v + 32, 17, PyxelColor.SEED_GOLD)
        self.image.circb(self.u + 32, self.v + 32, 12, PyxelColor.DARK_WOOD)
        self.image.text(self.u + 28, self.v + 28, "S", PyxelColor.DARK_WOOD)

    def seed(self) -> None:
        self.image.circ(
            self.u + 28, self.v + 36, 15, PyxelColor.SPRITE_OUTLINE
        )
        self.image.circ(self.u + 28, self.v + 36, 12, PyxelColor.SEED_GOLD)
        self.image.circ(
            self.u + 42, self.v + 24, 11, PyxelColor.SPRITE_OUTLINE
        )
        self.image.circ(self.u + 42, self.v + 24, 9, PyxelColor.PEA_GREEN)
        self.image.line(
            self.u + 30,
            self.v + 33,
            self.u + 43,
            self.v + 21,
            PyxelColor.POD_SHADOW,
        )

    def contract(self) -> None:
        outline = PyxelColor.SPRITE_OUTLINE
        board = PyxelColor.DARK_WOOD
        board_light = PyxelColor.WOOD_MIDTONE
        paper = PyxelColor.PARCHMENT_LIGHT
        ink = PyxelColor.UI_DARK

        # Wooden clipboard silhouette and inset highlight.
        self.image.rect(self.u + 14, self.v + 12, 38, 44, outline)
        self.image.rect(self.u + 17, self.v + 15, 32, 38, board)
        self.image.line(
            self.u + 18,
            self.v + 16,
            self.u + 47,
            self.v + 16,
            board_light,
        )

        # Contract sheet with a folded lower corner.
        self.image.rect(self.u + 20, self.v + 19, 25, 29, paper)
        self.image.tri(
            self.u + 39,
            self.v + 48,
            self.u + 45,
            self.v + 42,
            self.u + 45,
            self.v + 48,
            PyxelColor.PARCHMENT_BASE,
        )

        # Gold clipboard clasp.
        self.image.rect(self.u + 24, self.v + 9, 17, 8, outline)
        self.image.rect(self.u + 27, self.v + 7, 11, 4, outline)
        self.image.rect(self.u + 26, self.v + 11, 13, 4, PyxelColor.SEED_GOLD)
        self.image.rect(
            self.u + 29,
            self.v + 9,
            7,
            2,
            PyxelColor.SUNLIT_CREAM,
        )

        # Objective title, task lines, and completion checks.
        self.image.rect(self.u + 24, self.v + 23, 17, 3, PyxelColor.TOMATO_RED)
        for row in (31, 37, 43):
            self.image.rect(self.u + 24, self.v + row, 3, 3, outline)
            self.image.line(
                self.u + 30,
                self.v + row + 1,
                self.u + 40,
                self.v + row + 1,
                ink,
            )
        self.image.line(
            self.u + 24,
            self.v + 32,
            self.u + 25,
            self.v + 33,
            PyxelColor.SUCCESS_LIME,
        )
        self.image.line(
            self.u + 25,
            self.v + 33,
            self.u + 28,
            self.v + 29,
            PyxelColor.SUCCESS_LIME,
        )


if __name__ == "__main__":
    main()
