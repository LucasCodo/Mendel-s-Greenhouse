# Mendel's Greenhouse

**Learn genetics by growing, crossing and discovering plants.**

Mendel's Greenhouse is an educational single-player game about classical genetics, inspired by Mendel's Second Law: the Law of Independent Assortment.

Players manage a genetic greenhouse, crossbreed plants, observe offspring on a production conveyor, complete client contracts, expand their greenhouse, and build a collection of discovered species, phenotypes, and genotypes.

## Concept

The game teaches genetics through experimentation instead of long theoretical explanations. Players learn by selecting parent plants, observing inheritance patterns, forming hypotheses, and using those discoveries to solve increasingly complex contracts.

Core concepts include:

- Genes and alleles
- Genotypes and phenotypes
- Dominance and recessiveness
- Homozygosity and heterozygosity
- Genetic probability
- Independent assortment

## Main Mechanics

- **Crossbreeding:** select parent plants and generate offspring from inherited alleles.
- **Contracts:** fulfill client requests for phenotypes, genotypes, or probabilities.
- **Collection:** permanently register discovered species, phenotypes, and genotypes.
- **Greenhouse management:** decide what to store, sell, use, or deliver.
- **Genetic progression:** unlock deeper genetic information through the genetic analyzer.

## Educational Goals

Mendel's Greenhouse is designed so that learning emerges from play. The player should understand genetics by experimenting, observing results, and applying knowledge to practical goals.

The intended learning progression is:

```text
Phenotype
->
Genotype
->
Probability
->
Genetic Planning
```

## Status

The project is in active design and documentation. Mechanics, balance values, and content may change through prototyping and playtesting.

The approved visual direction is pixel art, and the approved game engine is [Pyxel](https://github.com/kitao/pyxel). The project is intended to become a web game. For now, implementation should focus only on the game; a future NiceGUI layer is planned for user accounts and save management.

Initial language support will include English and Brazilian Portuguese.

## Domains

Official project domains:

- [mendelsgreenhouse.com](https://mendelsgreenhouse.com)
- [mendelsgreenhouse.com.br](https://mendelsgreenhouse.com.br)

## Documentation Structure

Detailed game rules live in [`specs/`](specs/). Those documents are the official source of truth for gameplay, content, progression, UI flow, learning goals, and conceptual data models.

Start with:

- [Documentation Index](specs/README.md)
- [Game Design Document](specs/GDD.md)
- [Game Balance Document](specs/GBD.md)
- [Mechanics Specs](specs/mechanics/README.md)
- [Content Specs](specs/content/README.md)
- [Education Specs](specs/education/README.md)
- [UI/UX Specification](specs/ui/README.md)
- [Technical Direction](specs/technical/README.md)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) before proposing gameplay, balance, content, or documentation changes.

## License

Mendel's Greenhouse is licensed under the [MIT License](LICENSE).
