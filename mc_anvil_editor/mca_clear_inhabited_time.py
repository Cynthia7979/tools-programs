'''
Based on https://minecraft.wiki/w/Region_file_format
'''
import os
import sys
import zlib
import gzip
import time
import math
from io import BytesIO
from tqdm import tqdm

SECTOR_SIZE = 0x1000  # Size of a sector in bytes
CHUNK_COMPRESSION_TYPES = {
    1: 'gzip',
    2: 'zlib',
    3: 'uncompressed',
    4: 'lz4',
    127: 'custom'
}

class LocationEntry:
    def __init__(self, offset: int, sector_count: int):
        self.offset = offset
        self.sector_count = sector_count
    
    def __repr__(self):
        return f'({self.offset}, {self.sector_count})'

def bytes_to_int(n: bytes, byteorder='big'):
    return int.from_bytes(n, byteorder)

def main():
    file_path = 'D:/UserDocuments/temp/Drehmal v2.2.1 APOTHEOSIS 1.20/region/r.-1.3.mca'
    with open(file_path, 'rb') as f:
        region_file_size = os.stat(file_path).st_size
        # Parse the header of region file
        # 0x1000 bytes of chunk locations (AKA offsets)
        _locations_header = f.read(0x1000)
        locations = []
        for i in range(0, 0x1000, 4):
            # Each entry has 4 bytes: 3 bytes of offset and 1 byte sector count.
            # Offset is counted beginning at the very start of the file (right before the headers);
            # The first chunk data should start at sector 2 (right after the headers).
            # Each sector is 0x1000 (4096 or 4 KiB) in size.
            location_entry = _locations_header[i : i+4]
            offset = location_entry[:3]
            sector_count = location_entry[3]
            offset, sector_count = bytes_to_int(offset), sector_count  # `sector_count` is int
            locations.append(LocationEntry(offset, sector_count))
        # 0x1000 bytes of timestamps (time of last modification)
        _timestamps_header = f.read(0x1000)
        timestamps = []
        for i in range(0, 0x1000, 4):
            timestamps.append(bytes_to_int(_timestamps_header[i : i+4]))
        # The rest is chunks
        chunks = []
        while f.tell() <= region_file_size:
            # Load the next chunk
            # First thing in chunk is 4 bytes of chunk length, in bytes
            chunk_length = f.read(4)
            chunk_length = bytes_to_int(chunk_length)
            # Next byte denotes compression type
            _compression_type_index = f.read(1)
            _compression_type_index = bytes_to_int(_compression_type_index)
            compression_type = CHUNK_COMPRESSION_TYPES[_compression_type_index]
            if compression_type == 'custom':
                raise NotImplementedError('Custom chunk compression is not implemented.')
            elif compression_type == 'lz4':
                raise NotImplementedError('LZ4 chunk compression is not implemented.')
            elif compression_type == 'uncompressed':
                raise NotImplementedError('Uncompressed chunk format is not implemented (but it should be).')
            elif compression_type == 'gzip':
                raise NotImplementedError('GZip chunk compression is not implemented. It is unused in practice so there could be something wrong with the .mca file.')
            # `chunk_length-1` bytes of compressed chunk data follows
            _compressed_chunk_data = f.read(chunk_length-1)
            if compression_type == 'zlib':
                _decompressed_chunk_data = zlib.decompress(_compressed_chunk_data)
                chunk_bytes_stream = BytesIO(_decompressed_chunk_data)
                chunk_bytes_length = len(_decompressed_chunk_data)
            # Parse chunk NBT data
            tags = []
            while chunk_bytes_stream.tell() <= chunk_bytes_length:
                next_chunk_type = chunk_bytes_stream.read(1)
                
    print('I made it to the end!')

if __name__ == '__main__':
    main()