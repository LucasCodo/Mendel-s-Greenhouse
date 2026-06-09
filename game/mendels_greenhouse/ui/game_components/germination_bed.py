"""Germination Bed geometry helpers."""

from dataclasses import dataclass
from math import ceil, sqrt

from mendels_greenhouse.ui.components import Rect


@dataclass(frozen=True)
class BedGeometry:
    """Static Germination Bed sizing inputs."""

    origin_x: int
    origin_y: int
    max_columns: int
    cell_width: int
    cell_height: int
    gap: int


@dataclass(frozen=True)
class BedLayout:
    """Computed Germination Bed geometry for the current batch."""

    x: int
    y: int
    columns: int
    rows: int
    cell_count: int
    cell_width: int
    cell_height: int
    gap: int

    @property
    def width(self) -> int:
        """Return the pixel width occupied by cells."""
        return self.columns * self.cell_width + (self.columns - 1) * self.gap

    @property
    def height(self) -> int:
        """Return the pixel height occupied by cells."""
        return self.rows * self.cell_height + (self.rows - 1) * self.gap


def germination_layout(
    *,
    batch_size: int,
    fallback_cells: int,
    geometry: BedGeometry,
) -> BedLayout:
    """Return a readable grid layout for a generated batch."""
    cell_count = max(batch_size, fallback_cells)
    columns = min(max(ceil(sqrt(cell_count)), 1), geometry.max_columns)
    rows = ceil(cell_count / columns)
    width = columns * geometry.cell_width + (columns - 1) * geometry.gap
    return BedLayout(
        x=geometry.origin_x - width // 2,
        y=geometry.origin_y,
        columns=columns,
        rows=rows,
        cell_count=cell_count,
        cell_width=geometry.cell_width,
        cell_height=geometry.cell_height,
        gap=geometry.gap,
    )


def germination_cell_rect(index: int, layout: BedLayout) -> Rect:
    """Return a bed-cell rectangle."""
    col = index % layout.columns
    row = index // layout.columns
    return Rect(
        layout.x + col * (layout.cell_width + layout.gap),
        layout.y + row * (layout.cell_height + layout.gap),
        layout.cell_width,
        layout.cell_height,
    )
