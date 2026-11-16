import unittest

import numpy as np

from defringe import defringe_rgba, is_purple_hue


class DefringeTests(unittest.TestCase):
    def test_replaces_purple_edge_from_darkest_non_edge_neighbor_without_changing_alpha(self):
        image = np.zeros((5, 5, 4), dtype=np.uint8)
        image[1:4, 1:4] = (190, 80, 70, 255)
        image[1:4, 1] = (240, 0, 240, 255)
        image[2, 2] = (80, 30, 25, 255)

        result, stats = defringe_rgba(image)

        self.assertEqual(tuple(result[2, 1]), (80, 30, 25, 255))
        self.assertTrue(np.array_equal(result[:, :, 3], image[:, :, 3]))
        self.assertEqual(stats["purple_edge_before"], 3)
        self.assertEqual(stats["purple_edge_after"], 0)
        self.assertLessEqual(stats["opaque_color_count_after"], stats["opaque_color_count_before"])

    def test_preserves_purple_edge_when_all_non_edge_neighbors_are_purple(self):
        image = np.zeros((5, 5, 4), dtype=np.uint8)
        image[1:4, 1:4] = (200, 40, 200, 255)

        result, stats = defringe_rgba(image)

        self.assertTrue(np.array_equal(result, image))
        self.assertGreater(stats["purple_edge_before"], 0)
        self.assertEqual(stats["purple_edge_before"], stats["purple_edge_after"])

    def test_purple_hue_filter_uses_requested_hue_and_saturation_range(self):
        self.assertTrue(is_purple_hue((240, 0, 240)))
        self.assertFalse(is_purple_hue((80, 30, 25)))
        self.assertFalse(is_purple_hue((210, 190, 210)))


if __name__ == "__main__":
    unittest.main()
