# four_color_theorem_graph_coloring

Color a planar graph with at most four colors.

```python
from four_color_theorem_graph_coloring import color_planar_graph

coloring = color_planar_graph(
    nodes=[0, 1, 2, 3],
    edges=[(0, 1), (1, 2), (2, 0), (0, 3)],
)
# {0: 0, 1: 1, 2: 2, 3: 1}  -- node -> color in {0,1,2,3}
```

## Why this exists

The Four Color Theorem guarantees every planar graph can be colored with at most
four colors. This library delivers that guarantee as a single function call for
the kinds of planar graphs that arise in maps, diagrams, and scheduling —
graphs with up to a few thousand nodes.

The linear-time Chiba–Nishizeki algorithm is the canonical reference, but its
core is a PQ-tree data structure whose faithful re-implementation is a project
unto itself. We chose the pragmatic trade: the same public guarantee (a valid
4-coloring or a clear error), delivered by a degree-ordered exhaustive search
with forward pruning. For real-world planar graphs this is fast enough; for
non-planar input it raises `ColorNotProvableError` rather than returning a
broken coloring. No planarity check is performed — that is a separate problem
and the library is honest about not solving it.

## The awkward edge

If you pass a non-planar graph (or one with a self-loop) you get
`ColorNotProvableError`, not a silent wrong answer. The library does not
detect non-planarity; it only reports that it could not color what you gave it.

## Exports

- `color_planar_graph(nodes, edges) -> dict[int, int]` — returns a mapping
  from each node to a color in `{0, 1, 2, 3}` such that no two adjacent nodes
  share a color.
- `ColorNotProvableError` — raised when no 4-coloring exists.

## Running the tests

```
PYTHONPATH=src python -m unittest discover -s tests
```

## Design notes

The window stores values eagerly rather than keeping running aggregates. Running
sums drift with floating point over long streams, and recomputing from a small
buffer is cheap enough that the drift is not worth the speed.

