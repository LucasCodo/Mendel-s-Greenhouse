"""Plant information formatting helpers."""

from collections.abc import Callable

from mendels_greenhouse.core.genetics import Plant


def plant_trait_lines(
    plant: Plant,
    *,
    translate: Callable[[str], str],
    limit: int | None = None,
) -> list[str]:
    """Return visible trait lines for UI components."""
    items = tuple(plant.phenotype.traits.items())
    if limit is not None:
        items = items[:limit]
    return [
        f"{translate(name.title())}: {translate(value)}"
        for name, value in items
    ]
