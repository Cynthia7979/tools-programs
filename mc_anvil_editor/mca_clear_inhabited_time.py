'''
Based on https://minecraft.wiki/w/Region_file_format
## For testing use only not meant for production
'''
import os
import sys
import zlib
import math
import json
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

    def __eq__(s, o):
        if isinstance(o, LocationEntry):
            return s.offset == o.offset and s.sector_count == o.sector_count
        return False

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

def parse_region(path: str):
    chunk_to_inhabited_time = {}
    locations = []
    timestamps = []
    chunks = []
    with open(path, 'rb') as f:
        region_file_size = os.stat(path).st_size
        if region_file_size == 0:
            # TODO: Custom error class
            return None, None, None, None
        # Parse the header of region file
        # 0x1000 bytes of chunk locations (AKA offsets)
        _locations_header = f.read(0x1000)
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
        for i in range(0, 0x1000, 4):
            timestamps.append(bytes_to_int(_timestamps_header[i : i+4]))
        # The rest is chunks
        for loc in locations:
            assert isinstance(loc, LocationEntry)  # So that linter could be more helpful
            if loc.offset == 0:  # Ungenerated chunk (I think)
                chunks.append(None)
                continue
            assert 1 < loc.offset < math.ceil(region_file_size / SECTOR_SIZE), f'Invalid chunk offset {loc.offset}.'
            # Find the corresponding chunk
            f.seek(SECTOR_SIZE * loc.offset)
            current_chunk = ChunkStorage()
            # First thing in chunk is 4 bytes of chunk length, in bytes
            current_chunk.length = bytes_to_signed_int(f.read(4))
            # Next byte denotes compression type
            compression_type_index = f.read(1)
            compression_type_index = bytes_to_int(compression_type_index)
            compression_type = CHUNK_COMPRESSION_TYPES[compression_type_index]
            current_chunk.compression_type_index = compression_type_index
            # `chunk_length-1` bytes of compressed chunk data follows
            current_chunk.compressed_data = f.read(current_chunk.length-1)
            if compression_type == 'custom':
                raise NotImplementedError('Custom chunk compression is not implemented.')
            elif compression_type == 'lz4':
                raise NotImplementedError('LZ4 chunk compression is not implemented.')
            elif compression_type == 'uncompressed':
                decompressed_chunk_data = current_chunk.compressed_data
            elif compression_type == 'gzip':
                raise NotImplementedError('GZip chunk compression is not implemented. It is unused in practice so there could be something wrong with the .mca file.')
            elif compression_type == 'zlib':
                decompressed_chunk_data = zlib.decompress(current_chunk.compressed_data)
            working_chunk_data = bytearray(decompressed_chunk_data)
            # Find Xpos and Ypos for inhabitedtime storing
            _xpos_name_position = decompressed_chunk_data.find(b'\x03\x00\x04xPos')
            _xpos_value_position = _xpos_name_position + len(b'\x03\x00\x04xPos')
            xpos = working_chunk_data[_xpos_value_position:_xpos_value_position+4]  # Int
            xpos = bytes_to_signed_int(xpos)
            _ypos_name_position = decompressed_chunk_data.find(b'\x03\x00\x04yPos')
            _ypos_value_position = _ypos_name_position + len(b'\x03\x00\x04yPos')
            ypos = working_chunk_data[_ypos_value_position:_ypos_value_position+4]  # Int
            ypos = bytes_to_signed_int(ypos)
            # Find InhabitedTime
            _inti_name_position = decompressed_chunk_data.find(b'InhabitedTime')
            assert _inti_name_position != -1
            _inti_value_position = _inti_name_position + len(b'InhabitedTime')
            inhabited_time = working_chunk_data[_inti_value_position:_inti_value_position+8]  # Long
            inhabited_time = bytes_to_signed_int(inhabited_time)
            print(inhabited_time)
            chunk_to_inhabited_time[f'({xpos}, {ypos})'] = inhabited_time
            # Reset InhabitedTime
            working_chunk_data[_inti_value_position:_inti_value_position+8] = b'\x00' * 8
            # Prepare data for write
            _new_compressed_chunk = zlib.compress(bytes(working_chunk_data))
            current_chunk.compressed_data = _new_compressed_chunk
            current_chunk.length = len(_new_compressed_chunk) + 1 # Our compressed data may be different in size due to more zeroes
            loc.sector_count = math.ceil(current_chunk.length / SECTOR_SIZE)
            chunks.append(current_chunk)
    return chunk_to_inhabited_time, locations, timestamps, chunks

def write_region(outputfile_path: str, basefile_path: str, locations, timestamps, chunks):
    # Write out file on the basis of the given file
    # FIXME: Better code
    # TODO: Should be configurable
    working_file_bytes = bytearray()
    with open(basefile_path, 'rb') as fi:
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
        if current_offset == 0:  # Ungenerated chunk (I think)
            continue
        chunk_bytes = chunks[i].to_bytes()
        working_file_bytes[current_offset:current_offset+len(chunk_bytes)] = chunk_bytes
        current_offset += len(chunk_bytes)
    assert len(working_file_bytes) % SECTOR_SIZE == 0.0, f'Invalid initial file? File size is {len(working_file_bytes)} which is {len(working_file_bytes) / SECTOR_SIZE}x the sector size.'  # Should always be true given initial region file was valid
    with open(outputfile_path, 'wb') as fo:
        fo.write(bytes(working_file_bytes))

def main():
    regions_folder = 'D:/UserDocuments/temp/Drehmal v2.2.1 APOTHEOSIS 1.20/region/'
    # file_path = 'D:/UserDocuments/temp/r.-1.3.mca'
    out_folder = 'D:/UserDocuments/temp/out/region'
    inhabited_time_file = 'D:/UserDocuments/temp/out/inti.dat'
    stored_inhabited_time = {}
    
    for region_file in os.listdir(regions_folder):
        if not region_file.endswith('.mca'):
            continue
        chunk_to_inhabited_time, locations, timestamps, chunks = \
                parse_region(os.path.join(regions_folder, region_file))
        if None in (chunk_to_inhabited_time, locals, timestamps, chunks):
            print(f'WARNING: Skipping {region_file} because of empty file.')
            continue
        stored_inhabited_time[region_file] = chunk_to_inhabited_time
        write_region(
            os.path.join(out_folder, region_file),
            os.path.join(regions_folder, region_file),
            locations,
            timestamps,
            chunks
        )
    with open(inhabited_time_file, 'w') as intif:
        json.dump(stored_inhabited_time, intif)
    print('I made it to the end!')

if __name__ == '__main__':
    main()