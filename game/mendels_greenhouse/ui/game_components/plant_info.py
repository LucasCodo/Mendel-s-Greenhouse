"""Plant information formatting helpers."""

from collections.abc import Callable

from mendels_greenhouse.core.genetics import Plant


def localized_trait_name(name: str, translate: Callable[[str], str]) -> str:
    """Return a localized trait label with sentence-style capitalization."""
    translated = translate(name)
    if not translated:
        return translated
    return translated[0].upper() + translated[1:]


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
        f"{localized_trait_name(name, translate)}: {translate(value)}"
        for name, value in items
    ]
