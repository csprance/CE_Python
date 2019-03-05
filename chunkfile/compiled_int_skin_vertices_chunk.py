#Embedded file name: chunkfile\compiled_int_skin_vertices_chunk.pyc
from chunk import Chunk, VersionError, DataReader
from chunk_utils import *
import struct
vertex_field_defs = [FieldDef('obsolete0', '12s', hex_dump),
 FieldDef('pos', '3f'),
 FieldDef('obsolete2', '12s', hex_dump),
 FieldDef('boneIDs', '4H'),
 FieldDef('weights', '4f'),
 FieldDef('blend', '4B')]

class CompiledIntSkinVerticesChunk(Chunk):

    def format(self, pos):
        if self.version != 2048:
            raise VersionError
        reader = DataReader(self.data)
        header_field_defs = []
        if not self.withoutheader:
            add_chunk_header_fields(header_field_defs)
        header_field_defs.extend((FieldDef('reserved', '32s', hex_dump),))
        header = read_fields('', self.bigendian, header_field_defs, reader)
        header.format(pos)
        num_vertices = (len(self.data) - get_fields_size(header_field_defs)) / get_fields_size(vertex_field_defs)
        print 'VertexCount: {0}'.format(num_vertices)
        for vertex_index in xrange(num_vertices):
            self.read_vertex(reader, vertex_index).format(pos)

    def read_vertex(self, reader, vertex_index):
        return read_fields('Vertex (%d)' % vertex_index, self.bigendian, vertex_field_defs, reader)
