import unittest

from paperbak import utils


class TestUtilsFunctions(unittest.TestCase):

    def test_hex_0(self):
        """Test output of hex(0),"""
        self.assertEqual("0x00", utils.hex(0))

    def test_hex_15(self):
        """Test output of hex(15),"""
        self.assertEqual("0x0f", utils.hex(15))

    def test_hex_255(self):
        """Test output of hex(255),"""
        self.assertEqual("0xff", utils.hex(255))

if __name__ == '__main__':
    unittest.main()
