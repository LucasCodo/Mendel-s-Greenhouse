# Mechanics Specs

This directory contains the official gameplay system rules for Mendel's Greenhouse.

Use this directory when implementing or changing gameplay behavior.

## Reading Order

1. [gameplay.md](gameplay.md) - Formal rules for crossbreeding, inheritance, offspring generation, contract resolution, storage, sale, discoveries, and impossibility checks.
2. [contracts.md](contracts.md) - Procedural contract types, resolution modes, constraints, scaling, and validity criteria.
3. [progression.md](progression.md) - Greenhouse, genetic analyzer, species, and contract progression.
4. [collection.md](collection.md) - Discovery, collection, milestones, and completion rules.
5. [data-model.md](data-model.md) - Conceptual gameplay entities, responsibilities, relationships, and rules.

## Related Specs

- [../GDD.md](../GDD.md) - high-level game design.
- [../GBD.md](../GBD.md) - economy and balance values.
- [../content/content-bible.md](../content/content-bible.md) - species and genetic content.
- [../education/learning-objectives.md](../education/learning-objectives.md) - educational mapping.
- [../ui/README.md](../ui/README.md) - interface specifications.

## Rule

Do not implement a mechanic from memory. Load the smallest relevant file from this directory first.
