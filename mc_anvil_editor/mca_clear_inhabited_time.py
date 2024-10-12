'''
Based on https://minecraft.wiki/w/Region_file_format
'''
import os
import sys
import zlib
import math
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

class ChunkStorage:
    '''Primitive chunk data structure.
    For storing basic chunk information only (see Attributes).
    Should only be used for storing chunk data on file load and save.
    
    Attributes
    ----------
    length : int
        the length, counted in bytes, of compressed chunk data.
    compression_type_index : int
        Integer representing the type of compression this chunk's data uses.
        Should be one of 1 ('gzip'), 2 ('zlib'), 3 ('uncompressed'), 4 ('lz4'), or 127 ('custom')
    compressed_data : bytes
        Compressed chunk data.
    '''
    def __init__(self, length: int=None, compression_type_index: int=None, compressed_data: bytes=None):
        assert length is None or 0 <= length, f'Invalid chunk length: {length}'
        assert compression_type_index is None or compression_type_index in (1, 2, 3, 4, 127), f'Invalid compression type: {compression_type_index}'
        self.length = length
        self.compression_type_index = compression_type_index
        self.compressed_data = compressed_data

    def to_bytes(self) -> bytes:
        '''Converts this chunk storage into a bytes object.
        Returns
        -------
        A bytes object of length 4 + `self.length`.
        Notice that `self.length` must always be 1 longer than `len(self.compressed_data)`.
        '''
        assert self.length == 1 + len(self.compressed_data), f'Mismatch between proclaimed chunk length and actual data length. Expected {self.length}, got {1 + len(self.compressed_data)}.'
        result = bytearray(4 + self.length)
        result[:4] = self.length.to_bytes(4, 'big', signed=False)
        result[4] = self.compression_type_index
        result[5:] = self.compressed_data
        return bytes(result)
    
    def __repr__(self) -> str:
        return f'ChunkStorage(len={self.length}, compression type={CHUNK_COMPRESSION_TYPES[self.compression_type_index]}, {-1 if self.compressed_data is None else len(self.compressed_data)} bytes of compressed data)'


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
    initial_inti = {}
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
        for loc in locations:
            assert isinstance(loc, LocationEntry)  # So that linter could be more helpful
            assert 1 < loc.offset < (region_file_size // SECTOR_SIZE), f'Invalid chunk offset {loc.offset}.'
            # Find the corresponding chunk
            f.seek(SECTOR_SIZE * loc.offset)
            _current_chunk = ChunkStorage()
            # First thing in chunk is 4 bytes of chunk length, in bytes
            chunk_length = f.read(4)
            chunk_length = bytes_to_signed_int(chunk_length)
            _current_chunk.length = chunk_length
            # Next byte denotes compression type
            _compression_type_index = f.read(1)
            _compression_type_index = bytes_to_int(_compression_type_index)
            compression_type = CHUNK_COMPRESSION_TYPES[_compression_type_index]
            _current_chunk.compression_type_index = _compression_type_index
            # `chunk_length-1` bytes of compressed chunk data follows
            _compressed_chunk_data = f.read(chunk_length-1)
            _current_chunk.compressed_data = _compressed_chunk_data
            if compression_type == 'custom':
                raise NotImplementedError('Custom chunk compression is not implemented.')
            elif compression_type == 'lz4':
                raise NotImplementedError('LZ4 chunk compression is not implemented.')
            elif compression_type == 'uncompressed':
                _decompressed_chunk_data = _compressed_chunk_data
            elif compression_type == 'gzip':
                raise NotImplementedError('GZip chunk compression is not implemented. It is unused in practice so there could be something wrong with the .mca file.')
            elif compression_type == 'zlib':
                _decompressed_chunk_data = zlib.decompress(_compressed_chunk_data)
            _working_chunk_data = bytearray(_decompressed_chunk_data)
            # Find Xpos and Ypos for inhabitedtime storing
            _xpos_name_position = _decompressed_chunk_data.find(b'\x03\x00\x04xPos')
            _xpos_value_position = _xpos_name_position + len(b'\x03\x00\x04xPos')
            _current_xpos = _working_chunk_data[_xpos_value_position:_xpos_value_position+4]  # Int
            _current_xpos = bytes_to_signed_int(_current_xpos)
            _ypos_name_position = _decompressed_chunk_data.find(b'\x03\x00\x04yPos')
            _ypos_value_position = _ypos_name_position + len(b'\x03\x00\x04yPos')
            _current_ypos = _working_chunk_data[_ypos_value_position:_ypos_value_position+4]  # Int
            _current_ypos = bytes_to_signed_int(_current_ypos)
            # Find InhabitedTime
            _inti_name_position = _decompressed_chunk_data.find(b'InhabitedTime')
            assert _inti_name_position != -1
            _inti_value_position = _inti_name_position + len(b'InhabitedTime')
            _current_inti = _working_chunk_data[_inti_value_position:_inti_value_position+8]  # Long
            _current_inti = bytes_to_signed_int(_current_inti)
            print(_current_inti)
            initial_inti[(_current_xpos, _current_ypos)] = _current_inti
            # Reset InhabitedTime
            _working_chunk_data[_inti_value_position:_inti_value_position+8] = b'\x00' * 8
            # Prepare data for write
            _new_compressed_chunk = zlib.compress(bytes(_working_chunk_data))
            _current_chunk.compressed_data = _new_compressed_chunk
            _new_chunk_length = len(_new_compressed_chunk) + 1  # Our compressed data may be different in size
            _current_chunk.length = _new_chunk_length
            loc.sector_count = math.ceil(_new_chunk_length / SECTOR_SIZE)
            chunks.append(_current_chunk)
    
    # Write out file on the basis of the given file
    # TODO: Should be configurable
    working_file_bytes = bytearray()
    with open(file_path, 'rb') as fi:
        working_file_bytes = bytearray(fi.read())
    current_offset = 0  # Bookkeeping; use as seek()
    for loc in locations:
        working_file_bytes[current_offset:current_offset+4] = loc.to_bytes()
        current_offset += 4
    assert current_offset == SECTOR_SIZE
    for t in timestamps:
        working_file_bytes[current_offset:current_offset+4] = t.to_bytes(4, 'big', signed=False)
        current_offset += 4
    assert current_offset == 2 * SECTOR_SIZE
    for i, loc in enumerate(locations):
        current_offset = loc.offset * SECTOR_SIZE
        chunk_bytes = chunks[i].to_bytes()
        working_file_bytes[current_offset:current_offset+len(chunk_bytes)] = chunk_bytes
        current_offset += len(chunk_bytes)
    assert len(working_file_bytes) / SECTOR_SIZE == 0  # Should always be true given initial region file was valid
    with open(out_file, 'wb') as fo:
        fo.write(bytes(working_file_bytes))

        # for t in timestamps:
        #     fo.write(t.to_bytes(4, 'big', signed=False))
        # # Unoptimized but shouldn't matter much
        # for i, loc in enumerate(locations):  # Iterate again so we can find where chunks are supposed to be.
        #     fo.seek(loc.offset * SECTOR_SIZE)
        #     fo.write(chunks[i].to_bytes())
        # # Pad file end if it doesn't seem padded already
        # fo.seek(0, os.SEEK_END)
        # file_size = fo.tell()
        

        # # FIXME: Simply following stream doesn't seem to be working; need to change to location-based reading
        # _chunks_count = 0
        # while _chunks_count < len(locations) and _chunks_count < 1024:
        #     # Load the next chunk
            
        #         
        #         out_data += _new_chunk_length.to_bytes(4, 'big', signed=True)
        #         out_data += _compression_type_index.to_bytes(1, 'big', signed=False)
        #         out_data += _new_compressed_chunk
        #         # out_data += b'\x00' * (len(_compressed_chunk_data) - len(_new_compressed_chunk))
        #         # f.read(4096-4-(chunk_length % 4096))
        #         f.read(4096 - ((4+chunk_length) % 4096))
        #         out_data += b'\x00' * (4096 - ((4+_new_chunk_length) % 4096))
        #         # Sometimes an additional 4096 bytes padding is added after some chunks???
        #         # Will be an issue when reading. Not when writing. I'm having an issue here
        #         # purely because I don't want to edit the locations table just yet.
        #         while f.peek()[:2] != b'\x00\x00' or f.peek()[4] not in CHUNK_COMPRESSION_TYPES.keys():
        #             # Stopped working on #963???
        #             # Why are there 2 4096b paddings?????
        #             # WHY ARE YOU DOING THIS MOJANG
        #             # now that I think of it it could be garbage data leftover from repeated writing
        #             # but still
        #             out_data += f.read(4096)
        #             print(_chunks_count, file=sys.stderr)
        #         assert len(out_data) % 4096 == 0
        #         _chunks_count += 1
        #         continue

        #         chunk_bytes_stream = BytesIO(_decompressed_chunk_data)
        #         chunk_bytes_length = len(_decompressed_chunk_data)
            
        #     return
        #     # Parse chunk NBT data
        #     parsed_tags = []
        #     while chunk_bytes_stream.tell() <= chunk_bytes_length:
        #         # A byte begins with 1 byte tag type ID
        #         _next_tag_id = chunk_bytes_stream.read(1)
        #         _next_tag_id = bytes_to_int(_next_tag_id)
        #         next_tag_type = TAGS_LOOKUP[_next_tag_id]
        #         # If it is TAG_End, then it won't have a name
        #         # so we leave early
        #         if next_tag_type == tags.TAG_End:
        #             next_tag = tags.TAG_End()
        #             parsed_tags.append(next_tag)
        #             continue
        #         # Otherwise it is followed by 2 bytes big-endian name length
        #         next_tag_name_length = chunk_bytes_stream.read(2)
        #         next_tag_name_length = bytes_to_int(next_tag_name_length)
        #         # Then a NON-null-terminated UTF-8 string containing the tag name
        #         next_tag_name = chunk_bytes_stream.read(next_tag_name_length)
        #         next_tag_name = str(next_tag_name, 'utf-8')
        #         # Depending on the TAG type the payload will be different sizes
        # out_data += f.read()
        
                
    print('I made it to the end!')

if __name__ == '__main__':
    main()