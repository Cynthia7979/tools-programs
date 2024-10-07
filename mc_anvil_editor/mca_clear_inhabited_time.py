'''
Based on https://minecraft.wiki/w/Region_file_format
'''
import os
import sys
import zlib
import gzip
import time
import math
import struct
from io import BytesIO
from tqdm import tqdm
import tags
from bytes_conversion import *

SECTOR_SIZE = 0x1000  # Size of a sector in bytes
CHUNK_COMPRESSION_TYPES = {
    1: 'gzip',
    2: 'zlib',
    3: 'uncompressed',
    4: 'lz4',
    127: 'custom'
}

class LocationEntry:
    '''Represents an entry in the locations header of the region file.'''
    def __init__(self, offset: int, sector_count: int):
        self.offset = offset
        self.sector_count = sector_count
    
    def to_bytes(self) -> bytes:
        '''Converts this location entry into a `bytes` object of length 4.
        The first three bytes is the big-endian offset, and the last byte
        is the sector count of the particular chunk that this entry describes.
        '''
        return self.offset.to_bytes(3, 'big') + self.sector_count.to_bytes(1, 'big')

    def __repr__(self):
        return f'({self.offset}, {self.sector_count})'

TAGS_LOOKUP = {cls_.get_TAG_id(): cls_ for cls_ in (
    tags.TAG_Byte,
    tags.TAG_Byte_Array,
    tags.TAG_Double,
    tags.TAG_End,
    tags.TAG_Float,
    tags.TAG_Int,
    tags.TAG_Long,
    tags.TAG_Short
)}

def main():
    file_path = 'D:/UserDocuments/temp/Drehmal v2.2.1 APOTHEOSIS 1.20/region/r.-1.3.mca'
    ## For testing use only not meant for production
    # file_path = 'D:/UserDocuments/temp/r.-1.3.mca'
    out_file = 'D:/UserDocuments/temp/r.-1.3.mca'
    out_data = bytes()
    with open(file_path, 'rb') as f:
        region_file_size = os.stat(file_path).st_size
        # Parse the header of region file
        # 0x1000 bytes of chunk locations (AKA offsets)
        _locations_header = f.read(0x1000)
        out_data += _locations_header
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
        out_data += _timestamps_header
        timestamps = []
        for i in range(0, 0x1000, 4):
            timestamps.append(bytes_to_int(_timestamps_header[i : i+4]))
        # The rest is chunks
        # FIXME: Simply following stream doesn't seem to be working; need to change to location-based reading
        _chunks_count = 0
        while _chunks_count < len(locations) and _chunks_count < 1024:
            # Load the next chunk
            # First thing in chunk is 4 bytes of chunk length, in bytes
            chunk_length = f.read(4)
            chunk_length = bytes_to_signed_int(chunk_length)
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
                ## Just look for what we need and edit it
                _working_chunk_data = bytearray(_decompressed_chunk_data)
                _inti_name_position = _decompressed_chunk_data.find(b'InhabitedTime')
                assert _inti_name_position != -1
                _inti_value_position = _inti_name_position + len(b'InhabitedTime')
                _current_inti = _working_chunk_data[_inti_value_position:_inti_value_position+8]  # Long
                print(bytes_to_signed_int(_current_inti))
                _working_chunk_data[_inti_value_position:_inti_value_position+8] = b'\x00' * 8
                _new_compressed_chunk = zlib.compress(bytes(_working_chunk_data))
                _new_chunk_length = len(_new_compressed_chunk) + 1  ## Our compressed data may be different in size as there is less entropy
                out_data += _new_chunk_length.to_bytes(4, 'big', signed=True)
                out_data += _compression_type_index.to_bytes(1, 'big')
                out_data += _new_compressed_chunk
                # out_data += b'\x00' * (len(_compressed_chunk_data) - len(_new_compressed_chunk))
                # f.read(4096-4-(chunk_length % 4096))
                f.read(4096 - ((4+chunk_length) % 4096))
                out_data += b'\x00' * (4096 - ((4+_new_chunk_length) % 4096))
                # Sometimes an additional 4096 bytes padding is added after some chunks???
                # Will be an issue when reading. Not when writing. I'm having an issue here
                # purely because I don't want to edit the locations table just yet.
                while f.peek()[:2] != b'\x00\x00' or f.peek()[4] not in CHUNK_COMPRESSION_TYPES.keys():
                    # Stopped working on #963???
                    # Why are there 2 4096b paddings?????
                    # WHY ARE YOU DOING THIS MOJANG
                    # now that I think of it it could be garbage data leftover from repeated writing
                    # but still
                    out_data += f.read(4096)
                    print(_chunks_count, file=sys.stderr)
                assert len(out_data) % 4096 == 0
                _chunks_count += 1
                continue

                chunk_bytes_stream = BytesIO(_decompressed_chunk_data)
                chunk_bytes_length = len(_decompressed_chunk_data)
            
            return
            # Parse chunk NBT data
            parsed_tags = []
            while chunk_bytes_stream.tell() <= chunk_bytes_length:
                # A byte begins with 1 byte tag type ID
                _next_tag_id = chunk_bytes_stream.read(1)
                _next_tag_id = bytes_to_int(_next_tag_id)
                next_tag_type = TAGS_LOOKUP[_next_tag_id]
                # If it is TAG_End, then it won't have a name
                # so we leave early
                if next_tag_type == tags.TAG_End:
                    next_tag = tags.TAG_End()
                    parsed_tags.append(next_tag)
                    continue
                # Otherwise it is followed by 2 bytes big-endian name length
                next_tag_name_length = chunk_bytes_stream.read(2)
                next_tag_name_length = bytes_to_int(next_tag_name_length)
                # Then a NON-null-terminated UTF-8 string containing the tag name
                next_tag_name = chunk_bytes_stream.read(next_tag_name_length)
                next_tag_name = str(next_tag_name, 'utf-8')
                # Depending on the TAG type the payload will be different sizes
        out_data += f.read()

    with open(out_file, 'wb') as fo:
        fo.write(bytes(out_data))
                
    print('I made it to the end!')

if __name__ == '__main__':
    main()