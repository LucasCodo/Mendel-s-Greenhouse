# Shop Screen

## Purpose

The Shop Screen lets players spend credits on progression.

## Purchases

- Greenhouse slots.
- New species.
- Genetic analyzer upgrades.

## Layout

```text
+------------------------------------------------------------+
| Shop                                      Credits: 2500     |
+------------------+------------------+----------------------+
| Greenhouse Slots | Analyzer         | Species              |
| Slot 7 - 100     | Level 2 - 500    | Snapdragon - 3000    |
| Slot 8 - 125     | Level 3 - 2000   | Corn - 10000         |
+------------------+------------------+----------------------+
| Selected Upgrade Details                [Buy]              |
+------------------------------------------------------------+
```

## Upgrade Cards

Each card shows:

- Upgrade name.
- Cost.
- Requirement.
- Benefit.
- Current locked/unlocked state.

## States

- Affordable.
- Not enough credits.
- Locked by prerequisite.
- Already purchased.

## Feedback

- Successful purchase shows unlock popup.
- Failed purchase explains missing credits or prerequisite.
- Analyzer upgrades must clearly state new information unlocked.
