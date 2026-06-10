# ruff: noqa: PLR0915, PLR2004, E501, PLR0912
"""Standalone Botanical Laboratory Genetic Analyzer Handheld Console.

Replicates the visual target shown in the reference image:
- Beige/off-white rounded handheld case with rivets, weathering, and panel bevels.
- Glass tubes with green glowing fluid, reflection sheen, and bubble animations.
- Top digital screen with "ANALISADOR GENETICO" and green "NIVEL 2" badge.
- Main screen showing specimen plant icon, visible genotype boxes, and gene listings.
- Bottom hardware buttons: circular D-Pad, glowing green square leaf button,
  ridges roller slider, indicator light, and orange LED.
"""

import random
from dataclasses import dataclass

import pyxel

# ------------------------------------------------------------------------------
# 32-Color Project Palette
# ------------------------------------------------------------------------------
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


# ------------------------------------------------------------------------------
# Genetics Definitions for dynamic UI
# ------------------------------------------------------------------------------
@dataclass
class PlantSpecimen:
    genotype: str

    @property
    def color_phenotype_en(self) -> str:
        return "Yellow" if "A" in self.genotype[0:2] else "Green"

    @property
    def texture_phenotype_en(self) -> str:
        return "Smooth" if "B" in self.genotype[2:4] else "Wrinkled"

    @property
    def color_phenotype_pt(self) -> str:
        return "Amarela" if "A" in self.genotype[0:2] else "Verde"

    @property
    def texture_phenotype_pt(self) -> str:
        return "lisa" if "B" in self.genotype[2:4] else "rugosa"


# Language translation dict
LOC = {
    "pt-br": {
        "title": "ANALISADOR GENETICO",
        "level": "NIVEL",
        "specimen_name": "ERVILHA",
        "visible_genotype": "Genotipo (visivel):",
        "detected_genes": "Genes detectados:",
        "yellow_dom": "Amarela (A) dominante",
        "green_rec": "Verde (a) recessivo",
        "smooth_dom": "Lisa (B) dominante",
        "wrinkled_rec": "Rugosa (b) recessivo",
        "locked": "BLOQUEADO",
    },
    "en": {
        "title": "GENETIC ANALYZER",
        "level": "LEVEL",
        "specimen_name": "PEA PLANT",
        "visible_genotype": "Genotype (visible):",
        "detected_genes": "Detected genes:",
        "yellow_dom": "Yellow (A) dominant",
        "green_rec": "Green (a) recessive",
        "smooth_dom": "Smooth (B) dominant",
        "wrinkled_rec": "Wrinkled (b) recessive",
        "locked": "LOCKED",
    },
}


class HandheldAnalyzerApp:
    def __init__(self):
        # 240x380 console proportional layout window
        pyxel.init(
            240, 380, title="Mendel's Greenhouse - Genetic Analyzer Console"
        )
        pyxel.mouse(True)

        # Apply 32 color custom palette
        pyxel.colors[:] = PROJECT_PALETTE

        # Audio assets
        pyxel.sounds[0].set("c3e3g3", "p", "777", "nnn", 5)  # Click chime
        pyxel.sounds[1].set(
            "c2c#2c2c#2", "s", "4444", "nnnn", 3
        )  # Roller slide hum

        # Game/Device States
        self.language = "pt-br"
        self.analyzer_level = 2
        self.genotypes = [
            "AaBb",
            "AABB",
            "aabb",
            "AAbb",
            "aaBB",
            "Aabb",
            "aaBb",
        ]
        self.active_genotype_idx = 0
        self.active_plant = PlantSpecimen(
            self.genotypes[self.active_genotype_idx]
        )

        # Interactive hardware control triggers
        self.screen_flash = 0
        self.roller_val = 0.5  # 0.0 to 1.0 representing roller position
        self.scanline_y = 30

        # Procedural visual elements generators
        self.bubbles = []
        for _ in range(12):
            self.bubbles.append(
                {
                    "x": random.uniform(15, 39),
                    "y": random.uniform(85, 230),
                    "speed": random.uniform(0.4, 1.0),
                    "radius": random.choice([1, 2]),
                }
            )

        # Mini top-left tube bubbles
        self.top_bubbles = []
        for _ in range(5):
            self.top_bubbles.append(
                {
                    "x": random.uniform(18, 29),
                    "y": random.uniform(20, 40),
                    "speed": random.uniform(0.2, 0.5),
                }
            )

        pyxel.run(self.update, self.draw)

    def change_level(self, change: int):
        new_lvl = self.analyzer_level + change
        if 1 <= new_lvl <= 4:
            pyxel.play(0, 0)
            self.analyzer_level = new_lvl

    def change_genotype(self, change: int):
        pyxel.play(0, 0)
        self.active_genotype_idx = (self.active_genotype_idx + change) % len(
            self.genotypes
        )
        self.active_plant = PlantSpecimen(
            self.genotypes[self.active_genotype_idx]
        )

    def trigger_scan_flash(self):
        pyxel.play(0, 0)
        self.screen_flash = 12  # Screen flash frames count

    def toggle_language(self):
        pyxel.play(0, 0)
        self.language = "en" if self.language == "pt-br" else "pt-br"

    # ------------------------------------------------------------------------------
    # Update Loop
    # ------------------------------------------------------------------------------
    def update(self):
        # Scan flash countdown
        if self.screen_flash > 0:
            self.screen_flash -= 1

        # Liquid bubbles update
        for b in self.bubbles:
            b["y"] -= b["speed"]
            # fluid limit in the tube is around Y = 135
            if b["y"] < 135:
                b["y"] = 230
                b["x"] = random.uniform(15, 39)

        # Top tube bubbles update
        for b in self.top_bubbles:
            b["y"] -= b["speed"]
            if b["y"] < 18:
                b["y"] = 42
                b["x"] = random.uniform(18, 29)

        # Mouse clicks on hardware components
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            mx, my = pyxel.mouse_x, pyxel.mouse_y

            # 1. D-Pad arrows (direction controller)
            # Center of D-Pad is (45, 325)
            # Left arrow: (27, 320, 10, 10)
            if 22 <= mx <= 35 and 318 <= my <= 332:
                self.change_genotype(-1)
            # Right arrow: (55, 320, 10, 10)
            elif (55 <= mx <= 68 and 318 <= my <= 332) or (
                38 <= mx <= 52 and 304 <= my <= 316
            ):
                self.change_genotype(1)
            # Down arrow: (40, 334, 10, 10)
            elif 38 <= mx <= 52 and 334 <= my <= 346:
                self.change_genotype(-1)

            # 2. Glowing Square Green Leaf Button
            # Coords: (95, 285, 55, 55) -> X = 95 to 150, Y = 285 to 340
            if 95 <= mx <= 150 and 285 <= my <= 340:
                self.trigger_scan_flash()

            # 3. Vertical Roller Slider
            # Coords: (175, 290, 20, 50) -> X = 172 to 192, Y = 290 to 340
            if 172 <= mx <= 192 and 290 <= my <= 340:
                pyxel.play(1, 1)
                # Toggle through levels depending on click Y
                if my < 302:
                    self.analyzer_level = 1
                elif my < 315:
                    self.analyzer_level = 2
                elif my < 328:
                    self.analyzer_level = 3
                else:
                    self.analyzer_level = 4

            # 4. Glowing lens button or orange LED toggling language
            # Orange LED: (200, 328, 10, 10) or Lens (205, 295, 16, 16)
            if 200 <= mx <= 224 and 290 <= my <= 336:
                self.toggle_language()

    # ------------------------------------------------------------------------------
    # Drawing Loop
    # ------------------------------------------------------------------------------
    def draw(self):
        # Clear screen to a dark gray floor background
        pyxel.cls(PyxelColor.INK_SHADOW)

        # Draw Handheld Device Casing body
        self.draw_casing_body()

        # Draw Glass Fluid Columns
        self.draw_glass_tubes()

        # Draw Inset screens and contents
        self.draw_device_screens()

        # Draw Hardware knobs and buttons
        self.draw_hardware_controls()

        # Screen flash effect overlay (green/white flash)
        if self.screen_flash > 0:
            pyxel.rect(65, 80, 160, 195, PyxelColor.GLASS_HIGHLIGHT)

    # ------------------------------------------------------------------------------
    # Casing Body Graphics
    # ------------------------------------------------------------------------------
    def draw_casing_body(self):
        # Off-white beveled handheld device body frame (filling entire canvas)
        # Rounded capsule outer margins
        pyxel.rect(5, 5, 230, 370, PyxelColor.PARCHMENT_BASE)

        # Highlights & Shadows for 3D rounded appearance
        # Left Highlight vertical border
        pyxel.line(5, 10, 5, 370, PyxelColor.PARCHMENT_LIGHT)
        pyxel.line(6, 8, 6, 370, PyxelColor.PARCHMENT_LIGHT)
        # Top Highlight border
        pyxel.line(10, 5, 230, 5, PyxelColor.PARCHMENT_LIGHT)
        # Right Shadow border
        pyxel.line(234, 10, 234, 370, PyxelColor.WOOD_MIDTONE)
        pyxel.line(235, 12, 235, 370, PyxelColor.SOIL_DARK)
        # Bottom Shadow border
        pyxel.line(10, 374, 230, 374, PyxelColor.SOIL_DARK)

        # Outer Corner Cuts for rounded corners
        pyxel.pset(5, 5, PyxelColor.INK_SHADOW)
        pyxel.pset(6, 5, PyxelColor.INK_SHADOW)
        pyxel.pset(5, 6, PyxelColor.INK_SHADOW)
        pyxel.pset(234, 5, PyxelColor.INK_SHADOW)
        pyxel.pset(234, 6, PyxelColor.INK_SHADOW)
        pyxel.pset(235, 5, PyxelColor.INK_SHADOW)
        pyxel.pset(5, 374, PyxelColor.INK_SHADOW)
        pyxel.pset(5, 373, PyxelColor.INK_SHADOW)
        pyxel.pset(6, 374, PyxelColor.INK_SHADOW)
        pyxel.pset(234, 374, PyxelColor.INK_SHADOW)
        pyxel.pset(234, 373, PyxelColor.INK_SHADOW)
        pyxel.pset(235, 374, PyxelColor.INK_SHADOW)

        # Moss/rust weathering clusters (procedural pixel art details)
        # Cluster top right
        pyxel.pset(210, 12, PyxelColor.LEAF_GREEN)
        pyxel.pset(211, 12, PyxelColor.LEAF_SHADOW)
        pyxel.pset(210, 13, PyxelColor.LEAF_SHADOW)
        # Cluster bottom left
        pyxel.pset(18, 360, PyxelColor.LEAF_GREEN)
        pyxel.pset(19, 360, PyxelColor.LEAF_SHADOW)

        # Rivets / Screws (with slots)
        # 4 corners
        self.draw_casing_screw(15, 15)
        self.draw_casing_screw(225, 15)
        self.draw_casing_screw(15, 360)
        self.draw_casing_screw(225, 360)
        # Mid-sides
        self.draw_casing_screw(15, 185)
        self.draw_casing_screw(225, 185)

        # Right green grip textured plate
        # Located at X = 230 to 235, Y = 160 to 220
        pyxel.rect(230, 160, 5, 60, PyxelColor.LEAF_SHADOW)
        pyxel.rectb(230, 160, 5, 60, PyxelColor.SOIL_DARK)
        # Ridges inside grip
        for ry in range(165, 216, 5):
            pyxel.line(231, ry, 233, ry, PyxelColor.LEAF_HIGHLIGHT)

    def draw_casing_screw(self, x: int, y: int):
        # Draw a small 3D metal screw rivet
        pyxel.circ(x, y, 2, PyxelColor.METAL_LIGHT)
        pyxel.circb(x, y, 2, PyxelColor.SOIL_DARK)
        # Screw head slot line
        pyxel.pset(x, y, PyxelColor.SOIL_DARK)
        pyxel.pset(x - 1, y, PyxelColor.SOIL_DARK)
        # specular shine
        pyxel.pset(x - 1, y - 1, PyxelColor.WHITE_PETAL)

    # ------------------------------------------------------------------------------
    # Left Column: Glass Chambers Graphics
    # ------------------------------------------------------------------------------
    def draw_glass_tubes(self):
        # 1. Top Left Small Glass Cap
        # X = 15 to 32, Y = 16 to 42
        tx1, ty1, tw1, th1 = 16, 16, 16, 26
        pyxel.rect(tx1, ty1, tw1, th1, PyxelColor.INK_SHADOW)
        # Fill green fluid
        pyxel.rect(tx1 + 2, ty1 + 2, tw1 - 4, th1 - 4, PyxelColor.LEAF_GREEN)
        # Highlight sheen
        pyxel.line(
            tx1 + 3,
            ty1 + 3,
            tx1 + 3,
            ty1 + th1 - 3,
            PyxelColor.GLASS_HIGHLIGHT,
        )
        # Small bubbles update
        for b in self.top_bubbles:
            pyxel.pset(int(b["x"]), int(b["y"]), PyxelColor.LEAF_HIGHLIGHT)
        # Metal cap
        pyxel.rect(tx1 - 1, ty1 - 2, tw1 + 2, 4, PyxelColor.METAL_DARK)
        pyxel.rectb(tx1 - 1, ty1 - 2, tw1 + 2, 4, PyxelColor.SOIL_DARK)

        # 2. Main Large Glass Cylinder (Lower Left)
        # Coords: X = 12 to 43, Y = 70 to 240 (Height = 170)
        tx, ty, tw, th = 12, 70, 32, 170
        pyxel.rect(tx, ty, tw, th, PyxelColor.INK_SHADOW)

        # Cylinder fluid: Filled up to Y = 135 (about 60% full)
        fluid_level_y = 135
        # Fluid background
        pyxel.rect(
            tx + 2,
            fluid_level_y,
            tw - 4,
            (ty + th - 2) - fluid_level_y,
            PyxelColor.LEAF_GREEN,
        )

        # 3D shading columns on liquid
        for cx in range(tx + 2, tx + tw - 2):
            rel_x = (cx - (tx + 2)) / (tw - 4)
            if rel_x < 0.25 or rel_x > 0.75:
                col = PyxelColor.LEAF_SHADOW
            else:
                col = PyxelColor.LEAF_HIGHLIGHT
            # draw cylinder shading column
            pyxel.line(cx, fluid_level_y, cx, ty + th - 2, col)

        # Draw liquid surface meniscus curved lines
        pyxel.line(
            tx + 2,
            fluid_level_y,
            tx + 6,
            fluid_level_y + 1,
            PyxelColor.LEAF_HIGHLIGHT,
        )
        pyxel.line(
            tx + 7,
            fluid_level_y + 2,
            tx + tw - 8,
            fluid_level_y + 2,
            PyxelColor.LEAF_HIGHLIGHT,
        )
        pyxel.line(
            tx + tw - 7,
            fluid_level_y + 1,
            tx + tw - 3,
            fluid_level_y,
            PyxelColor.LEAF_HIGHLIGHT,
        )

        # Meniscus dark outline
        pyxel.line(
            tx + 2,
            fluid_level_y - 1,
            tx + 6,
            fluid_level_y,
            PyxelColor.SOIL_DARK,
        )
        pyxel.line(
            tx + 7,
            fluid_level_y + 1,
            tx + tw - 8,
            fluid_level_y + 1,
            PyxelColor.SOIL_DARK,
        )
        pyxel.line(
            tx + tw - 7,
            fluid_level_y,
            tx + tw - 3,
            fluid_level_y - 1,
            PyxelColor.SOIL_DARK,
        )

        # Spores/Bubbles rising inside fluid
        for b in self.bubbles:
            bx, by = int(b["x"]), int(b["y"])
            # Renders bubbles inside tube
            pyxel.circ(bx, by, b["radius"], PyxelColor.LEAF_HIGHLIGHT)
            if b["radius"] > 1:
                pyxel.pset(bx - 1, by - 1, PyxelColor.WHITE_PETAL)

        # Glass cylinder metallic cap (top and bottom)
        pyxel.rect(tx - 2, ty - 5, tw + 4, 6, PyxelColor.METAL_DARK)
        pyxel.rectb(tx - 2, ty - 5, tw + 4, 6, PyxelColor.SOIL_DARK)
        pyxel.rect(tx - 2, ty + th - 1, tw + 4, 6, PyxelColor.METAL_DARK)
        pyxel.rectb(tx - 2, ty + th - 1, tw + 4, 6, PyxelColor.SOIL_DARK)

        # 3D sheen highlights on glass surface
        pyxel.line(
            tx + 3, ty + 2, tx + 3, ty + th - 3, PyxelColor.GLASS_HIGHLIGHT
        )
        pyxel.line(tx + 5, ty + 5, tx + 5, ty + 40, PyxelColor.GLASS_HIGHLIGHT)
        pyxel.line(
            tx + tw - 3,
            ty + 2,
            tx + tw - 3,
            ty + th - 3,
            PyxelColor.PARCHMENT_LIGHT,
        )

    # ------------------------------------------------------------------------------
    # Digital Display and Terminal Info Screens
    # ------------------------------------------------------------------------------
    def draw_device_screens(self):
        loc = LOC[self.language]

        # 1. Top Banner Screen (Title and Level)
        # Position: X = 70 to 220, Y = 15 to 65
        pyxel.rect(70, 15, 150, 48, PyxelColor.INK_SHADOW)
        pyxel.rectb(70, 15, 150, 48, PyxelColor.METAL_DARK)

        # Double screen highlight border
        pyxel.rectb(72, 17, 146, 44, PyxelColor.METAL_LIGHT)

        # Title text
        self.draw_text_shadow(92, 23, loc["title"], PyxelColor.TEXT)

        # Level Badge Capsule (NIVEL 2 / LEVEL 2)
        # Capsule coordinates
        bx, by, bw, bh = 80, 36, 130, 18
        pyxel.rect(bx, by, bw, bh, PyxelColor.SUCCESS_LIME)
        pyxel.rectb(bx, by, bw, bh, PyxelColor.LEAF_SHADOW)
        # Level text
        lbl = f"{loc['level']} {self.analyzer_level}"
        self.draw_text_shadow(bx + 40, by + 6, lbl, PyxelColor.WHITE_PETAL)

        # 2. Main Terminal Screen
        # Position: X = 65 to 225 (W = 160), Y = 80 to 275 (H = 195)
        sx, sy, sw, sh = 65, 80, 160, 195

        # Screen frame
        pyxel.rect(sx, sy, sw, sh, PyxelColor.INK_SHADOW)
        # Outer screen frame shadow
        pyxel.rectb(sx, sy, sw, sh, PyxelColor.METAL_LIGHT)
        # Inner screen border line
        pyxel.rectb(sx + 2, sy + 2, sw - 4, sh - 4, PyxelColor.DEEP_GLASS_NAVY)

        # Terminal Background green grid pattern
        for gx in range(sx + 10, sx + sw, 14):
            for gy in range(sy + 10, sy + sh, 14):
                pyxel.pset(gx, gy, PyxelColor.LEAF_SHADOW)

        # Terminal Scanline scroll animation
        pyxel.line(
            sx + 3,
            int(self.scanline_y) % (sh - 6) + sy + 3,
            sx + sw - 4,
            int(self.scanline_y) % (sh - 6) + sy + 3,
            PyxelColor.DEEP_GLASS_NAVY,
        )

        # --- Screen Contents ---

        # Row 1: Plant Specimen Icon
        # Miniature potted plant draw
        self.draw_plant_icon(sx + 12, sy + 10)
        # Species label
        self.draw_text_shadow(
            sx + 40, sy + 12, loc["specimen_name"], PyxelColor.TEXT
        )
        # Phenotype trait text (Amarela lisa / Verde lisa, etc.)
        if self.language == "pt-br":
            trait_lbl = f"{self.active_plant.color_phenotype_pt} {self.active_plant.texture_phenotype_pt}"
        else:
            trait_lbl = f"{self.active_plant.color_phenotype_en} {self.active_plant.texture_phenotype_en}"

        pyxel.text(sx + 40, sy + 22, trait_lbl, PyxelColor.LEAF_HIGHLIGHT)

        # Divider line
        pyxel.line(
            sx + 8, sy + 38, sx + sw - 8, sy + 38, PyxelColor.LEAF_SHADOW
        )

        # Row 2: Visible Genotypes
        # Label: Genotipo (visivel):
        pyxel.text(
            sx + 12, sy + 44, loc["visible_genotype"], PyxelColor.TEXT_MUTED
        )

        # Draw allele boxes
        box_y = sy + 56
        # Genotype displays based on level
        if self.analyzer_level == 1:
            # Masked boxes
            self.draw_allele_box(sx + 16, box_y, "?", PyxelColor.TOMATO_RED)
            self.draw_allele_box(sx + 74, box_y, "?", PyxelColor.TOMATO_RED)
        elif self.analyzer_level == 2:
            # Phenotypic visible genotype (e.g. "A -" and "B -")
            allele_a = (
                "A -" if "A" in self.active_plant.genotype[0:2] else "a a"
            )
            allele_b = (
                "B -" if "B" in self.active_plant.genotype[2:4] else "b b"
            )
            self.draw_allele_box(
                sx + 16, box_y, allele_a, PyxelColor.SUCCESS_LIME
            )
            self.draw_allele_box(
                sx + 74, box_y, allele_b, PyxelColor.SUCCESS_LIME
            )
        else:
            # Sequence genotype (e.g. "A a" and "B b")
            allele_a = f"{self.active_plant.genotype[0]} {self.active_plant.genotype[1]}"
            allele_b = f"{self.active_plant.genotype[2]} {self.active_plant.genotype[3]}"
            self.draw_allele_box(sx + 16, box_y, allele_a, PyxelColor.ACCENT)
            self.draw_allele_box(sx + 74, box_y, allele_b, PyxelColor.ACCENT)

        # Divider line
        pyxel.line(
            sx + 8, sy + 90, sx + sw - 8, sy + 90, PyxelColor.LEAF_SHADOW
        )

        # Row 3: Detected Genes
        pyxel.text(
            sx + 12, sy + 96, loc["detected_genes"], PyxelColor.TEXT_MUTED
        )

        gene_a_txt = (
            loc["yellow_dom"]
            if "A" in self.active_plant.genotype[0:2]
            else loc["green_rec"]
        )
        gene_b_txt = (
            loc["smooth_dom"]
            if "B" in self.active_plant.genotype[2:4]
            else loc["wrinkled_rec"]
        )

        # Display Detected Gene A
        g_ay = sy + 110
        # draw color box: yellow for dominant, green for recessive
        is_dom_a = "A" in self.active_plant.genotype[0:2]
        gene_a_color = PyxelColor.ACCENT if is_dom_a else PyxelColor.PEA_GREEN
        pyxel.rectb(sx + 16, g_ay, 14, 14, gene_a_color)
        pyxel.rectb(sx + 17, g_ay + 1, 12, 12, PyxelColor.DEEP_GLASS_NAVY)
        # Letter
        char_a = "A" if is_dom_a else "a"
        pyxel.text(sx + 21, g_ay + 5, char_a, PyxelColor.TEXT)
        # Text
        pyxel.text(sx + 36, g_ay + 5, gene_a_txt, PyxelColor.TEXT)

        # Display Detected Gene B
        g_by = sy + 130
        is_dom_b = "B" in self.active_plant.genotype[2:4]
        gene_b_color = PyxelColor.ACCENT if is_dom_b else PyxelColor.PEA_GREEN
        pyxel.rectb(sx + 16, g_by, 14, 14, gene_b_color)
        pyxel.rectb(sx + 17, g_by + 1, 12, 12, PyxelColor.DEEP_GLASS_NAVY)
        char_b = "B" if is_dom_b else "b"
        pyxel.text(sx + 21, g_by + 5, char_b, PyxelColor.TEXT)
        pyxel.text(sx + 36, g_by + 5, gene_b_txt, PyxelColor.TEXT)

        # Extra detailed text for level 3/4
        if self.analyzer_level >= 3:
            # Draw minor probability statistics indicator at the bottom
            pr_y = sy + 152
            pyxel.line(sx + 8, pr_y, sx + sw - 8, pr_y, PyxelColor.LEAF_SHADOW)

            p_lbl = (
                "Level 3: Genetic Probability Enabled"
                if self.analyzer_level == 3
                else "Level 4: Simulator Planning Mode"
            )
            pyxel.text(sx + 12, pr_y + 6, p_lbl, PyxelColor.CYAN_SCIENCE)

            # Simple Punnett summary preview
            pyxel.text(
                sx + 16,
                pr_y + 16,
                "P.Square combos fully unlocked.",
                PyxelColor.TEXT_MUTED,
            )

    def draw_plant_icon(self, x: int, y: int):
        # Draw terracotta flowerpot icon
        pyxel.rect(x + 2, y + 12, 12, 8, PyxelColor.TERRACOTTA)
        pyxel.rect(x, y + 10, 16, 3, PyxelColor.TOMATO_ORANGE)
        pyxel.rectb(x + 2, y + 12, 12, 8, PyxelColor.SOIL_DARK)
        pyxel.rectb(x, y + 10, 16, 3, PyxelColor.SOIL_DARK)
        # Stem
        pyxel.line(x + 8, y + 9, x + 8, y + 2, PyxelColor.LEAF_GREEN)
        # Leaves
        pyxel.line(x + 8, y + 5, x + 4, y + 3, PyxelColor.LEAF_HIGHLIGHT)
        pyxel.line(x + 8, y + 5, x + 12, y + 3, PyxelColor.LEAF_HIGHLIGHT)
        pyxel.line(x + 8, y + 2, x + 5, y + 0, PyxelColor.LEAF_HIGHLIGHT)
        pyxel.line(x + 8, y + 2, x + 11, y + 0, PyxelColor.LEAF_HIGHLIGHT)

    def draw_allele_box(self, x: int, y: int, txt: str, col: int):
        # Draw allele green border box
        pyxel.rectb(x, y, 46, 20, col)
        pyxel.rectb(x + 1, y + 1, 44, 18, PyxelColor.INK_SHADOW)
        # text inside centered
        self.draw_text_shadow(x + 15, y + 7, txt, PyxelColor.TEXT)

    # ------------------------------------------------------------------------------
    # Hardware Controls Drawing (Pokedex interface)
    # ------------------------------------------------------------------------------
    def draw_hardware_controls(self):
        # 1. Circular D-Pad on the lower-left
        # Center of D-Pad: X = 48, Y = 328
        cx, cy = 48, 328
        pyxel.circ(cx, cy, 22, PyxelColor.METAL_DARK)
        pyxel.circb(cx, cy, 22, PyxelColor.SOIL_DARK)
        # Bevel ring
        pyxel.circb(cx, cy, 20, PyxelColor.METAL_LIGHT)

        # D-pad cross buttons
        # Horizontal cross rect
        pyxel.rect(cx - 16, cy - 5, 32, 10, PyxelColor.INK_SHADOW)
        pyxel.rectb(cx - 16, cy - 5, 32, 10, PyxelColor.METAL_DARK)
        # Vertical cross rect
        pyxel.rect(cx - 5, cy - 16, 10, 32, PyxelColor.INK_SHADOW)
        pyxel.rectb(cx - 5, cy - 16, 10, 32, PyxelColor.METAL_DARK)

        # Directional arrows on buttons
        pyxel.text(cx - 13, cy - 2, "<", PyxelColor.TEXT_MUTED)
        pyxel.text(cx + 9, cy - 2, ">", PyxelColor.TEXT_MUTED)
        pyxel.text(cx - 2, cy - 14, "^", PyxelColor.TEXT_MUTED)
        pyxel.text(cx - 2, cy + 9, "v", PyxelColor.TEXT_MUTED)

        # 2. Glowing Square Green Leaf Button
        # Position: X = 95 to 148, Y = 295 to 348 (W = 53, H = 53)
        bx, by, bw, bh = 95, 295, 50, 50
        pyxel.rect(bx, by, bw, bh, PyxelColor.LEAF_GREEN)
        # 3D outer bevels
        pyxel.rectb(bx, by, bw, bh, PyxelColor.SOIL_DARK)
        pyxel.rectb(bx + 2, by + 2, bw - 4, bh - 4, PyxelColor.LEAF_SHADOW)
        pyxel.rectb(bx + 3, by + 3, bw - 6, bh - 6, PyxelColor.LEAF_HIGHLIGHT)

        # Draw stylized white Leaf outline icon inside the button
        lx, ly = bx + bw // 2, by + bh // 2
        # leaf stem line
        pyxel.line(lx - 12, ly + 12, lx + 12, ly - 12, PyxelColor.WHITE_PETAL)
        # Leaf blade outlines
        pyxel.line(lx - 12, ly + 12, lx - 10, ly + 4, PyxelColor.WHITE_PETAL)
        pyxel.line(lx - 10, ly + 4, lx - 2, ly - 4, PyxelColor.WHITE_PETAL)
        pyxel.line(lx - 2, ly - 4, lx + 6, ly - 8, PyxelColor.WHITE_PETAL)
        pyxel.line(lx + 6, ly - 8, lx + 12, ly - 12, PyxelColor.WHITE_PETAL)

        pyxel.line(lx - 12, ly + 12, lx - 4, ly + 10, PyxelColor.WHITE_PETAL)
        pyxel.line(lx - 4, ly + 10, lx + 4, ly + 6, PyxelColor.WHITE_PETAL)
        pyxel.line(lx + 4, ly + 6, lx + 8, ly - 2, PyxelColor.WHITE_PETAL)
        pyxel.line(lx + 8, ly - 2, lx + 12, ly - 12, PyxelColor.WHITE_PETAL)

        # leaf veins
        pyxel.line(lx - 4, ly + 4, lx - 6, ly + 8, PyxelColor.LEAF_HIGHLIGHT)
        pyxel.line(lx + 2, ly - 2, lx + 4, ly + 2, PyxelColor.LEAF_HIGHLIGHT)

        # 3. Vertical Roller Slider
        # Position: X = 165 to 180, Y = 295 to 345
        rx, ry, rw, rh = 165, 295, 15, 50
        pyxel.rect(rx, ry, rw, rh, PyxelColor.METAL_DARK)
        pyxel.rectb(rx, ry, rw, rh, PyxelColor.SOIL_DARK)
        # Roller ridges lines
        for r_y in range(ry + 4, ry + rh - 4, 4):
            pyxel.line(rx + 1, r_y, rx + rw - 2, r_y, PyxelColor.INK_SHADOW)
            pyxel.line(
                rx + 1, r_y + 1, rx + rw - 2, r_y + 1, PyxelColor.METAL_LIGHT
            )

        # Green slider cap marking level
        # Calculate level relative Y
        slider_y = ry + 4 + (self.analyzer_level - 1) * 12
        pyxel.rect(rx + 1, slider_y, rw - 2, 7, PyxelColor.SUCCESS_LIME)
        pyxel.rectb(rx + 1, slider_y, rw - 2, 7, PyxelColor.SOIL_DARK)

        # 4. Circular green glowing lens button
        # Position: X = 195 to 215, Y = 295 to 315
        lx_btn, ly_btn = 205, 305
        pyxel.circ(lx_btn, ly_btn, 10, PyxelColor.METAL_DARK)
        pyxel.circb(lx_btn, ly_btn, 10, PyxelColor.SOIL_DARK)
        # Glowing inner lens green
        pyxel.circ(lx_btn, ly_btn, 7, PyxelColor.LEAF_GREEN)
        pyxel.circb(lx_btn, ly_btn, 7, PyxelColor.SUCCESS_LIME)
        # Specular gloss dot on lens
        pyxel.pset(lx_btn - 3, ly_btn - 3, PyxelColor.GLASS_HIGHLIGHT)

        # 5. Orange indicator LED below roller
        # Position: X = 172, Y = 354
        led_x, led_y = 172, 354
        pyxel.circ(led_x, led_y, 2, PyxelColor.TOMATO_ORANGE)
        pyxel.circb(led_x, led_y, 2, PyxelColor.SOIL_DARK)
        # Small highlight shine on orange led
        pyxel.pset(led_x - 1, led_y - 1, PyxelColor.SUNLIT_CREAM)

        # Tiny label pointing to orange LED showing language status
        lang_code = "PT" if self.language == "pt-br" else "EN"
        pyxel.text(led_x + 8, led_y - 2, lang_code, PyxelColor.TEXT_MUTED)

    def draw_text_shadow(
        self,
        x: int,
        y: int,
        text: str,
        text_col: int,
        shadow_col: int = PyxelColor.INK_SHADOW,
    ):
        pyxel.text(x + 1, y + 1, text, shadow_col)
        pyxel.text(x, y, text, text_col)


if __name__ == "__main__":
    HandheldAnalyzerApp()
