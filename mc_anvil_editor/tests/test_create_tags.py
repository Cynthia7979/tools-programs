import unittest
import tags

class TestCreateTags(unittest.TestCase):
    def test_create_TAG_Byte(self):
        result = tags.TAG_Byte(b'byte1', b'\x42')
        self.assertEqual(result.name, b'byte1')
        self.assertNotEqual(result.name, 'byte1')
        self.assertEqual(result.payload, b'\x42')
        self.assertEqual(result.value, 0x42)
    
    def test_create_neg_TAG_Byte(self):
        result = tags.TAG_Byte(b'byte1', b'\xff')
        self.assertEqual(result.value, -1)
    
    def test_bad_create_TAG_Byte(self):
        with self.assertRaises(AssertionError):
            result = tags.TAG_Byte(b'byte1', b'\x00\x42')
    
    def test_create_TAG_Short(self):
        result = tags.TAG_Short(b'short1', b'\x00\x42')
        self.assertEqual(result.name, b'short1')
        self.assertNotEqual(result.name, 'short1')
        self.assertEqual(result.payload, b'\x00\x42')
        self.assertEqual(result.value, 0x42)
    
    def test_create_neg_TAG_Short(self):
        result = tags.TAG_Short(b'short1', b'\xff\xff')
        self.assertEqual(result.value, -1)
    
    # TODO hands hurty