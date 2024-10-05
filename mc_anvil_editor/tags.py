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
            Other descriptors that must be stripped:
            - Payload type byte (TAG_List)
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
        super().__init__(None, None)

class TAG_Byte(TAG):
    '''A single raw byte of data.
    Represents a signed integer or a boolean.
    '''
    TAG_ID = 1
    def __init__(self, name: bytes, payload: bytes):
        assert len(payload) == 1, f'Incorrect number of bytes found in the payload of a TAG_Byte (expected 1): {len(payload)}.'
        super().__init__(name, payload)
        self.value = bytes_to_signed_int(payload)

class TAG_Short(TAG):
    '''Two big-endian bytes of data.
    Represents a signed integer.
    '''
    TAG_ID = 2
    def __init__(self, name: bytes, payload: bytes):
        assert len(payload) == 2, f'Incorrect number of bytes found in the payload of a TAG_Short (expected 2): {len(payload)}.'
        super().__init__(name, payload)
        self.value = bytes_to_signed_int(payload)

class TAG_Int(TAG):
    '''Four big-endian bytes of data.
    Represents a signed integer.
    '''
    TAG_ID = 3
    def __init__(self, name: bytes, payload: bytes):
        assert len(payload) == 4, f'Incorrect number of bytes found in the payload of a TAG_Int (expected 4): {len(payload)}.'
        super().__init__(name, payload)
        self.value = bytes_to_signed_int(payload)

class TAG_Long(TAG):
    '''Eight big-endian bytes of data.
    Represents a signed integer.
    '''
    TAG_ID = 4
    def __init__(self, name: bytes, payload: bytes):
        assert len(payload) == 8, f'Incorrect number of bytes found in the payload of a TAG_Long (expected 8): {len(payload)}.'
        super().__init__(name, payload)
        self.value = bytes_to_signed_int(payload)

class TAG_Float(TAG):
    '''A signed big-endian single-precision IEEE 754 floating point number.'''
    TAG_ID = 5
    def __init__(self, name: bytes, payload: bytes):
        assert len(payload) == 4, f'Incorrect number of bytes found in the payload of a TAG_Float (expected 4): {len(payload)}'
        super().__init__(name, payload)
        self.value = struct.unpack('f', payload)

class TAG_Double(TAG):
    '''A signed big-endian double-precision IEEE 754 floating point number.'''
    TAG_ID = 6
    def __init__(self, name: bytes, payload: bytes):
        assert len(payload) == 8, f'Incorrect number of bytes found in the payload of a TAG_Double (expected 8): {len(payload)}'
        super().__init__(name, payload)
        self.value = struct.unpack('f', payload)

class TAG_Byte_Array(TAG):
    '''An array of signed bytes.'''
    TAG_ID = 7
    def __init__(self, name: bytes, payload: bytes):
        super().__init__(name, payload)
        self.value = bytearray(payload)

class TAG_String(TAG):
    '''A UTF-8, NON-null-terminated string.'''
    TAG_ID = 8
    def __init__(self, name: bytes, payload: bytes):
        super().__init__(name, payload)
        self.value = str(payload, 'utf-8')

class TAG_List(TAG):
    '''A list of nameless values of the same type.
    
    Attributes
    ----------
    list_type : int
        TAG ID denoting the type of TAGs included in this List.
    '''
    TAG_ID = 9
    def __init__(self, name: bytes, payload: bytes, list_type: int):
        '''
        Arguments
        ---------
        list_type : int
            TAG ID denoting the type of TAGs included in this List.
        
        Raises
        ------
        ValueError
            if `list_type` is less than 0 or greater than 12.
            Such ID does not correspond to a valid TAG type.
        AssertionError
            if `payload` contains an incorrect number of bytes considering the payload type.
            For example, if the payload has an odd number of bytes when the type is Short.
        '''
        if list_type < 0 or list_type > 12 or list_type is None:
            raise ValueError(f'Invalid type for TAG_List: {list_type}')
        super().__init__(name, payload)

        self.list_type = list_type
        
        # Parse the payload
        # (Even though it'd be more elegant to dispatch this task to each TAG subclass,
        # it clutters code structure so I will not do that.)
        _value = []
        if list_type == TAG_End.TAG_ID:
            pass
        elif list_type == TAG_Byte.TAG_ID:
            for byte in payload:
                _child_TAG_Byte = TAG_Byte(None, byte)
                _value.append(_child_TAG_Byte)
        elif list_type == TAG_Short.TAG_ID:
            assert len(payload) % 2 == 0, f'Excessive or incomplete List payload: Expected a multiple of 2 bytes (short), found {len(payload)}.'
            for i in range(0, len(payload), 2):
                _child_TAG_Short = TAG_Short(None, payload[i:i+2])
                _value.append(_child_TAG_Short)
        elif list_type == TAG_Int.TAG_ID:
            assert len(payload) % 4 == 0, f'Excessive or incomplete List payload: Expected a multiple of 4 bytes (int), found {len(payload)}.'
            for i in range(0, len(payload), 4):
                _child_TAG_Int = TAG_Int(None, payload[i:i+4])
                _value.append(_child_TAG_Int)
        elif list_type == TAG_Long.TAG_ID:
            assert len(payload) % 8 == 0, f'Excessive or incomplete List payload: Expected a multiple of 8 bytes (long), found {len(payload)}.'
            for i in range(0, len(payload), 8):
                _child_TAG_Long = TAG_Long(None, payload[i:i+8])
                _value.append(_child_TAG_Long)
        elif list_type == TAG_Float.TAG_ID:
            assert len(payload) % 4 == 0, f'Excessive or incomplete List payload: Expected a multiple of 4 bytes (float), found {len(payload)}.'
            for i in range(0, len(payload), 4):
                _child_TAG_Float = TAG_Float(None, payload[i:i+4])
                _value.append(_child_TAG_Float)
        elif list_type == TAG_Double.TAG_ID:
            assert len(payload) % 8 == 0, f'Excessive or incomplete List payload: Expected a multiple of 8 bytes (double), found {len(payload)}.'
            for i in range(0, len(payload), 8):
                _child_TAG_Double = TAG_Double(None, payload[i:i+8])
                _value.append(_child_TAG_Double)
        elif list_type == TAG_Byte_Array.TAG_ID:
            _list_payload_stream = BytesIO(payload)
            while _list_payload_stream.tell() <= len(payload):
                _byte_array_length = _list_payload_stream.read(4)
                _byte_array_length = bytes_to_signed_int(_byte_array_length)
                _byte_array_payload = _list_payload_stream.read(_byte_array_length)
                _child_TAG_Byte_Array = TAG_Byte_Array(None, _byte_array_payload)
                _value.append(_child_TAG_Byte_Array)
        elif list_type == TAG_String.TAG_ID:
            _list_payload_stream = BytesIO(payload)
            while _list_payload_stream.tell() <= len(payload):
                _string_length = _list_payload_stream.read(2)
                _string_length = bytes_to_int(_string_length)
                _string_payload = _list_payload_stream.read(_string_length)
                _child_TAG_String = TAG_String(None, _string_payload)
                _value.append(_child_TAG_String)
        elif list_type == TAG_List.TAG_ID:  # oh god
            _list_payload_stream = BytesIO(payload)
            while _list_payload_stream.tell() <= len(payload):
                _list_type = _list_payload_stream.read(1)
                _list_type = bytes_to_int(_list_type)
                _list_length = _list_payload_stream.read(4)
                _list_length = bytes_to_signed_int(_list_length)
                _list_payload = _list_payload_stream.read(_list_length)
                _child_TAG_List = TAG_List(None, )