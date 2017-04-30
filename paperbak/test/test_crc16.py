import unittest

import numpy as np

from paperbak import crc16

from . import TEST_DATA


class TestCRC16(unittest.TestCase):

    def test(self):
        """Test CRC16 over TEST_DATA matches new_cpp/test_crc16.cpp."""
        self.assertEqual(crc16.crc16(bytes(TEST_DATA)), np.uint16(62557))

    def test_type(self):
        """Test CRC16 return correct data type."""
        self.assertEqual(type(crc16.crc16(bytes(TEST_DATA))), np.uint16)


if __name__ == '__main__':
    unittest.main()
