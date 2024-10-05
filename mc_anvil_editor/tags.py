'''tags.py
Defines classes for every TAG as listed in the NBT specifications.
https://wiki.vg/NBT#Specification
'''
import struct
from io import BytesIO
from bytes_conversion import *

class TAG:
    '''Base class for NBT TAGs.

    Attributes
    -----------
    name : bytes
        raw bytes containing the non-null-terminated string identifier for this TAG.
        If a TAG does not have a name because of its type, this attribute should be set to `None`.
    payload : bytes
        raw bytes containing the complete payload data pertaining to this TAG.
        The payload is not mutable. To edit a TAG, access its `value` attribute.
        If a TAG does not have a payload because of its type, this attribute should be set to `None`.
    value : Any
        the TAG's payload represented as Python structures.
    
    Methods
    -------
    TAG.get_TAG_id()
        Returns the TAG ID as defined by Minecraft NBT specifications.
        Raises TypeError if called on this base TAG class.
    '''
    TAG_ID = None
    def __init__(self, name: bytes, payload: bytes):
        f'''Initializes a new {self.__class__.__name__} instance using the given arguments.

        Arguments
        ---------
        name : bytes
            string identifier of the TAG.
            Raw data should be prefixed by a 2 bytes unsigned integer denoting name length.
            Value passed in for this argument must have these 2 bytes stripped.
        payload : bytes
            raw payload of the TAG.
            If TAG has a variable payload length (e.g. List, String, Compound), then
            the payload must have its length bytes stripped before being passed in for this argument.
        '''
        self.name = name
        self.payload = payload
    
    @classmethod
    def get_TAG_id(cls):
        if cls.TAG_ID is None:
            raise TypeError('Cannot retrieve TAG ID because base class is not a real TAG.')

class TAG_End:
    '''Closing TAG for `TAG_Compound`.
    Does not have a name or payload. `self.name` and `self.payload` are `None`.
    '''
    TAG_ID = 0
    def __init__(self):
        super(TAG_End, self).__init__(None, None)

class TAG_Byte(TAG):
    '''A single raw byte of data.
    Represents a signed integer or a boolean.
    '''
    TAG_ID = 1
    def __init__(self, name: bytes, payload: bytes):
        assert len(payload) == 1, f'Incorrect number of bytes found in the payload of a TAG_Byte (expected 1): {len(payload)}.'
        super(TAG_Byte, self).__init__(name, payload)
        self.value = bytes_to_signed_int(payload)

class TAG_Short(TAG):
    '''Two big-endian bytes of data.
    Represents a signed integer.
    '''
    TAG_ID = 2
    def __init__(self, name: bytes, payload: bytes):
        assert len(payload) == 2, f'Incorrect number of bytes found in the payload of a TAG_Short (expected 2): {len(payload)}.'
        super(TAG_Short, self).__init__(name, payload)
        self.value = bytes_to_signed_int(payload)

class TAG_Int(TAG):
    '''Four big-endian bytes of data.
    Represents a signed integer.
    '''
    TAG_ID = 3
    def __init__(self, name: bytes, payload: bytes):
        assert len(payload) == 4, f'Incorrect number of bytes found in the payload of a TAG_Int (expected 4): {len(payload)}.'
        super(TAG_Int, self).__init__(name, payload)
        self.value = bytes_to_signed_int(payload)

class TAG_Long(TAG):
    '''Eight big-endian bytes of data.
    Represents a signed integer.
    '''
    TAG_ID = 4
    def __init__(self, name: bytes, payload: bytes):
        assert len(payload) == 8, f'Incorrect number of bytes found in the payload of a TAG_Long (expected 8): {len(payload)}.'
        super(TAG_Long, self).__init__(name, payload)
        self.value = bytes_to_signed_int(payload)

class TAG_Float(TAG):
    '''A signed big-endian single-precision IEEE 754 floating point number.'''
    TAG_ID = 5
    def __init__(self, name: bytes, payload: bytes):
        assert len(payload) == 4, f'Incorrect number of bytes found in the payload of a TAG_Float (expected 4): {len(payload)}'
        super(TAG_Float, self).__init__(name, payload)
        self.value = struct.unpack('f', payload)

class TAG_Double(TAG):
    '''A signed big-endian double-precision IEEE 754 floating point number.'''
    TAG_ID = 6
    def __init__(self, name: bytes, payload: bytes):
        assert len(payload) == 8, f'Incorrect number of bytes found in the payload of a TAG_Double (expected 8): {len(payload)}'
        super(TAG_Double, self).__init__(name, payload)
        self.value = struct.unpack('f', payload)

class TAG_Byte_Array(TAG):
    '''An array of signed bytes.'''
    TAG_ID = 7
    def __init__(self, name: bytes, payload: bytes):
        # _length, _array = payload[:4], payload[4:]
        # _length = bytes_to_signed_int(_length)
        # assert len(_array) == _length, f'Incomplete or excessive payload found for TAG_Byte_Array. Expected {_length}, found {len(_array)}.'
        super(TAG_Byte_Array, self).__init__(name, payload)
        self.value = bytearray(payload)

class TAG_String(TAG):
    '''A UTF-8, NON-null-terminated string.'''
    TAG_ID = 8
    def __init__(self, name: bytes, payload: bytes):
        super().__init__(name, payload)
        self.value = str(payload, 'utf-8')

