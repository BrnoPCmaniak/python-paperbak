import unittest

from paperbak.structures import Data

from . import TEST_DATA


class TestData(unittest.TestCase):

    def setUp(self):
        self.data = Data()
        self.data.address = 15
        self.data.data = bytes(TEST_DATA)
        self.data2 = Data()
        self.data2.address = 15
        self.data2.data = TEST_DATA

    def test_tobytes(self):
        """Test that tobytes matches to new_cpp/test_t_data_crc_ecc.cpp."""
        data = [
            0x0f, 0x00, 0x00, 0x00, 0xae, 0x6f, 0x2c, 0xea, 0xc0, 0xab, 0x94, 0x06, 0x62, 0x0b,
            0xf7, 0xe9, 0xe8, 0x34, 0xf5, 0xee, 0x73, 0xfc, 0x32, 0x96, 0xba, 0xa3, 0xcc, 0x4b,
            0x59, 0xf2, 0x7c, 0x4f, 0x77, 0xaf, 0x09, 0x74, 0xc6, 0xd3, 0xab, 0x2f, 0xad, 0x4e,
            0x96, 0xa5, 0x5f, 0xe5, 0x9d, 0x4b, 0x39, 0x6a, 0x63, 0x1a, 0x29, 0x49, 0x1e, 0xdf,
            0x85, 0x36, 0x58, 0x74, 0xde, 0x78, 0x86, 0xfd, 0xea, 0xbd, 0x11, 0x22, 0x54, 0x05,
            0x05, 0x03, 0x58, 0x14, 0x09, 0x00, 0xdd, 0xa2, 0xc8, 0x84, 0x96, 0x8e, 0xea, 0xb2,
            0x59, 0xb5, 0xb7, 0xfc, 0x3e, 0xe1, 0x18, 0x2c, 0x3b, 0x48,
        ]
        self.assertEqual(self.data.tobytes(False, False), bytes(data))

    def test_calc_crc(self):
        """Test that CRC16 matches to new_cpp/test_t_data_crc_ecc.cpp."""
        self.data.calc_crc()
        self.assertEqual(self.data.crc, 31055)

    def test_calc_ecc_assert(self):
        """Test that calc_ecc raises AssertionError if ecc is empty."""
        self.assertRaises(AssertionError, self.data.calc_ecc)

    def test_calc_ecc(self):
        """Test that ECC matches to new_cpp/test_t_data_crc_ecc.cpp."""
        data = [
            0x74, 0x8d, 0xe3, 0xa0, 0x30, 0x5d, 0x76, 0x59, 0xcf, 0x3f, 0x3d, 0xf2, 0x78, 0x11,
            0x4b, 0xe1, 0x64, 0x56, 0x98, 0xd7, 0xbc, 0x98, 0xa0, 0xd9, 0xe6, 0x17, 0xd7, 0x40,
            0x29, 0x1c, 0x3e, 0x53,
        ]
        self.data.calc_crc()
        self.data.calc_ecc()
        self.assertEqual(self.data.ecc, bytes(data))

    def test_tobytes_len(self):
        """Test that tobytes have correct len."""
        self.assertEqual(len(self.data.tobytes(True, True)), 128)

    def test__eq__self(self):
        """Test that object equals to itself."""
        self.assertEqual(self.data, self.data)

    def test__eq__(self):
        """Test that two objects equals."""
        self.assertEqual(self.data, self.data2)

    def test__eq__empty(self):
        """Test that two empty objects equals."""
        self.assertEqual(Data(), Data())

    def test__eq__address(self):
        """Test that two objects with different address doesn't equal."""
        self.data2.address = 1
        self.assertNotEqual(self.data, self.data2)

    def test__eq__data(self):
        """Test that two objects with different data doesn't equal."""
        self.data2.data = None
        self.assertNotEqual(self.data, self.data2)

    def test__eq__crc(self):
        """Test that two objects with different crc doesn't equal."""
        self.data2.calc_crc()
        self.assertNotEqual(self.data, self.data2)

    def test__eq__ecc(self):
        """Test that two objects with different crc doesn't equal."""
        self.data2.calc_crc()
        self.data2.calc_ecc()
        self.data2.crc = self.data.crc
        self.assertNotEqual(self.data, self.data2)

    def test_from_bytes(self):
        """Test that we can recontstruct address back from bytes."""
        # We have to calculate crc and ecc beacause otherwise ecc and crc would be converted
        # from None to 0
        self.data.calc_crc()
        self.data.calc_ecc()
        self.assertEqual(self.data, Data.frombytes(self.data.tobytes()))
