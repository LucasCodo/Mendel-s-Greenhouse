"""Human-readable names for Pyxel palette indexes."""

import pyxel

PROJECT_PALETTE = [
    0x111827,  # 0 ink shadow
    0x1E293B,  # 1 deep glass navy
    0x7C3AED,  # 2 genetic purple
    0x2D9D78,  # 3 leaf shadow
    0x7C4F2C,  # 4 dark wood
    0x4F6FAF,  # 5 blue glass
    0xC7DDFB,  # 6 glass highlight
    0xF8F4E8,  # 7 parchment light
    0xD94B6A,  # 8 tomato red
    0xD88B3A,  # 9 terracotta
    0xF2C94C,  # 10 seed gold
    0x6BCB77,  # 11 leaf green
    0xB89A72,  # 12 wood midtone
    0x334155,  # 13 warm floor
    0xF7D96E,  # 14 sunlit cream
    0xE8D3B0,  # 15 parchment base
    0xA7E48A,  # 16 leaf highlight
    0x86C8AA,  # 17 cyan science
    0x7AA2F7,  # 18 blue flower
    0xF7A8B8,  # 19 pink flower
    0xF8F4E8,  # 20 white petal
    0x9B58D6,  # 21 orchid violet
    0xF7D96E,  # 22 corn yellow
    0xA7E48A,  # 23 corn husk
    0xD88B3A,  # 24 tomato orange
    0xD94B6A,  # 25 tomato red bright
    0x3A2A20,  # 26 soil dark
    0x334155,  # 27 metal dark
    0x9CA3AF,  # 28 metal light
    0xA35CFF,  # 29 rare gem
    0x6BCB77,  # 30 success lime
    0xD94B6A,  # 31 error ember
]


class PyxelColor:
    """Human-readable project palette indexes."""

    INK_SHADOW = 0
    DEEP_GLASS_NAVY = 1
    GENETIC_PURPLE = 2
    LEAF_SHADOW = 3
    DARK_WOOD = 4
    BLUE_GLASS = 5
    GLASS_HIGHLIGHT = 6
    PARCHMENT_LIGHT = 7
    TOMATO_RED = 8
    TERRACOTTA = 9
    SEED_GOLD = 10
    LEAF_GREEN = 11
    WOOD_MIDTONE = 12
    WARM_FLOOR = 13
    SUNLIT_CREAM = 14
    PARCHMENT_BASE = 15
    LEAF_HIGHLIGHT = 16
    CYAN_SCIENCE = 17
    BLUE_FLOWER = 18
    PINK_FLOWER = 19
    WHITE_PETAL = 20
    ORCHID_VIOLET = 21
    CORN_YELLOW = 22
    CORN_HUSK = 23
    TOMATO_ORANGE = 24
    TOMATO_RED_BRIGHT = 25
    SOIL_DARK = 26
    METAL_DARK = 27
    METAL_LIGHT = 28
    RARE_GEM = 29
    SUCCESS_LIME = 30
    ERROR_EMBER = 31

    GREENHOUSE_BG = DEEP_GLASS_NAVY
    UI_DARK = INK_SHADOW
    PANEL_DARK = DARK_WOOD
    PARCHMENT = PARCHMENT_BASE
    FRAME = DARK_WOOD
    FIELD = PARCHMENT_LIGHT
    CONVEYOR = METAL_DARK
    BAR_EMPTY = WOOD_MIDTONE
    PROGRESS = SUCCESS_LIME
    ACTION = LEAF_GREEN
    POT = TERRACOTTA
    TEXT = PARCHMENT_LIGHT
    TEXT_MUTED = METAL_LIGHT
    ACCENT = SEED_GOLD
    PEA_YELLOW = SEED_GOLD
    PEA_GREEN = LEAF_HIGHLIGHT
    POD_SHADOW = LEAF_SHADOW
    POD_BASE = LEAF_GREEN
    POD_HIGHLIGHT = LEAF_HIGHLIGHT
    SPRITE_OUTLINE = SOIL_DARK
    FLOWER_PURPLE = GENETIC_PURPLE
    FLOWER_WHITE = WHITE_PETAL


def apply_project_palette() -> None:
    """Apply the project palette before loading visual assets."""
    pyxel.colors[:] = PROJECT_PALETTE
