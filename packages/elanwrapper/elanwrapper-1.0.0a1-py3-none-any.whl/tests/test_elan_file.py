import os
import tempfile
import unittest

from elanwrapper import ElanFile, ElanSegment


class TestElanFile(unittest.TestCase):
    maxDiff = None

    def test_instantiate(self):
        ela = ElanFile()
        segment = ElanSegment(
            symbol="asdf",
            begin_ms=123456,
            end_ms=789000,
            tier="default"
        )
        ela.add(segment)
        print(ela)

    def test_read_write(self):
        with tempfile.TemporaryDirectory() as d:
            temp_filename = os.path.join(d, f"myfile.eaf")
            eaf = ElanFile()
            eaf.add(ElanSegment(
                symbol="a",
                begin_ms=0,
                end_ms=1000,
                tier="tier-a",
                linguistic_type="ling-type-a",
            ))
            eaf.add(ElanSegment(
                symbol="a",
                begin_ms=0,
                end_ms=1000,
                tier="tier-b",
                ref_tier="tier-a",
                linguistic_type="ling-type-b",
            ))
            eaf.to_elan(temp_filename)

            eaf_reloaded = ElanFile.from_elan(temp_filename)
            with self.subTest("media_descriptors"):
                self.assertEqual(eaf.media_descriptors, eaf_reloaded.media_descriptors)
            with self.subTest("_tier_meta"):
                self.assertEqual(eaf._tier_meta, eaf_reloaded._tier_meta)
            with self.subTest("_linguistic_types"):
                self.assertEqual(eaf._linguistic_types, eaf_reloaded._linguistic_types)


if __name__ == '__main__':
    unittest.main()
