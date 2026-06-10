# ruff: noqa: PLR0915, PLR2004, E501, B905, PLR0912, RUF015, B007, SIM113
"""Standalone Procedural Genetic Analyzer Experiment for Mendel's Greenhouse.

This script runs a Pyxel-based interactive sandbox showing a procedurally generated
genetic analyzer with the official four-level progression.
- Level 1: Phenotypic Observation
- Level 2: Genetic Sequencing
- Level 3: Probabilistic Analysis
- Level 4: Genetic Simulator

No .pyxres resources are loaded; all visual assets are procedurally rendered in code.
"""

import math
import random
from collections import Counter
from dataclasses import dataclass
from itertools import product

import pyxel

# ------------------------------------------------------------------------------
# Project Custom Palette (32 Colors)
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
# Genetics Engine Data & Logic
# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class Plant:
    genotype: str
    species: str
    generation: int = 0

    @property
    def phenotype(self) -> dict[str, str]:
        """Procedural translation of genotype to visible traits."""
        if self.species == "Mendel Pea":
            # A: Color (AA/Aa -> Yellow, aa -> Green)
            # B: Texture (BB/Bb -> Smooth, bb -> Wrinkled)
            g_a = self.genotype[0:2]
            g_b = self.genotype[2:4]
            return {
                "color": "Yellow" if "A" in g_a else "Green",
                "texture": "Smooth" if "B" in g_b else "Wrinkled",
            }
        if self.species == "Snapdragon":
            # A: Color (AA/Aa -> Red, aa -> White)
            # B: Height (BB/Bb -> Tall, bb -> Short)
            # C: Shape (CC/Cc -> Wide, cc -> Narrow)
            g_a = self.genotype[0:2]
            g_b = self.genotype[2:4]
            g_c = self.genotype[4:6]
            return {
                "color": "Red" if "A" in g_a else "White",
                "height": "Tall" if "B" in g_b else "Short",
                "shape": "Wide Petals" if "C" in g_c else "Narrow Petals",
            }
        return {}

    @property
    def phenotype_desc(self) -> str:
        traits = self.phenotype
        return ", ".join(traits.values())


def parse_genotype_pairs(genotype: str) -> list[str]:
    return [genotype[i : i + 2] for i in range(0, len(genotype), 2)]


def get_gametes(genotype: str) -> list[str]:
    pairs = parse_genotype_pairs(genotype)
    # Deduplicate within each pair to get alleles, e.g. "Aa" -> ('A', 'a')
    options = [tuple(dict.fromkeys(pair)) for pair in pairs]
    # Cartesian product
    prod = product(*options)
    # Sort for consistent order
    return sorted(["".join(g) for g in prod])


def combine_gametes(gamete_a: str, gamete_b: str) -> str:
    combined = []
    for a, b in zip(gamete_a, gamete_b):
        pair = sorted([a, b], key=lambda x: (x.islower(), x))
        combined.append("".join(pair))
    return "".join(combined)


def get_cross_probabilities(
    genotype_a: str, genotype_b: str
) -> dict[str, float]:
    gametes_a = get_gametes(genotype_a)
    gametes_b = get_gametes(genotype_b)
    counts = Counter()
    for g1 in gametes_a:
        for g2 in gametes_b:
            counts[combine_gametes(g1, g2)] += 1
    total = len(gametes_a) * len(gametes_b)
    return {gen: count / total for gen, count in sorted(counts.items())}


# ------------------------------------------------------------------------------
# App Definition
# ------------------------------------------------------------------------------
class ProceduralAnalyzerApp:
    def __init__(self):
        # 640x360 window
        pyxel.init(
            640, 360, title="Mendel's Greenhouse - Procedural Analyzer Sandbox"
        )
        pyxel.mouse(True)

        # Apply palette
        pyxel.colors[:] = PROJECT_PALETTE

        # Setup Pyxel Audio Channel Sounds for buttons/buzzes
        # Sound 0: Chime/Click
        pyxel.sounds[0].set("c3e3g3", "p", "777", "nnn", 5)
        # Sound 1: Simulator Hum
        pyxel.sounds[1].set(
            "c2c#2c2c#2c2c#2c2c#2", "s", "55555555", "nnnnnnnn", 3
        )
        # Sound 2: Success Ping
        pyxel.sounds[2].set("e3g3c4e4", "p", "7777", "nnff", 6)

        # Game State Variables
        self.active_species = "Mendel Pea"
        self.active_level = 3  # Level 1 to 4

        # Plant lists
        self.pea_inventory = [
            Plant("AABB", "Mendel Pea", 0),
            Plant("aabb", "Mendel Pea", 0),
            Plant("AaBb", "Mendel Pea", 0),
            Plant("Aabb", "Mendel Pea", 0),
            Plant("aaBb", "Mendel Pea", 0),
            Plant("AAbb", "Mendel Pea", 0),
            Plant("aaBB", "Mendel Pea", 0),
        ]
        self.snap_inventory = [
            Plant("AABBCC", "Snapdragon", 0),
            Plant("aabbcc", "Snapdragon", 0),
            Plant("AaBbCc", "Snapdragon", 0),
            Plant("Aabbcc", "Snapdragon", 0),
            Plant("aaBbcc", "Snapdragon", 0),
            Plant("AAbbCC", "Snapdragon", 0),
            Plant("aaBBCC", "Snapdragon", 0),
        ]

        self.selected_plant = self.pea_inventory[0]
        self.parent_a = None
        self.parent_b = None

        # Level 4 Simulator values
        self.target_genotype = ""
        self.sim_progress = -1  # -1 means idle
        self.simulated_offspring = []

        # Scrolling laser effect
        self.laser_y = 40
        self.laser_dir = 1

        # Particles inside tubes
        self.particles = []
        for _ in range(25):
            self.particles.append(
                {
                    "x": random.randint(305, 325),
                    "y": random.randint(40, 180),
                    "speed": random.uniform(0.5, 1.5),
                    "color": random.choice(
                        [PyxelColor.CYAN_SCIENCE, PyxelColor.LEAF_HIGHLIGHT]
                    ),
                }
            )

        pyxel.run(self.update, self.draw)

    def select_species(self, species: str):
        if self.active_species != species:
            pyxel.play(0, 0)
            self.active_species = species
            self.parent_a = None
            self.parent_b = None
            self.simulated_offspring = []
            self.sim_progress = -1
            if species == "Mendel Pea":
                self.selected_plant = self.pea_inventory[0]
                self.target_genotype = "aabb"
            else:
                self.selected_plant = self.snap_inventory[0]
                self.target_genotype = "aabbcc"

    def select_level(self, level: int):
        if self.active_level != level:
            pyxel.play(0, 0)
            self.active_level = level

    @property
    def inventory(self) -> list[Plant]:
        return (
            self.pea_inventory
            if self.active_species == "Mendel Pea"
            else self.snap_inventory
        )

    # ------------------------------------------------------------------------------
    # Update Loop
    # ------------------------------------------------------------------------------
    def update(self):
        # Update laser position
        self.laser_y += self.laser_dir * 1.5
        if self.laser_y >= 350 or self.laser_y <= 40:
            self.laser_dir *= -1

        # Update bubbles particles inside the reactor chamber
        for p in self.particles:
            p["y"] -= p["speed"]
            if p["y"] < 40:
                p["y"] = 180
                p["x"] = random.randint(305, 325)

        # Simulation progress increment
        if self.sim_progress >= 0:
            self.sim_progress += 1
            if self.sim_progress % 5 == 0 and self.sim_progress < 30:
                # Play simulation hum
                pyxel.play(1, 1)
            if self.sim_progress >= 30:
                self.sim_progress = -1
                pyxel.play(2, 2)
                # Generate 8 random offspring according to cross probabilities
                probs = get_cross_probabilities(
                    self.parent_a.genotype, self.parent_b.genotype
                )
                genotypes = list(probs.keys())
                weights = list(probs.values())

                self.simulated_offspring = []
                for _ in range(8):
                    # Simple weighted random choice
                    r = random.random()
                    cumulative = 0.0
                    chosen = genotypes[-1]
                    for g, w in zip(genotypes, weights):
                        cumulative += w
                        if r <= cumulative:
                            chosen = g
                            break
                    self.simulated_offspring.append(
                        Plant(
                            chosen,
                            self.active_species,
                            max(
                                self.parent_a.generation,
                                self.parent_b.generation,
                            )
                            + 1,
                        )
                    )

        # Handle Mouse Clicks
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            mx, my = pyxel.mouse_x, pyxel.mouse_y

            # Species selector tabs
            if 6 <= my <= 24:
                if 180 <= mx <= 240:
                    self.select_species("Mendel Pea")
                elif 245 <= mx <= 325:
                    self.select_species("Snapdragon")

            # Level selector tabs
            if 6 <= my <= 24:
                for i in range(1, 5):
                    tx = 350 + (i - 1) * 65
                    if tx <= mx <= tx + 60:
                        self.select_level(i)

            # Inventory list item selection
            # List region: X = 10 to 150, Y = 50 to 340. Slots are spaced by 28px
            if 10 <= mx <= 150 and 50 <= my <= 340:
                idx = (my - 50) // 28
                if 0 <= idx < len(self.inventory):
                    pyxel.play(0, 0)
                    self.selected_plant = self.inventory[idx]

            # Action Buttons in the Specimen Detail area
            # Button Parent A: X = 165 to 235, Y = 285 to 300
            # Button Parent B: X = 245 to 315, Y = 285 to 300
            if 285 <= my <= 300 and self.active_level >= 3:
                if 165 <= mx <= 235:
                    pyxel.play(0, 0)
                    self.parent_a = self.selected_plant
                    self.simulated_offspring = []
                elif 245 <= mx <= 315:
                    pyxel.play(0, 0)
                    self.parent_b = self.selected_plant
                    self.simulated_offspring = []

            # Reset Parent buttons (clicks inside slot borders)
            if self.parent_a and 335 <= mx <= 445 and 45 <= my <= 75:
                pyxel.play(0, 0)
                self.parent_a = None
                self.simulated_offspring = []
            if self.parent_b and 455 <= mx <= 565 and 45 <= my <= 75:
                pyxel.play(0, 0)
                self.parent_b = None
                self.simulated_offspring = []

            # Level 4 Interactive Simulator Targets selector
            if self.active_level == 4 and self.parent_a and self.parent_b:
                # We draw targets in the right column. X = 485 to 620, Y = 80 to 180
                # Spaced by 14px
                if 485 <= mx <= 620 and 80 <= my <= 190:
                    probs = get_cross_probabilities(
                        self.parent_a.genotype, self.parent_b.genotype
                    )
                    target_list = list(probs.keys())
                    t_idx = (my - 80) // 14
                    if 0 <= t_idx < len(target_list):
                        pyxel.play(0, 0)
                        self.target_genotype = target_list[t_idx]

                # Recommender Click
                # The recommendation panel is listed below target panel. Y = 195 to 260
                # Clicking a recommended parents slots them!
                if 485 <= mx <= 620 and 195 <= my <= 260:
                    rec_idx = (my - 195) // 20
                    recs = self.get_recommendations()
                    if 0 <= rec_idx < len(recs):
                        pyxel.play(0, 0)
                        p_a_gen, p_b_gen, _ = recs[rec_idx]
                        # find or create matching Plants
                        self.parent_a = next(
                            (
                                p
                                for p in self.inventory
                                if p.genotype == p_a_gen
                            ),
                            Plant(p_a_gen, self.active_species),
                        )
                        self.parent_b = next(
                            (
                                p
                                for p in self.inventory
                                if p.genotype == p_b_gen
                            ),
                            Plant(p_b_gen, self.active_species),
                        )
                        self.simulated_offspring = []

                # Breeding Trigger Button
                # Button coords: X = 338 to 478, Y = 195 to 215
                if (
                    338 <= mx <= 478
                    and 195 <= my <= 215
                    and self.parent_a
                    and self.parent_b
                ):
                    self.sim_progress = 0

            # Offspring clicks to inspect
            # Offspring are drawn in a bottom tray at X = 335 to 630, Y = 265 to 345
            # Spaced by 35px each, size 30x30
            if self.Y_OFFSPRING_TRAY <= my <= self.Y_OFFSPRING_TRAY + 35:
                o_idx = (mx - 335) // 36
                if 0 <= o_idx < len(self.simulated_offspring):
                    pyxel.play(0, 0)
                    self.selected_plant = self.simulated_offspring[o_idx]

    # Helper method for simulator recommendations
    def get_recommendations(self) -> list[tuple[str, str, float]]:
        """Find the best parent pairs in our inventory to produce the target genotype."""
        target = self.target_genotype
        if not target:
            return []

        matches = []
        # Query combinations in inventory
        for i in range(len(self.inventory)):
            for j in range(i, len(self.inventory)):
                p1 = self.inventory[i]
                p2 = self.inventory[j]
                probs = get_cross_probabilities(p1.genotype, p2.genotype)
                if target in probs:
                    matches.append((p1.genotype, p2.genotype, probs[target]))
        # Sort descending by probability
        matches.sort(key=lambda x: x[2], reverse=True)
        return matches[:3]

    # ------------------------------------------------------------------------------
    # Drawing Loop
    # ------------------------------------------------------------------------------
    def draw(self):
        # Clear screen to deep navy glass color
        pyxel.cls(PyxelColor.DEEP_GLASS_NAVY)

        # Grid overlay for cybernetic tech vibe
        for x in range(0, 640, 20):
            pyxel.line(x, 30, x, 360, PyxelColor.INK_SHADOW)
        for y in range(30, 360, 20):
            pyxel.line(0, y, 640, y, PyxelColor.INK_SHADOW)

        # Draw reactor glass chamber in the middle for style
        pyxel.rect(300, 32, 28, 150, PyxelColor.BLUE_GLASS)
        pyxel.rectb(300, 32, 28, 150, PyxelColor.METAL_LIGHT)
        # Draw particles inside
        for p in self.particles:
            pyxel.pset(int(p["x"]), int(p["y"]), p["color"])
        # Flask metal caps
        pyxel.rect(298, 29, 32, 4, PyxelColor.METAL_DARK)
        pyxel.rect(298, 181, 32, 4, PyxelColor.METAL_DARK)

        # Draw Header
        self.draw_header()

        # Draw Left Panel (Inventory)
        self.draw_inventory()

        # Draw Center Panel (Specimen Details)
        self.draw_details()

        # Draw Right Panel (Genetics Analyzer / Punnett Square)
        self.draw_workspace()

        # Render laser scan line animation
        pyxel.line(
            160, self.laser_y, 300, self.laser_y, PyxelColor.CYAN_SCIENCE
        )
        # Glow ends of the laser
        pyxel.pset(160, self.laser_y, PyxelColor.SUCCESS_LIME)
        pyxel.pset(300, self.laser_y, PyxelColor.SUCCESS_LIME)

        # Drawing custom cursor coordinate helper (if debug needed) or hover effect
        # Draw cursor pointer as a glowing dot
        pyxel.pset(pyxel.mouse_x, pyxel.mouse_y, PyxelColor.SUCCESS_LIME)

    # ------------------------------------------------------------------------------
    # Sub-Drawing Functions
    # ------------------------------------------------------------------------------
    def draw_header(self):
        # Top banner panel
        pyxel.rect(0, 0, 640, 30, PyxelColor.INK_SHADOW)
        pyxel.line(0, 30, 640, 30, PyxelColor.GENETIC_PURPLE)

        # Title
        self.draw_text_shadow(
            10,
            8,
            "MENDEL'S GREENHOUSE - GENETIC ANALYZER",
            PyxelColor.TEXT,
            PyxelColor.INK_SHADOW,
        )

        # Species Selector tabs
        pea_col = (
            PyxelColor.ACCENT
            if self.active_species == "Mendel Pea"
            else PyxelColor.TEXT_MUTED
        )
        snap_col = (
            PyxelColor.ACCENT
            if self.active_species == "Snapdragon"
            else PyxelColor.TEXT_MUTED
        )

        pyxel.rectb(
            180,
            5,
            60,
            18,
            PyxelColor.METAL_LIGHT
            if self.active_species == "Mendel Pea"
            else PyxelColor.METAL_DARK,
        )
        if self.active_species == "Mendel Pea":
            pyxel.rect(181, 6, 58, 16, PyxelColor.WARM_FLOOR)
        pyxel.text(188, 11, "Mendel Pea", pea_col)

        pyxel.rectb(
            245,
            5,
            80,
            18,
            PyxelColor.METAL_LIGHT
            if self.active_species == "Snapdragon"
            else PyxelColor.METAL_DARK,
        )
        if self.active_species == "Snapdragon":
            pyxel.rect(246, 6, 78, 16, PyxelColor.WARM_FLOOR)
        pyxel.text(253, 11, "Snapdragon", snap_col)

        # Levels tabs selector
        for i in range(1, 5):
            tx = 350 + (i - 1) * 65
            is_active = self.active_level == i
            tab_col = PyxelColor.ACCENT if is_active else PyxelColor.TEXT_MUTED

            pyxel.rectb(
                tx,
                5,
                60,
                18,
                PyxelColor.METAL_LIGHT if is_active else PyxelColor.METAL_DARK,
            )
            if is_active:
                pyxel.rect(tx + 1, 6, 58, 16, PyxelColor.WARM_FLOOR)
            pyxel.text(tx + 8, 11, f"L{i}: Level {i}", tab_col)

    def draw_inventory(self):
        # Panel boundary
        pyxel.rect(5, 32, 150, 320, PyxelColor.INK_SHADOW)
        pyxel.rectb(5, 32, 150, 320, PyxelColor.METAL_DARK)

        self.draw_text_shadow(
            10,
            38,
            "INVENTORY BINS",
            PyxelColor.CYAN_SCIENCE,
            PyxelColor.INK_SHADOW,
        )

        # Render list of seeds
        for idx, plant in enumerate(self.inventory):
            ty = 50 + idx * 28
            is_selected = self.selected_plant == plant

            # Hover check
            hover = (
                10 <= pyxel.mouse_x <= 150 and ty <= pyxel.mouse_y <= ty + 24
            )
            bg_col = (
                PyxelColor.WARM_FLOOR
                if is_selected
                else (
                    PyxelColor.METAL_DARK
                    if hover
                    else PyxelColor.DEEP_GLASS_NAVY
                )
            )
            border_col = (
                PyxelColor.ACCENT if is_selected else PyxelColor.METAL_DARK
            )

            pyxel.rect(8, ty, 144, 24, bg_col)
            pyxel.rectb(8, ty, 144, 24, border_col)

            # Miniature seed drawing (procedural)
            self.draw_plant_miniature(18, ty + 12, plant)

            # Label
            # If level 1, genotype is masked!
            if self.active_level == 1:
                label = plant.phenotype_desc
                if len(label) > 18:
                    label = label[:16] + "..."
                pyxel.text(35, ty + 9, label, PyxelColor.TEXT)
            else:
                pyxel.text(35, ty + 5, plant.genotype, PyxelColor.TEXT)
                pheno_lbl = plant.phenotype_desc
                if len(pheno_lbl) > 20:
                    pheno_lbl = pheno_lbl[:18] + ".."
                pyxel.text(35, ty + 14, pheno_lbl, PyxelColor.TEXT_MUTED)

    def draw_details(self):
        # Detail workspace frame
        pyxel.rect(160, 32, 135, 320, PyxelColor.INK_SHADOW)
        pyxel.rectb(160, 32, 135, 320, PyxelColor.METAL_DARK)

        self.draw_text_shadow(
            165,
            38,
            "SPECIMEN DETAILS",
            PyxelColor.CYAN_SCIENCE,
            PyxelColor.INK_SHADOW,
        )

        # Draw Large plant specimen model
        self.draw_large_plant_procedural(227, 95, self.selected_plant)

        # Details text
        label_y = 155

        # Visible Phenotype
        pyxel.text(165, label_y, "PHENOTYPE:", PyxelColor.TEXT_MUTED)
        traits = self.selected_plant.phenotype
        t_y = label_y + 10
        for k, v in traits.items():
            pyxel.text(175, t_y, f"- {k.capitalize()}: {v}", PyxelColor.TEXT)
            t_y += 9

        # Level 1 masks genetic sequencing
        if self.active_level == 1:
            pyxel.rect(165, t_y + 10, 125, 45, PyxelColor.METAL_DARK)
            pyxel.text(170, t_y + 15, "Genotype Data", PyxelColor.ERROR_EMBER)
            pyxel.text(
                170, t_y + 25, "LOCKED. Upgrade to", PyxelColor.TEXT_MUTED
            )
            pyxel.text(
                170, t_y + 35, "Level 2 sequencer.", PyxelColor.CYAN_SCIENCE
            )
            return

        # Genotype & Allele breakdown for Level 2+
        pyxel.text(
            165,
            t_y + 5,
            f"GENOTYPE: {self.selected_plant.genotype}",
            PyxelColor.ACCENT,
        )

        # Allele explanation
        a_y = t_y + 16
        pyxel.text(165, a_y, "ALLELES:", PyxelColor.TEXT_MUTED)
        a_y += 9

        if self.active_species == "Mendel Pea":
            g_a = self.selected_plant.genotype[0:2]
            g_b = self.selected_plant.genotype[2:4]
            pyxel.text(172, a_y, f"A/a: Seed Color ({g_a})", PyxelColor.TEXT)
            pyxel.text(
                172, a_y + 9, f"B/b: Texture    ({g_b})", PyxelColor.TEXT
            )
            a_y += 18
        else:
            g_a = self.selected_plant.genotype[0:2]
            g_b = self.selected_plant.genotype[2:4]
            g_c = self.selected_plant.genotype[4:6]
            pyxel.text(172, a_y, f"A/a: Color  ({g_a})", PyxelColor.TEXT)
            pyxel.text(172, a_y + 9, f"B/b: Height ({g_b})", PyxelColor.TEXT)
            pyxel.text(172, a_y + 18, f"C/c: Shape  ({g_c})", PyxelColor.TEXT)
            a_y += 27

        # Parent slots actions for Level 3+
        if self.active_level >= 3:
            # Slot buttons
            btn1_hover = (
                165 <= pyxel.mouse_x <= 223 and 280 <= pyxel.mouse_y <= 295
            )
            btn2_hover = (
                231 <= pyxel.mouse_x <= 290 and 280 <= pyxel.mouse_y <= 295
            )

            pyxel.rect(
                165,
                280,
                58,
                15,
                PyxelColor.METAL_LIGHT
                if btn1_hover
                else PyxelColor.METAL_DARK,
            )
            pyxel.rectb(
                165,
                280,
                58,
                15,
                PyxelColor.GLASS_HIGHLIGHT
                if btn1_hover
                else PyxelColor.METAL_LIGHT,
            )
            pyxel.text(170, 285, "Load Parent A", PyxelColor.TEXT)

            pyxel.rect(
                231,
                280,
                59,
                15,
                PyxelColor.METAL_LIGHT
                if btn2_hover
                else PyxelColor.METAL_DARK,
            )
            pyxel.rectb(
                231,
                280,
                59,
                15,
                PyxelColor.GLASS_HIGHLIGHT
                if btn2_hover
                else PyxelColor.METAL_LIGHT,
            )
            pyxel.text(236, 285, "Load Parent B", PyxelColor.TEXT)

    def draw_workspace(self):
        # Frame
        pyxel.rect(330, 32, 305, 320, PyxelColor.INK_SHADOW)
        pyxel.rectb(330, 32, 305, 320, PyxelColor.METAL_DARK)

        title_map = {
            1: "OBSERVATION MODE",
            2: "SEQUENCING DATA",
            3: "PROBABILISTIC MATRIX",
            4: "GENETIC CHROMOSOME SIMULATOR",
        }
        self.draw_text_shadow(
            335,
            38,
            f"WORKSPACE: {title_map[self.active_level]}",
            PyxelColor.CYAN_SCIENCE,
            PyxelColor.INK_SHADOW,
        )

        # Slots for Parents
        self.draw_parent_slots()

        # Render main contents based on level
        if self.active_level <= 2:
            self.draw_procedural_helix_screen()
        elif self.active_level == 3:
            self.draw_punnett_probabilities_view()
        elif self.active_level == 4:
            self.draw_simulator_view()

    def draw_parent_slots(self):
        # Slot Parent A
        slot_a_col = (
            PyxelColor.METAL_LIGHT if self.parent_a else PyxelColor.METAL_DARK
        )
        pyxel.rectb(335, 48, 110, 24, slot_a_col)
        if self.parent_a:
            pyxel.rect(336, 49, 108, 22, PyxelColor.DEEP_GLASS_NAVY)
            pyxel.text(
                342, 57, f"A: {self.parent_a.genotype}", PyxelColor.ACCENT
            )
            # draw click to reset cross button
            pyxel.text(435, 57, "x", PyxelColor.ERROR_EMBER)
        else:
            pyxel.text(342, 57, "[Parent A Empty]", PyxelColor.TEXT_MUTED)

        # Slot Parent B
        slot_b_col = (
            PyxelColor.METAL_LIGHT if self.parent_b else PyxelColor.METAL_DARK
        )
        pyxel.rectb(455, 48, 110, 24, slot_b_col)
        if self.parent_b:
            pyxel.rect(456, 49, 108, 22, PyxelColor.DEEP_GLASS_NAVY)
            pyxel.text(
                462, 57, f"B: {self.parent_b.genotype}", PyxelColor.ACCENT
            )
            pyxel.text(555, 57, "x", PyxelColor.ERROR_EMBER)
        else:
            pyxel.text(462, 57, "[Parent B Empty]", PyxelColor.TEXT_MUTED)

    # Draws a cool scanning DNA helix in L1/L2
    def draw_procedural_helix_screen(self):
        center_x = 482
        center_y = 200

        pyxel.text(
            342, 85, "DIAGNOSTIC DISPLAY ACTIVE", PyxelColor.CYAN_SCIENCE
        )
        pyxel.text(
            342, 98, "Punnett Square combinations", PyxelColor.TEXT_MUTED
        )
        pyxel.text(342, 108, "locked at this level.", PyxelColor.TEXT_MUTED)

        # Double helix animation
        t = pyxel.frame_count * 0.05
        for cy in range(-60, 60, 4):
            # Coordinates
            angle = cy * 0.15 + t
            dx1 = math.sin(angle) * 20
            dx2 = math.sin(angle + math.pi) * 20

            # draw rung line
            pyxel.line(
                int(center_x + dx1),
                center_y + cy,
                int(center_x + dx2),
                center_y + cy,
                PyxelColor.METAL_DARK,
            )

            # Nodes
            pyxel.circ(
                int(center_x + dx1), center_y + cy, 2, PyxelColor.CYAN_SCIENCE
            )
            pyxel.circ(
                int(center_x + dx2),
                center_y + cy,
                2,
                PyxelColor.GENETIC_PURPLE,
            )

    # Layout offsets
    Y_OFFSPRING_TRAY = 270

    def draw_punnett_probabilities_view(self):
        if not self.parent_a or not self.parent_b:
            pyxel.text(
                345, 120, "PLEASE LOAD BOTH PARENTS", PyxelColor.ERROR_EMBER
            )
            pyxel.text(
                345,
                132,
                "to analyze Mendelian probabilities.",
                PyxelColor.TEXT_MUTED,
            )
            return

        # Perform calculations
        g1 = self.parent_a.genotype
        g2 = self.parent_b.genotype
        gametes_a = get_gametes(g1)
        gametes_b = get_gametes(g2)

        # Draw Punnett Grid
        # Left margin = 340, Top = 85
        # Cell size: dynamic based on number of gametes to fit comfortably.
        # Pea has 1, 2, or 4 gametes. Snapdragon has 1, 2, 4, or 8.
        # We cap grid size at 4x4 for Pea, or fit up to 4x4.
        sz_a = min(len(gametes_a), 4)
        sz_b = min(len(gametes_b), 4)

        cell_w = 26
        cell_h = 20
        grid_start_x = 380
        grid_start_y = 110

        # Draw labels
        pyxel.text(
            grid_start_x - 30,
            grid_start_y - 12,
            "Gametes:",
            PyxelColor.CYAN_SCIENCE,
        )

        # Columns (Parent A)
        for c in range(sz_a):
            px = grid_start_x + c * cell_w
            pyxel.rect(
                px, grid_start_y - 14, cell_w - 2, 10, PyxelColor.METAL_DARK
            )
            pyxel.text(
                px + 4,
                grid_start_y - 12,
                gametes_a[c],
                PyxelColor.CYAN_SCIENCE,
            )

        # Rows (Parent B)
        for r in range(sz_b):
            py = grid_start_y + r * cell_h
            pyxel.rect(
                grid_start_x - 30, py, 26, cell_h - 2, PyxelColor.METAL_DARK
            )
            pyxel.text(
                grid_start_x - 26,
                py + 7,
                gametes_b[r],
                PyxelColor.CYAN_SCIENCE,
            )

        # Grid Cells
        for r in range(sz_b):
            for c in range(sz_a):
                px = grid_start_x + c * cell_w
                py = grid_start_y + r * cell_h

                # Combine
                combined = combine_gametes(gametes_a[c], gametes_b[r])

                # Draw cell
                pyxel.rect(
                    px, py, cell_w - 2, cell_h - 2, PyxelColor.DEEP_GLASS_NAVY
                )
                pyxel.rectb(
                    px, py, cell_w - 2, cell_h - 2, PyxelColor.METAL_DARK
                )

                # Print inside (truncated if Snapdragon)
                display_gen = combined
                if len(display_gen) > 4:
                    display_gen = display_gen[:4]
                pyxel.text(
                    px + 2, py + 7, display_gen, PyxelColor.PARCHMENT_LIGHT
                )

        # Draw Expected Offspring Probabilities List
        probs = get_cross_probabilities(g1, g2)
        pr_x = 505
        pr_y = 110
        pyxel.text(pr_x, pr_y - 12, "EXPECTED RATIOS:", PyxelColor.ACCENT)

        count = 0
        for gen, prob in probs.items():
            if count >= 8:
                pyxel.text(pr_x, pr_y, "...more", PyxelColor.TEXT_MUTED)
                break
            pct = prob * 100
            pyxel.text(pr_x, pr_y, f"{gen}: {pct:.1f}%", PyxelColor.TEXT)
            pr_y += 11
            count += 1

        # Dihybrid 9:3:3:1 ratio badge check
        # Pea dihybrid cross AaBb x AaBb
        if (
            self.active_species == "Mendel Pea"
            and g1 == "AaBb"
            and g2 == "AaBb"
        ):
            pyxel.rect(340, 210, 280, 24, PyxelColor.METAL_DARK)
            pyxel.rectb(340, 210, 280, 24, PyxelColor.ACCENT)
            pyxel.text(
                348,
                219,
                "Mendel Dihybrid Cross Detected: 9:3:3:1 Phenotype ratio",
                PyxelColor.SUCCESS_LIME,
            )

    def draw_simulator_view(self):
        if not self.parent_a or not self.parent_b:
            pyxel.text(
                345, 120, "PLEASE LOAD BOTH PARENTS", PyxelColor.ERROR_EMBER
            )
            pyxel.text(
                345,
                132,
                "to active the Genetic Simulator.",
                PyxelColor.TEXT_MUTED,
            )
            return

        g1 = self.parent_a.genotype
        g2 = self.parent_b.genotype
        gametes_a = get_gametes(g1)
        gametes_b = get_gametes(g2)
        probs = get_cross_probabilities(g1, g2)

        # Check default target genotype is valid for this cross
        if self.target_genotype not in probs:
            self.target_genotype = list(probs.keys())[0]

        # Draw Punnett Matrix (Mini 4x4)
        sz_a = min(len(gametes_a), 4)
        sz_b = min(len(gametes_b), 4)
        cell_w = 26
        cell_h = 20
        grid_start_x = 375
        grid_start_y = 100

        # Columns
        for c in range(sz_a):
            px = grid_start_x + c * cell_w
            pyxel.text(
                px + 4,
                grid_start_y - 10,
                gametes_a[c],
                PyxelColor.CYAN_SCIENCE,
            )
        # Rows
        for r in range(sz_b):
            py = grid_start_y + r * cell_h
            pyxel.text(
                grid_start_x - 18,
                py + 7,
                gametes_b[r],
                PyxelColor.CYAN_SCIENCE,
            )

        # Renders grid and highlights matching cells
        # Pulse animation factor
        pulse = (math.sin(pyxel.frame_count * 0.3) + 1.0) * 0.5
        pulse_color = (
            PyxelColor.CYAN_SCIENCE
            if pulse > 0.5
            else PyxelColor.GENETIC_PURPLE
        )

        for r in range(sz_b):
            for c in range(sz_a):
                px = grid_start_x + c * cell_w
                py = grid_start_y + r * cell_h
                combined = combine_gametes(gametes_a[c], gametes_b[r])

                is_match = combined == self.target_genotype
                bg = (
                    PyxelColor.WARM_FLOOR
                    if is_match
                    else PyxelColor.DEEP_GLASS_NAVY
                )
                border = pulse_color if is_match else PyxelColor.METAL_DARK

                pyxel.rect(px, py, cell_w - 2, cell_h - 2, bg)
                pyxel.rectb(px, py, cell_w - 2, cell_h - 2, border)

                display_gen = combined
                if len(display_gen) > 4:
                    display_gen = display_gen[:4]
                pyxel.text(
                    px + 2,
                    py + 7,
                    display_gen,
                    PyxelColor.PARCHMENT_LIGHT
                    if is_match
                    else PyxelColor.TEXT_MUTED,
                )

        # Target Selector Panel
        tr_x = 485
        tr_y = 80
        pyxel.text(tr_x, tr_y, "SELECT TARGET:", PyxelColor.CYAN_SCIENCE)
        tr_y += 10

        target_list = list(probs.keys())
        for idx, t_gen in enumerate(target_list):
            if idx >= 6:
                break
            is_active_target = t_gen == self.target_genotype
            col = PyxelColor.ACCENT if is_active_target else PyxelColor.TEXT
            pyxel.text(
                tr_x + 6, tr_y, f"{t_gen} ({probs[t_gen] * 100:.1f}%)", col
            )
            if is_active_target:
                pyxel.rectb(tr_x, tr_y - 2, 130, 9, PyxelColor.CYAN_SCIENCE)
            tr_y += 11

        # Recommendations panel (AI assistance)
        rec_y = 155
        pyxel.text(tr_x, rec_y, "SUGGESTED PARENTS:", PyxelColor.ACCENT)
        rec_y += 10
        recs = self.get_recommendations()

        if not recs:
            pyxel.text(
                tr_x + 5, rec_y, "No inventory match", PyxelColor.TEXT_MUTED
            )
        else:
            for r_idx, (p1, p2, p_chance) in enumerate(recs):
                label = f"{p1} x {p2} ({p_chance * 100:.0f}%)"
                # hover
                hover = (
                    tr_x <= pyxel.mouse_x <= tr_x + 130
                    and rec_y <= pyxel.mouse_y <= rec_y + 9
                )
                col = PyxelColor.SUCCESS_LIME if hover else PyxelColor.TEXT
                pyxel.text(tr_x + 5, rec_y, label, col)
                rec_y += 11

        # Simulate breeding section
        btn_hover = 338 <= pyxel.mouse_x <= 478 and 215 <= pyxel.mouse_y <= 235
        btn_col = (
            PyxelColor.SUCCESS_LIME if btn_hover else PyxelColor.METAL_LIGHT
        )

        pyxel.rect(338, 215, 140, 20, PyxelColor.METAL_DARK)
        pyxel.rectb(338, 215, 140, 20, btn_col)
        pyxel.text(348, 222, "COMBINE CHROMOSOMES", btn_col)

        # Simulation processing animation
        if self.sim_progress >= 0:
            # Draw progress bar
            pct = self.sim_progress / 30.0
            p_w = int(140 * pct)
            pyxel.rect(338, 215, p_w, 20, PyxelColor.SUCCESS_LIME)
            pyxel.text(348, 222, "COMBINING...", PyxelColor.INK_SHADOW)

            # Rising molecular particles effect
            for i in range(5):
                part_x = 338 + (i * 28) + (pyxel.frame_count % 10)
                part_y = 210 - (self.sim_progress * 2) + (i * 4)
                if part_y > 100:
                    pyxel.circ(part_x, part_y, 2, PyxelColor.CYAN_SCIENCE)

        # Offspring tray output display
        self.draw_offspring_tray()

    def draw_offspring_tray(self):
        # Draw background tray line
        pyxel.rect(
            335, self.Y_OFFSPRING_TRAY - 5, 296, 45, PyxelColor.METAL_DARK
        )
        pyxel.rectb(
            335, self.Y_OFFSPRING_TRAY - 5, 296, 45, PyxelColor.METAL_LIGHT
        )

        if not self.simulated_offspring:
            pyxel.text(
                350,
                self.Y_OFFSPRING_TRAY + 15,
                "OFFSPRING BINS READY - RUN COMBINATOR",
                PyxelColor.TEXT_MUTED,
            )
            return

        for idx, child in enumerate(self.simulated_offspring):
            cx = 345 + idx * 36
            cy = self.Y_OFFSPRING_TRAY + 18

            # Renders miniature slot
            is_hover = (
                cx - 15 <= pyxel.mouse_x <= cx + 15
                and cy - 18 <= pyxel.mouse_y <= cy + 18
            )
            border_col = (
                PyxelColor.ACCENT if is_hover else PyxelColor.METAL_LIGHT
            )

            pyxel.rect(cx - 15, cy - 18, 30, 36, PyxelColor.DEEP_GLASS_NAVY)
            pyxel.rectb(cx - 15, cy - 18, 30, 36, border_col)

            self.draw_plant_miniature(cx, cy - 3, child)

            # Print abbreviated genotype label
            g_lbl = child.genotype
            if len(g_lbl) > 4:
                g_lbl = g_lbl[:4]
            pyxel.text(cx - 11, cy + 9, g_lbl, PyxelColor.PARCHMENT_LIGHT)

    # ------------------------------------------------------------------------------
    # High-Fidelity Procedural Drawing Helpers
    # ------------------------------------------------------------------------------
    def draw_plant_miniature(self, x: int, y: int, plant: Plant):
        """Procedural drawing of miniature representation (thumbnail) of seeds/flowers."""
        if plant.species == "Mendel Pea":
            # Color
            col = (
                PyxelColor.SEED_GOLD
                if plant.phenotype["color"] == "Yellow"
                else PyxelColor.LEAF_GREEN
            )

            # Smooth vs Wrinkled
            if plant.phenotype["texture"] == "Smooth":
                pyxel.circ(x, y, 4, col)
                pyxel.circb(x, y, 4, PyxelColor.SOIL_DARK)
                # shine dot
                pyxel.pset(x - 1, y - 1, PyxelColor.GLASS_HIGHLIGHT)
            else:
                # Draws a small wavy blob
                pyxel.circ(x, y, 3, col)
                pyxel.pset(x - 4, y, col)
                pyxel.pset(x + 4, y, col)
                pyxel.pset(x, y - 4, col)
                pyxel.pset(x, y + 4, col)

                # outline corners
                pyxel.pset(x - 3, y - 3, PyxelColor.SOIL_DARK)
                pyxel.pset(x + 3, y - 3, PyxelColor.SOIL_DARK)
                pyxel.pset(x - 3, y + 3, PyxelColor.SOIL_DARK)
                pyxel.pset(x + 3, y + 3, PyxelColor.SOIL_DARK)
        else:  # Snapdragon
            # stem line
            pyxel.line(x, y - 3, x, y + 5, PyxelColor.LEAF_GREEN)

            # Flower color
            col = (
                PyxelColor.TOMATO_RED
                if plant.phenotype["color"] == "Red"
                else PyxelColor.WHITE_PETAL
            )
            # draw simple cross/star flower
            pyxel.pset(x, y - 3, col)
            pyxel.pset(x - 2, y - 4, col)
            pyxel.pset(x + 2, y - 4, col)
            # center yellow pistil
            pyxel.pset(x, y - 4, PyxelColor.ACCENT)

    def draw_large_plant_procedural(self, x: int, y: int, plant: Plant):
        """High-Fidelity Procedural drawing of large plant details."""
        if plant.species == "Mendel Pea":
            # Draws a detailed laboratory jar holding a large pea seed
            # Glass Jar outline
            pyxel.rect(x - 25, y - 30, 50, 60, PyxelColor.BLUE_GLASS)
            pyxel.rectb(x - 25, y - 30, 50, 60, PyxelColor.METAL_LIGHT)
            # Glass highlight sheen lines
            pyxel.line(
                x - 20, y - 25, x - 20, y + 25, PyxelColor.GLASS_HIGHLIGHT
            )
            pyxel.line(
                x - 16, y - 25, x - 16, y - 10, PyxelColor.GLASS_HIGHLIGHT
            )

            # Metal base / lid
            pyxel.rect(x - 27, y - 34, 54, 5, PyxelColor.METAL_DARK)
            pyxel.rect(x - 27, y + 30, 54, 5, PyxelColor.METAL_DARK)

            # Floating bubbles inside jar
            b_offset = (pyxel.frame_count // 3) % 40
            pyxel.pset(x - 12, y + 20 - b_offset, PyxelColor.CYAN_SCIENCE)
            pyxel.pset(x + 15, y + 10 - b_offset, PyxelColor.CYAN_SCIENCE)
            pyxel.pset(x + 2, y + 30 - b_offset, PyxelColor.CYAN_SCIENCE)

            # Large Seed
            col = (
                PyxelColor.SEED_GOLD
                if plant.phenotype["color"] == "Yellow"
                else PyxelColor.LEAF_GREEN
            )

            if plant.phenotype["texture"] == "Smooth":
                # Shaded seed
                pyxel.circ(x, y, 16, col)
                # Outer shadow outline
                pyxel.circb(x, y, 16, PyxelColor.SOIL_DARK)
                # High specular glass-like reflection
                pyxel.circ(x - 5, y - 5, 4, PyxelColor.WHITE_PETAL)
                pyxel.pset(x - 5, y - 5, PyxelColor.GLASS_HIGHLIGHT)
                # Highlight crescent curve
                pyxel.line(
                    x + 4,
                    y + 10,
                    x + 10,
                    y + 4,
                    PyxelColor.SUNLIT_CREAM
                    if plant.phenotype["color"] == "Yellow"
                    else PyxelColor.LEAF_HIGHLIGHT,
                )
            else:  # Wrinkled
                # Draw seed with custom wavy perimeter
                for angle in range(0, 360, 15):
                    rad = angle * math.pi / 180.0
                    dist = (
                        16
                        + math.sin(angle * 0.1 + pyxel.frame_count * 0.1) * 2.0
                    )
                    px = int(x + math.cos(rad) * dist)
                    py = int(y + math.sin(rad) * dist)
                    pyxel.line(x, y, px, py, col)

                # Outer outline
                for angle in range(0, 360, 5):
                    rad = angle * math.pi / 180.0
                    dist = (
                        16
                        + math.sin(angle * 0.1 + pyxel.frame_count * 0.1) * 2.0
                    )
                    px = int(x + math.cos(rad) * dist)
                    py = int(y + math.sin(rad) * dist)
                    pyxel.pset(px, py, PyxelColor.SOIL_DARK)

                # Shine spot inside
                pyxel.circ(x - 4, y - 4, 3, PyxelColor.GLASS_HIGHLIGHT)
        else:  # Snapdragon
            # Soil Pot
            pyxel.rect(x - 20, y + 25, 40, 12, PyxelColor.TERRACOTTA)
            pyxel.rect(x - 22, y + 22, 44, 4, PyxelColor.WOOD_MIDTONE)
            pyxel.rectb(x - 20, y + 25, 40, 12, PyxelColor.SOIL_DARK)

            # Stem height
            tall = plant.phenotype["height"] == "Tall"
            stem_y = y + 22
            top_y = y - 25 if tall else y + 0

            pyxel.line(x, stem_y, x, top_y, PyxelColor.LEAF_GREEN)
            pyxel.line(x - 1, stem_y, x - 1, top_y, PyxelColor.LEAF_SHADOW)

            # Leaves along stem
            pyxel.line(x, top_y + 15, x + 8, top_y + 10, PyxelColor.LEAF_GREEN)
            pyxel.line(x, top_y + 25, x - 8, top_y + 20, PyxelColor.LEAF_GREEN)

            # Flower Bloom at the top Y
            flower_col = (
                PyxelColor.TOMATO_RED
                if plant.phenotype["color"] == "Red"
                else PyxelColor.WHITE_PETAL
            )

            # Draw Snapdragon detailed flower head
            wide_petals = plant.phenotype["shape"] == "Wide Petals"
            pr = 10 if wide_petals else 6

            # 5-lobed petals
            pyxel.circ(x, top_y - 8, pr, flower_col)
            pyxel.circ(x - 8, top_y - 2, pr, flower_col)
            pyxel.circ(x + 8, top_y - 2, pr, flower_col)
            pyxel.circ(x - 5, top_y + 6, pr - 1, flower_col)
            pyxel.circ(x + 5, top_y + 6, pr - 1, flower_col)

            # Petal outlines
            pyxel.circb(x, top_y - 8, pr, PyxelColor.SOIL_DARK)
            pyxel.circb(x - 8, top_y - 2, pr, PyxelColor.SOIL_DARK)
            pyxel.circb(x + 8, top_y - 2, pr, PyxelColor.SOIL_DARK)

            # Golden Pistil / Stamen
            pyxel.circ(x, top_y, 3, PyxelColor.ACCENT)
            pyxel.circb(x, top_y, 3, PyxelColor.SOIL_DARK)

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


# Start sandbox
if __name__ == "__main__":
    ProceduralAnalyzerApp()
