# Audio Assets

## Purpose

Audio reinforces feedback, pacing, and the cozy scientific greenhouse fantasy.

Audio should help the player understand what happened without making repeated experimentation tiring.

## Style Direction

The soundscape should feel:

- Cozy.
- Botanical.
- Lightly mechanical.
- Curious and scientific.
- Warm rather than arcade-harsh.

Avoid:

- Loud alarms.
- Harsh industrial loops.
- Overly magical fantasy sounds that imply non-Mendelian mechanics.
- Long reward sounds that interrupt repeated play.

## Music

Music should be:

- Calm.
- Loopable.
- Low fatigue.
- Suitable for planning and repeated experimentation.
- Lightly botanical/laboratory themed.

Suggested instrumentation style:

- Soft chiptune leads.
- Warm plucks.
- Gentle bell tones.
- Light bass.
- Subtle greenhouse ambience.

## Sound Effects

| Event | Direction |
| ----- | --------- |
| Button click | short wooden/glass click |
| Parent selected | soft plant label tick |
| Crossbreeding starts | gentle machine start plus pollen shimmer |
| Offspring appears | soft pop/grow sound |
| Contract progress | positive short chime |
| Contract complete | warm reward stinger |
| Discovery | bright but brief sparkle |
| Analyzer opens | soft electronic hum |
| Probability revealed | light sequence of tones |
| Invalid action | soft muted knock, not harsh |
| Germination bed reveal | soft soil, seed, and sprout accents |

## Pyxel Resource Requirements

Audio should live in:

```text
game/mendels_greenhouse/assets/mendels_greenhouse.pyxres
```

Use Pyxel sound and music banks for production runtime audio.

## MCP Verification

When `pyxel-mcp` is available:

- Use `render_audio` to verify sounds and music are not silent.
- Check waveform duration for short UI effects.
- Check loopable tracks for abrupt endings.
- Record any audio checks in the implementation notes or PR description.

When MCP is not available, use direct Pyxel smoke checks and manual listening.

## Rules

- Audio must not replace visual feedback.
- Repeated core-loop sounds must be subtle.
- Discovery and reward sounds may be more expressive but should stay brief.
- Sounds should support both casual play and classroom use.
