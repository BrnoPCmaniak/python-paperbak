import unittest
from datetime import datetime, timezone

from paperbak.dtypes import FileTime


class TestFileTime(unittest.TestCase):
    def test_new(self):
        """Test that 1/1/1970 equals to FileTime.EPOCH_DIFF*FileTime.N100_NSEC_IN_SEC."""
        self.assertEqual(FileTime(datetime(1970,1,1, tzinfo=timezone.utc)),
                         FileTime.EPOCH_DIFF*FileTime.N100_NSEC_IN_SEC)
    def test_get_datetime(self):
        """Test that FileTime(0) equals to 1/1/1601"""
        self.assertEqual(FileTime(0).get_datetime(), datetime(1601, 1, 1, tzinfo=timezone.utc))

if __name__ == '__main__':
    unittest.main()
