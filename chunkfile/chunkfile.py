import chunks
import chunk_utils
import struct
import sys

class BadChunkFileFormatError(Exception):
    pass


class ChunkDocument(object):

    def __init__(self):
        self.chunks = []
        self.id_chunk_map = {}

    def add_chunk(self, chunk):
        assert chunk.id not in self.id_chunk_map
        self.chunks.append(chunk)
        self.id_chunk_map[chunk.id] = chunk


class ChunkEntry(object):

    def __init__(self, chunk, pos):
        self.chunk = chunk
        self.pos = pos


class IDError(Exception):
    pass


class OffsetMapEntry(object):

    def __init__(self, bounds):
        self.bounds = bounds

    def format(self):
        print('[%.8X - %.8X] %s' % (self.bounds[0], self.bounds[1], self.get_description()))


class FileHeaderOffsetMapEntry(OffsetMapEntry):

    def __init__(self, bounds):
        OffsetMapEntry.__init__(self, bounds)

    def get_description(self):
        return 'File Header'


class ChunkListOffsetMapEntry(OffsetMapEntry):

    def __init__(self, bounds):
        OffsetMapEntry.__init__(self, bounds)

    def get_description(self):
        return 'Chunk List'


class ChunkOffsetMapEntry(OffsetMapEntry):

    def __init__(self, bounds, chunk):
        OffsetMapEntry.__init__(self, bounds)
        self.chunk = chunk

    def get_description(self):
        return 'Chunk ID = 0x%X: %s' % (self.chunk.id, self.chunk.name)


class ChunkFile(object):

    def __init__(self):
        self.doc = ChunkDocument()
        self.chunk_entries = []
        self.id_entry_map = {}
        self.offset_map = []
        self.version = -1
        self.header_text = []

    def add_chunk(self, chunk, pos):
        if chunk.id in self.id_entry_map:
            return False
        entry = ChunkEntry(chunk, pos)
        self.chunk_entries.append(entry)
        self.id_entry_map[chunk.id] = entry
        self.doc.add_chunk(chunk)
        return True

    def get_chunk(self, chunk_id):
        try:
            chunk = self.id_entry_map[chunk_id]
        except KeyError as err:
            raise IDError

        return (chunk.pos, chunk.chunk)

    def iter_chunk_entries(self):
        for entry in self.chunk_entries:
            yield (entry.chunk.id,
             entry.chunk.typecode,
             entry.pos,
             entry.chunk.name)

    def iter_chunks(self):
        for entry in self.chunk_entries:
            yield (entry.chunk, entry.pos)


def read_header(f, offset_map, chunk_descriptors, header_text):
    f.seek(0, 2)
    file_size = f.tell()
    f.seek(0, 0)
    header_fmt = '<4siII'
    header = f.read(struct.calcsize(header_fmt))
    sig, version, chunk_count, chunktablepos = struct.unpack(header_fmt, header)
    header_text.append('File header:')
    if sig == 'CrCh' and version == 1862 and chunk_count >= 0:
        header_text.append("    signature = '{0}'".format(sig))
        header_text.append('    version = {0}'.format(hex(version)))
        header_text.append('    chunk count = {0}'.format(chunk_count))
        header_text.append('    chunk table offset = {0}'.format(chunktablepos))
    else:
        f.seek(0, 0)
        header_fmt = '<6sbxIiI'
        header = f.read(struct.calcsize(header_fmt))
        sig, sigTail, filetype, version, chunktablepos = struct.unpack(header_fmt, header)
        chunk_count = -1
        if sig != 'CryTek' or sigTail != 0 or version < 1860 or version > 1861:
            raise BadChunkFileFormatError()
        header_text.append("    signature = '{0}'".format(sig))
        header_text.append('    filetype = {0}'.format(hex(filetype)))
        header_text.append('    version = {0}'.format(hex(version)))
        header_text.append('    chunk table offset = {0}'.format(chunktablepos))
    header_text.append('File header (hex dump):')
    header_text.append('    {0}'.format(chunk_utils.hex_dump(struct.unpack('{0}B'.format(len(header)), header))))
    offset_map.append(FileHeaderOffsetMapEntry((0, struct.calcsize(header_fmt))))
    if version <= 1861:
        entry_fmt = '<' + ('IIIi' if version < 1861 else 'IIIiI')
    else:
        entry_fmt = '<HHIiI'
    if version <= 1861:
        f.seek(chunktablepos)
        header_fmt = '<I'
        header = f.read(struct.calcsize(header_fmt))
        chunk_count, = struct.unpack(header_fmt, header)
        offset_map.append(ChunkListOffsetMapEntry((chunktablepos, chunktablepos + struct.calcsize(header_fmt) + chunk_count * struct.calcsize(entry_fmt))))
        chunktablepos += struct.calcsize(header_fmt)
    header_text.append('Chunk count: {0}'.format(chunk_count))
    f.seek(chunktablepos)
    for index in xrange(chunk_count):
        entry = f.read(struct.calcsize(entry_fmt))
        if version >= 1862:
            ch_type, ch_version, ch_id, ch_size, ch_pos = struct.unpack(entry_fmt, entry)
            ch_bigendian = ch_version & 32768 != 0
            ch_version = ch_version & -32769
            ch_withoutheader = True
        else:
            if version >= 1861:
                ch_type, ch_version, ch_pos, ch_id, ch_size = struct.unpack(entry_fmt, entry)
            else:
                ch_type, ch_version, ch_pos, ch_id = struct.unpack(entry_fmt, entry)
                ch_size = 0
            ch_bigendian = ch_version & 2147483648L != 0
            ch_version = ch_version & -2147483649L
            ch_withoutheader = False
        chunk_descriptors.append([ch_id,
         ch_type,
         ch_version,
         ch_pos,
         ch_size,
         ch_bigendian,
         ch_withoutheader])

    chunk_descriptors.sort(lambda a, b: cmp(a[3], b[3]))
    if version < 1861:
        chunk_starts = [ e[3] for e in chunk_descriptors ]
        chunk_ends = chunk_starts[1:] + [file_size]
        if chunktablepos > chunk_starts[-1]:
            chunk_ends[-1] = chunktablepos
        for index in xrange(chunk_count):
            chunk_descriptors[index][4] = chunk_ends[index] - chunk_starts[index]


def load_chunk_file(filename):
    chunk_file = ChunkFile()
    f = file(filename, 'rb')
    chunk_descriptors = []
    read_header(f, chunk_file.offset_map, chunk_descriptors, chunk_file.header_text)
    for id, type, version, pos, size, bigendian, withoutheader in chunk_descriptors:
        f.seek(pos)
        data = f.read(size)
        chunk = chunks.create_chunk(id, type, version, bigendian, withoutheader, data)
        if not chunk_file.add_chunk(chunk, pos):
            continue
        chunk_file.offset_map.append(ChunkOffsetMapEntry((pos, pos + size), chunk))

    return chunk_file
