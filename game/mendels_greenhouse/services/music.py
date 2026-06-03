"""Runtime music initialization service."""

import pyxel


def init_music() -> None:
    """Initialize the background music using MML at runtime.

    This is required because Pyxel does not fully persist MML-defined
    sounds in the binary .pyxres file.
    """
    # Track 0: Melody (Plucked bell/music-box style in G Major)
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

    pyxel.sounds[5].mml(" ".join(track0_parts))
    pyxel.sounds[6].mml(" ".join(track1_parts))
    pyxel.sounds[7].mml(" ".join(track2_parts))
    pyxel.musics[0].set([5], [6], [7])
