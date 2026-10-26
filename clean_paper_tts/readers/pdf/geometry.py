from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Rect:
    x0: float
    y0: float
    x1: float
    y1: float

    @property
    def w(self) -> float:
        return self.x1 - self.x0

    @property
    def h(self) -> float:
        return self.y1 - self.y0

    @property
    def cx(self) -> float:
        return (self.x0 + self.x1) / 2

    @property
    def cy(self) -> float:
        return (self.y0 + self.y1) / 2

    @property
    def area(self) -> float:
        return max(0.0, self.w) * max(0.0, self.h)

    def union(self, o: Rect) -> Rect:
        return Rect(min(self.x0, o.x0), min(self.y0, o.y0), max(self.x1, o.x1), max(self.y1, o.y1))

    def inter_area(self, o: Rect) -> float:
        w = min(self.x1, o.x1) - max(self.x0, o.x0)
        h = min(self.y1, o.y1) - max(self.y0, o.y0)
        return w * h if w > 0 and h > 0 else 0.0

    def frac_inside(self, o: Rect) -> float:
        """Fraction of self covered by o."""
        return self.inter_area(o) / self.area if self.area > 0 else 0.0

    def expanded(self, d: float) -> Rect:
        return Rect(self.x0 - d, self.y0 - d, self.x1 + d, self.y1 + d)

    def gap_to(self, o: Rect) -> float:
        dx = max(o.x0 - self.x1, self.x0 - o.x1, 0)
        dy = max(o.y0 - self.y1, self.y0 - o.y1, 0)
        return max(dx, dy) if (dx == 0 or dy == 0) else (dx * dx + dy * dy) ** 0.5

    def h_overlap(self, o: Rect) -> float:
        return max(0.0, min(self.x1, o.x1) - max(self.x0, o.x0))

    def tuple(self) -> tuple[float, float, float, float]:
        return (self.x0, self.y0, self.x1, self.y1)


class Orientation:
    """Maps page coordinates to an 'upright' frame where text reads left-to-right, top-to-bottom."""

    def __init__(self, kind: int, width: float, height: float):
        self.kind = kind  # 0 upright, 1 reads bottom-to-top, 2 reads top-to-bottom
        self.W, self.H = width, height

    @property
    def upright_size(self) -> tuple[float, float]:
        return (self.W, self.H) if self.kind == 0 else (self.H, self.W)

    def to_upright(self, r: tuple[float, float, float, float]) -> Rect:
        x0, y0, x1, y1 = r
        if self.kind == 0:
            return Rect(x0, y0, x1, y1)
        if self.kind == 1:  # x' = H - y, y' = x
            return Rect(self.H - y1, x0, self.H - y0, x1)
        return Rect(y0, self.W - x1, y1, self.W - x0)  # x' = y, y' = W - x

    def to_page(self, r: Rect) -> tuple[float, float, float, float]:
        if self.kind == 0:
            return r.tuple()
        if self.kind == 1:
            return (r.y0, self.H - r.x1, r.y1, self.H - r.x0)
        return (self.W - r.y1, r.x0, self.W - r.y0, r.x1)
