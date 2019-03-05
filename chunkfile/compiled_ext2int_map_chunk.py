#Embedded file name: chunkfile\compiled_ext2int_map_chunk.pyc
from chunk import Chunk, VersionError, DataReader
from chunk_utils import *
import struct

class CompiledExt2intMapChunk(Chunk):

    def format(self, pos):
        if self.version != 2048:
            raise VersionError
        reader = DataReader(self.data)
        header_field_defs = []
        if not self.withoutheader:
            add_chunk_header_fields(header_field_defs)
        if len(header_field_defs) > 0:
            header = read_fields('', self.bigendian, header_field_defs, reader)
            header.format(pos)
            num_items = (len(self.data) - get_fields_size(header_field_defs)) / struct.calcsize('H')
        else:
            num_items = len(self.data) / struct.calcsize('H')
        print 'Count: {0}'.format(num_items)
        for item_index in xrange(num_items):
            self.read_item(reader, item_index).format(pos)

    def read_item(self, reader, item_index):
        return read_fields(None, self.bigendian, [FieldDef('ext2int[{0}]'.format(item_index), 'H')], reader)
