def bytes_to_int(n: bytes, byteorder='big'):
    '''Converts the *big-endian*, *unsigned* bytes `n` into an integer.'''
    return int.from_bytes(n, byteorder)

def bytes_to_signed_int(n: bytes, byteorder='big'):
    '''Converts the *big-endian*, *signed* bytes `n` into an integer.'''
    return int.from_bytes(n, byteorder, signed=True)
