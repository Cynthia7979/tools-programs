def bytes_to_int(n: bytes, byteorder='big'):
    return int.from_bytes(n, byteorder)

def bytes_to_signed_int(n: bytes, byteorder='big'):
    return int.from_bytes(n, byteorder, signed=True)

def int_to_bytes(n: int, byteorder='big'):
    return int.to_bytes(n, byteorder)