import unittest
from datetime import datetime

import numpy as np

from paperbak.structures import Data, SuperData

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

    def test_tobytes_len(self):
        """Test that tobytes have correct len."""
        self.assertEqual(len(self.data.tobytes(True, True)), 128)

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
        self.data.crc = self.data2.crc
        self.assertNotEqual(self.data, self.data2)

    def test_from_bytes(self):
        """Test that we can recontstruct block back from bytes."""
        # We have to calculate crc and ecc beacause otherwise ecc and crc would be converted
        # from None to 0
        self.data.calc_crc()
        self.data.calc_ecc()
        self.assertEqual(self.data, Data.frombytes(self.data.tobytes()))


class TestSuperData(unittest.TestCase):

    def setUp(self):
        self.superdata = SuperData()
        self.superdata.datasize = 90
        self.superdata.pagesize = 1
        self.superdata.origsize = 90
        self.superdata.pbm_compressed = True
        self.superdata.page = 1
        self.superdata.modified = datetime.fromtimestamp(1483228800)
        self.superdata.filecrc = 31055
        self.superdata.name = "README.txt"

        self.superdata2 = SuperData()
        self.superdata2.datasize = 90
        self.superdata2.pagesize = 1
        self.superdata2.origsize = 90
        self.superdata2.pbm_compressed = True
        self.superdata2.page = 1
        self.superdata2.modified = datetime.fromtimestamp(1483228800)
        self.superdata2.filecrc = 31055
        self.superdata2.name = "README.txt"

    def test_mode_0(self):
        """Test that mode property returns 0 when all pbm_* are off."""
        superdata = SuperData()
        self.assertEqual(superdata.mode, 0)
        self.assertEqual(type(superdata.mode), np.uint8)

    def test_mode_compress(self):
        """Test that if pbm_compressed is True mode is 1."""
        superdata = SuperData()
        superdata.pbm_compressed = True
        self.assertEqual(superdata.mode, 1)
        self.assertEqual(type(superdata.mode), np.uint8)

    def test_mode_encrypted(self):
        """Test that if pbm_encrypted is True mode is 2."""
        superdata = SuperData()
        superdata.pbm_encrypted = True
        self.assertEqual(superdata.mode, 2)
        self.assertEqual(type(superdata.mode), np.uint8)

    def test_mode_compress_encrypted(self):
        """Test that if pbm_encrypted and pbm_compressed is True mode is 2."""
        superdata = SuperData()
        superdata.pbm_compressed = True
        superdata.pbm_encrypted = True
        self.assertEqual(superdata.mode, 3)
        self.assertEqual(type(superdata.mode), np.uint8)

    def test_tobytes(self):
        """Test that tobytes matches to new_cpp/test_t_superdata_crc_ecc.cpp."""
        data = [
            0xff, 0xff, 0xff, 0xff, 0x5a, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x5a, 0x00,
            0x00, 0x00, 0x01, 0x80, 0x01, 0x00, 0x00, 0xc0, 0xb0, 0xfe, 0xc1, 0x63, 0xd2, 0x01,
            0x4f, 0x79, 0x52, 0x45, 0x41, 0x44, 0x4d, 0x45, 0x2e, 0x74, 0x78, 0x74, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        ]
        self.assertEqual(self.superdata.tobytes(False, False), bytes(data))

    def test_tobytes_len(self):
        """Test that tobytes have correct len."""
        self.assertEqual(len(self.superdata.tobytes(True, True)), 128)

    def test_calc_crc(self):
        """Test that CRC16 matches to new_cpp/test_t_superdata_crc_ecc.cpp."""
        self.superdata.calc_crc()
        self.assertEqual(self.superdata.crc, 9130)

    def test_calc_ecc_assert(self):
        """Test that calc_ecc raises AssertionError if ecc is empty."""
        self.assertRaises(AssertionError, self.superdata.calc_ecc)

    def test_calc_ecc(self):
        """Test that ECC matches to new_cpp/test_t_superdata_crc_ecc.cpp."""
        data = [
            0x9a, 0xfa, 0x40, 0x43, 0xbc, 0x54, 0x1c, 0x22, 0xab, 0x38, 0x80, 0x1a, 0x66, 0x1c,
            0x26, 0xfa, 0x6b, 0x8d, 0xfc, 0x36, 0x6f, 0x46, 0x51, 0x04, 0xd9, 0x87, 0x82, 0xc2,
            0x77, 0x3c, 0xfd, 0xd8,

        ]
        self.superdata.calc_crc()
        self.superdata.calc_ecc()
        self.assertEqual(self.superdata.ecc, bytes(data))

    def test__eq__self(self):
        """Test that object equals to itself."""
        self.assertEqual(self.superdata, self.superdata)

    def test__eq__(self):
        """Test that two objects equals."""
        self.assertEqual(self.superdata, self.superdata2)

    def test__eq__empty(self):
        """Test that two empty objects equals."""
        self.assertEqual(SuperData(), SuperData())

    def test__eq__datasize(self):
        """Test that two objects with different datasize doesn't equal."""
        self.superdata2.datasize = None
        self.assertNotEqual(self.superdata, self.superdata2)

    def test__eq__pagesize(self):
        """Test that two objects with different pagesize doesn't equal."""
        self.superdata2.pagesize = None
        self.assertNotEqual(self.superdata, self.superdata2)

    def test__eq__origsize(self):
        """Test that two objects with different origsize doesn't equal."""
        self.superdata2.origsize = None
        self.assertNotEqual(self.superdata, self.superdata2)

    def test__eq__pbm_compressed(self):
        """Test that two objects with different pbm_compressed doesn't equal."""
        self.superdata2.pbm_compressed = False
        self.assertNotEqual(self.superdata, self.superdata2)

    def test__eq__pbm_encrypted(self):
        """Test that two objects with different pbm_encrypted doesn't equal."""
        self.superdata.pbm_encrypted = True
        self.assertNotEqual(self.superdata, self.superdata2)

    def test__eq__attributes(self):
        """Test that two objects with different attributes doesn't equal."""
        self.superdata2.attributes = None
        self.assertNotEqual(self.superdata, self.superdata2)

    def test__eq__page(self):
        """Test that two objects with different page doesn't equal."""
        self.superdata2.page = None
        self.assertNotEqual(self.superdata, self.superdata2)

    def test__eq__modified(self):
        """Test that two objects with different modified doesn't equal."""
        self.superdata2.modified = datetime.fromtimestamp(0)
        self.assertNotEqual(self.superdata, self.superdata2)

    def test__eq__filecrc(self):
        """Test that two objects with different filecrc doesn't equal."""
        self.superdata2.filecrc = None
        self.assertNotEqual(self.superdata, self.superdata2)

    def test__eq__name(self):
        """Test that two objects with different name doesn't equal."""
        self.superdata2.name = None
        self.assertNotEqual(self.superdata, self.superdata2)

    def test__eq__crc(self):
        """Test that two objects with different crc doesn't equal."""
        self.superdata2.calc_crc()
        self.assertNotEqual(self.superdata, self.superdata2)

    def test__eq__ecc(self):
        """Test that two objects with different crc doesn't equal."""
        self.superdata2.calc_crc()
        self.superdata2.calc_ecc()
        self.superdata.crc = self.superdata2.crc
        self.assertNotEqual(self.superdata, self.superdata2)

    def test_from_bytes(self):
        """Test that we can recontstruct block back from bytes."""
        # We have to calculate crc and ecc beacause otherwise ecc and crc would be converted
        # from None to 0
        self.superdata.calc_crc()
        self.superdata.calc_ecc()
        self.assertEqual(self.superdata, SuperData.frombytes(self.superdata.tobytes()))
