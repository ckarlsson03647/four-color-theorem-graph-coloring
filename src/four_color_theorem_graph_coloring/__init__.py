"""Four Color Theorem graph coloring.

Public API:
    color_planar_graph(nodes, edges) -> dict[int, int]
    ColorNotProvableError
"""

from .core import color_planar_graph, ColorNotProvableError

__all__ = ["color_planar_graph", "ColorNotProvableError"]
