import unittest

import numpy as np

from paperbak.type_checking import auto_attr_check

class TestAutoAttrCheckDecorator(unittest.TestCase):
    def setUp(self):
        @auto_attr_check
        class Test(object):
            params = {
                "type_1": (np.uint32, 0),
                "type_1_def": (np.uint32, 0),
                "type_2": (bool, False, False),  # None won't be valid value
                "type_2_ex2": (bool, False, True),  # None will be valid value
                "type_2_def": (bool, False, False),
                "type_3": False, # Read only with default None
                "type_3_def": False, # Read only
                "type_4": (False, 42),  # Read only with default 42
                "type_4_def": (False, 21),
                "type_5": np.uint8,  # Default will be None
                "type_5_def": bool,
            }
            type_1_def = 2
            type_2_def = True
            type_3_def = 0x55555555  # set default for type_3
            type_4_def = False  # set default for type_3
            type_5_def = False  # set default for type_5_def

        self.cls_inst = Test()

    # TYPE_1
    def test_type_1_default(self):
        """Test that type_1 have correct default."""
        self.assertEqual(self.cls_inst.type_1, 0)

    def test_type_1_def(self):
        """Test that type_1 get default from attribute."""
        self.assertEqual(self.cls_inst.type_1_def, 2)

    def test_type_1_default_type(self):
        """Test that type_1 default type is not changed."""
        self.assertEqual(type(self.cls_inst.type_1), int)

    def test_type_1_None(self):
        """Test that type_1 can be None."""
        self.cls_inst.type_1 = None
        self.assertEqual(self.cls_inst.type_1, None)

    def test_type_1_type(self):
        """Test that type_1 don't change it's type."""
        self.cls_inst.type_1 = np.uint32(64)
        self.assertEqual(self.cls_inst.type_1, np.uint32(64))
        self.assertEqual(type(self.cls_inst.type_1), np.uint32)

    def test_type_1_re_type(self):
        """Test that type_1 change type as needed."""
        self.cls_inst.type_1 = 15
        self.assertEqual(self.cls_inst.type_1, np.uint32(15))
        self.assertEqual(type(self.cls_inst.type_1), np.uint32)

    # TYPE_2
    def test_type_2_default(self):
        """Test that type_2 have correct default."""
        self.assertEqual(self.cls_inst.type_2, False)

    def test_type_2_def(self):
        """Test that type_2 get default from attribute."""
        self.assertEqual(self.cls_inst.type_2_def, True)

    def test_type_2_default_type(self):
        """Test that type_2 default type is not changed."""
        self.assertEqual(type(self.cls_inst.type_2), bool)

    def test_type_2_None(self):
        """Test that type_2 can't be None."""
        with self.assertRaises(ValueError):
            self.cls_inst.type_2 = None
        # The value is still the same
        self.assertEqual(self.cls_inst.type_2, False)

    def test_type_2_ex2_None(self):
        """Test that type_2_ex2 can be None."""
        self.cls_inst.type_2_ex2 = None
        self.assertEqual(self.cls_inst.type_2_ex2, None)

    def test_type_2_type(self):
        """Test that type_2 don't change it's type."""
        self.cls_inst.type_2 = True
        self.assertEqual(self.cls_inst.type_2, True)
        self.assertEqual(type(self.cls_inst.type_2), bool)

    def test_type_2_re_type(self):
        """Test that type_2 change type as needed."""
        self.cls_inst.type_2 = 1
        self.assertEqual(self.cls_inst.type_2, bool(1))
        self.assertEqual(type(self.cls_inst.type_2), bool)

    # TYPE 3
    def test_type_3_default(self):
        """Test that type_3 have correct default."""
        self.assertEqual(self.cls_inst.type_3, None)

    def test_type_3_read_only(self):
        """Test that type_3 is read only."""
        with self.assertRaises(TypeError):
            self.cls_inst.type_3 = 1
        self.assertEqual(self.cls_inst.type_3, None)

    @unittest.skip("__type_3 can't be find on Test object under unittest.")
    def test_type_3_set(self):
        """Test that type_3 can be set via __type_3"""
        self.cls_inst.__type_3 = 1
        self.assertEqual(self.cls_inst.type_3, 1)

    def test_type_3_def(self):
        """Test that type_3 get default from attribute."""
        self.assertEqual(self.cls_inst.type_3_def, 0x55555555)

    # TYPE 4
    def test_type_4_default(self):
        """Test that type_4 have correct default."""
        self.assertEqual(self.cls_inst.type_4, 42)

    def test_type_4_read_only(self):
        """Test that type_4 is read only."""
        with self.assertRaises(TypeError):
            self.cls_inst.type_4 = 1
        self.assertEqual(self.cls_inst.type_4, 42)

    @unittest.skip("__type_4 can't be find on Test object under unittest.")
    def test_type_4_set(self):
        """Test that type_4 can be set via __type_4"""
        self.cls_inst.__type_4 = 1
        self.assertEqual(self.cls_inst.type_4, 1)

    def test_type_4_def(self):
        """Test that type_4 get default from attribute."""
        self.assertEqual(self.cls_inst.type_4_def, False)

    # TYPE 5
    def test_type_5_default(self):
        """Test that type_5 have correct default."""
        self.assertEqual(self.cls_inst.type_5, None)

    def test_type_5_def(self):
        """Test that type_5 get default from attribute."""
        self.assertEqual(self.cls_inst.type_5_def, False)

    def test_type_5_None(self):
        """Test that type_5 can be set to None."""
        self.cls_inst.type_5 = None
        self.assertEqual(self.cls_inst.type_5, None)

    def test_type_5_type(self):
        """Test that type_5 don't change it's type."""
        self.cls_inst.type_5 = np.uint8(64)
        self.assertEqual(self.cls_inst.type_5, np.uint8(64))
        self.assertEqual(type(self.cls_inst.type_5), np.uint8)

    def test_type_5_re_type(self):
        """Test that type_5 change type as needed."""
        self.cls_inst.type_5 = 15
        self.assertEqual(self.cls_inst.type_5, np.uint8(15))
        self.assertEqual(type(self.cls_inst.type_5), np.uint8)

    def test_wrong_params_tupple(self):
        """Test that AttributeError is raised with incorrect params dictionary."""
        class TestWrongParams(object):
            params = {
                "correct": np.uint8,
                "incorrect": (1,2,3,4)
            }

        with self.assertRaises(AttributeError):
            auto_attr_check(TestWrongParams)

    def test_wrong_params(self):
        """Test that AttributeError is raised with incorrect params dictionary."""
        class TestWrongParams(object):
            params = {
                "correct": np.uint8,
                "incorrect": 1
            }

        with self.assertRaises(AttributeError):
            auto_attr_check(TestWrongParams)

    def test_missing_params(self):
        """Test that AttributeError is raised when params dictionary is not present."""
        class TestMissingParams(object):
            something = 5
        with self.assertRaises(AttributeError):
            auto_attr_check(TestMissingParams)
