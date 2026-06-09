# Greenhouse Screen

## Purpose

The Greenhouse Screen, shown to players as the Garden Scene, manages stored
plants, parent selection, analysis, discard decisions, and slot pressure.

Detailed scene decomposition and the official visual target live in
[../scenes/garden/README.md](../scenes/garden/README.md).

## Capacity

Maximum capacity:

```text
20 slots
5 x 4
```

Initial capacity:

```text
4 slots
```

Initial plants:

```text
AABB
aabb
```

## Layout

```text
+--------------------------------------------------+
| Greenhouse                 Slots: 6/20           |
+--------------------------------------------------+
| [Plant] [Plant] [Empty] [Empty] [Locked]         |
| [Plant] [Empty] [Locked][Locked][Locked]         |
| [Locked][Locked][Locked][Locked][Locked]         |
| [Locked][Locked][Locked][Locked][Locked]         |
+--------------------------+-----------------------+
| Selected Plant Details   | Actions               |
| Phenotype / Genotype     | Select Parent / Discard |
+--------------------------+-----------------------+
```

## Slot Types

- Pure plant.
- Stored hybrid.
- Rare offspring.
- Empty slot.
- Locked slot.
- Reserved contract plant.

## Actions

- Select as Parent A.
- Select as Parent B.
- Inspect.
- Discard non-founder plants when rules allow it.
- Reserve for contract.
- Move to another slot.

## States

- Empty.
- Occupied.
- Locked.
- Selected.
- Reserved.
- Deliverable.
- Newly discovered.

## Information Visibility

Cards must show only information allowed by analyzer level.
