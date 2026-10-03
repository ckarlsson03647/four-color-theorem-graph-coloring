import unittest

from four_color_theorem_graph_coloring import (
    color_planar_graph,
    ColorNotProvableError,
)


class TestColorPlanarGraph(unittest.TestCase):
    """Tests for the public color_planar_graph function.

    We test the behavior the implementation actually claims to support: it
    produces a valid 4-coloring of a planar graph, and raises a clear error
    when it cannot. We do NOT test planarity detection — the library explicitly
    does not do that.
    """

    def _assert_valid_coloring(self, nodes, edges, coloring):
        """Shared validity check: every node colored, colors in range, proper."""
        self.assertEqual(set(coloring.keys()), set(nodes),
                         "every node must be assigned a color")
        for c in coloring.values():
            self.assertIn(c, (0, 1, 2, 3),
                          "color must be one of {0,1,2,3}")
        for u, v in edges:
            self.assertNotEqual(coloring[u], coloring[v],
                                f"adjacent {u!r},{v!r} share color")

    def test_empty_graph(self):
        result = color_planar_graph([], [])
        self.assertEqual(result, {})

    def test_single_node(self):
        result = color_planar_graph([0], [])
        self._assert_valid_coloring([0], [], result)

    def test_two_nodes_one_edge(self):
        result = color_planar_graph([0, 1], [(0, 1)])
        self._assert_valid_coloring([0, 1], [(0, 1)], result)
        self.assertNotEqual(result[0], result[1])

    def test_triangle_needs_three_colors(self):
        nodes = [0, 1, 2]
        edges = [(0, 1), (1, 2), (2, 0)]
        result = color_planar_graph(nodes, edges)
        self._assert_valid_coloring(nodes, edges, result)
        # Triangle requires exactly three distinct colors.
        self.assertEqual(len(set(result.values())), 3)

    def test_complete_graph_k4_needs_four_colors(self):
        # K4 is the largest planar clique and needs all four colors.
        nodes = [0, 1, 2, 3]
        edges = [
            (0, 1), (0, 2), (0, 3),
            (1, 2), (1, 3), (2, 3),
        ]
        result = color_planar_graph(nodes, edges)
        self._assert_valid_coloring(nodes, edges, result)
        self.assertEqual(len(set(result.values())), 4)

    def test_disjoint_components(self):
        # Two separate triangles in one graph; each needs three colors.
        nodes = [0, 1, 2, 10, 11, 12]
        edges = [(0, 1), (1, 2), (2, 0),
                 (10, 11), (11, 12), (12, 10)]
        result = color_planar_graph(nodes, edges)
        self._assert_valid_coloring(nodes, edges, result)

    def test_duplicate_edges_collapsed(self):
        # Duplicate edges should not break the coloring.
        nodes = [0, 1, 2]
        edges = [(0, 1), (0, 1), (1, 2), (1, 2), (2, 0)]
        result = color_planar_graph(nodes, edges)
        self._assert_valid_coloring(nodes, edges, result)

    def test_grid_graph_is_planar(self):
        # A 3x3 grid is planar and easily 4-colorable.
        nodes = [(r * 3 + c) for r in range(3) for c in range(3)]
        edges = []
        for r in range(3):
            for c in range(3):
                n = r * 3 + c
                if c + 1 < 3:
                    edges.append((n, r * 3 + (c + 1)))
                if r + 1 < 3:
                    edges.append((n, (r + 1) * 3 + c))
        result = color_planar_graph(nodes, edges)
        self._assert_valid_coloring(nodes, edges, result)

    def test_self_loop_is_not_colorable(self):
        # A self-loop means a node is adjacent to itself — impossible to color.
        with self.assertRaises(ColorNotProvableError):
            color_planar_graph([0, 1], [(0, 1), (0, 0)])

    def test_k5_is_not_colorable(self):
        # K5 is non-planar and the theorem's guarantee does not apply.
        nodes = [0, 1, 2, 3, 4]
        edges = [(i, j) for i in nodes for j in nodes if i < j]
        with self.assertRaises(ColorNotProvableError):
            color_planar_graph(nodes, edges)

    def test_edge_with_unknown_node_raises_value_error(self):
        with self.assertRaises(ValueError):
            color_planar_graph([0, 1], [(0, 99)])

    def test_coloring_is_deterministic(self):
        # Same input, same output, every time. Degree ordering + id tiebreak
        # guarantees this; we assert it because callers may depend on it.
        nodes = list(range(8))
        edges = [(0, 1), (1, 2), (2, 3), (3, 0),
                 (4, 5), (5, 6), (6, 7), (7, 4),
                 (0, 4), (1, 5), (2, 6), (3, 7)]
        a = color_planar_graph(nodes, edges)
        b = color_planar_graph(nodes, edges)
        self.assertEqual(a, b)

    def test_star_graph_two_colors(self):
        # A star is bipartite: two colors suffice.
        nodes = [0, 1, 2, 3, 4]
        edges = [(0, 1), (0, 2), (0, 3), (0, 4)]
        result = color_planar_graph(nodes, edges)
        self._assert_valid_coloring(nodes, edges, result)
        self.assertEqual(len(set(result.values())), 2)

    def test_non_contiguous_node_ids(self):
        # Node ids need not be 0..n-1.
        nodes = [100, 200, 300, 400]
        edges = [(100, 200), (200, 300), (300, 400), (400, 100),
                 (100, 300)]
        result = color_planar_graph(nodes, edges)
        self._assert_valid_coloring(nodes, edges, result)


if __name__ == "__main__":
    unittest.main()
