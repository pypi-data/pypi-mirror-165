import unittest

from elanwrapper.conflicts import ConflictResolver
from elanwrapper.segments import Segment, Timeline, TimelineOverlapError, TimelineDict


class TestSegmentSet(unittest.TestCase):
    def test_segment_intersection(self):
        test_cases = [
            ((Segment(2, 5), Segment(1, 3)), True),
            ((Segment(2, 5), Segment(2, 3)), True),
            ((Segment(2, 5), Segment(4, 6)), True),
            ((Segment(2, 5), Segment(1, 6)), True),
            ((Segment(2, 5), Segment(3, 4)), True),
            ((Segment(2, 5), Segment(6, 7)), False),
            ((Segment(2, 5), Segment(0, 1)), False),
            ((Segment(2, 5), Segment(5, 6)), False),
            ((Segment(2, 5), Segment(5, 5)), False),
            ((Segment(2, 2), Segment(2, 5)), True),
            ((Segment(2, 2), Segment(2, 2)), True),
            ((Segment(2, 5), Segment(2, 5)), True),
        ]
        for (segment_a, segment_b), expect_intersect in test_cases:
            with self.subTest(((segment_a, segment_b), expect_intersect)):
                actual_intersect = segment_a.intersect(segment_b)
                self.assertEqual(actual_intersect, expect_intersect)

    def test_timeline_overlap(self):
        test_cases = [
            ([Segment(2, 5), Segment(1, 3)], Segment(1, 3)),
            ([Segment(2, 5), Segment(2, 3)], Segment(2, 3)),
            ([Segment(2, 5), Segment(4, 6)], Segment(4, 6)),
            ([Segment(2, 5), Segment(1, 6)], Segment(1, 6)),
            ([Segment(2, 5), Segment(3, 4)], Segment(3, 4)),
            ([Segment(2, 5), Segment(5, 6)], None),
            ([Segment(2, 5), Segment(6, 7)], None),
            ([Segment(2, 5), Segment(0, 1)], None),
            ([Segment(2, 5), Segment(0, 2)], None),
        ]
        for segments, expected_raise in test_cases:
            timeline = Timeline()
            with self.subTest((segments, expected_raise)):
                try:
                    for segment in segments:
                        timeline.insert(segment)
                    self.assertIsNone(expected_raise)
                except TimelineOverlapError:
                    self.assertEqual(expected_raise, segment)

    def test_timeline_get(self):
        timeline = Timeline([Segment(-20, -5), Segment(0, 1), Segment(2, 5), Segment(6, 8)])
        test_cases = [
            (Segment(2, 5), [Segment(2, 5)]),
            (2, [Segment(2, 5)]),
            (4.9, [Segment(2, 5)]),
            (5, []),
            (Segment(2, 7), [Segment(2, 5), Segment(6, 8)]),
            (7.9, [Segment(6, 8)]),
            (8, []),
            (-20, [Segment(-20, -5)]),
            (-21, []),
            (-4, []),
            (1.5, []),
            (9, []),
        ]
        for at_time, expect_segment in test_cases:
            with self.subTest((at_time, expect_segment)):
                actual_segment = timeline.get_all(at_time)
                self.assertEqual(tuple(expect_segment), tuple(actual_segment))

    def test_timeline_dict(self):
        timeline_dict = TimelineDict({
            Segment(-20, -5): "a",
            Segment(0, 1): "b",
            Segment(2, 5): "c",
            Segment(6, 8): "d"
        })
        test_cases = [
            (-21, None),
            (-20, "a"),
            (3, "c"),
            (7.9, "d"),
            (8, None),
            (9, None),
        ]

        for at_time, expect_value in test_cases:
            with self.subTest((at_time, expect_value)):
                actual_value = timeline_dict.get(at_time)
                self.assertEqual(expect_value, actual_value)

    def test_conflict_resolver(self):
        class ReplaceResolver(ConflictResolver):
            def resolve(self, inserting, conflicting):
                return [inserting]

        base = TimelineDict({
            Segment(-20, -5): "a",
            Segment(0, 1): "b",
            Segment(2, 5): "c",
            Segment(6, 8): "d"
        })

        test_cases = [
            ({Segment(0, 1): "e"}, ["a", "e", "c", "d"]),
        ]


        for insertions, expected_values in test_cases:
            with self.subTest((insertions, expected_values)):
                timeline_dict = TimelineDict(base, conflict_resolver=ReplaceResolver())
                timeline_dict.update(insertions)
                actual_values = list(timeline_dict.values())
                self.assertEqual(expected_values, actual_values)



if __name__ == '__main__':
    unittest.main()
