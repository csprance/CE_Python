#Embedded file name: chunkfile\compiled_int_faces_chunk.pyc
from chunk import Chunk, VersionError, DataReader
from chunk_utils import *
import struct

class CompiledIntFacesChunk(Chunk):

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
            num_faces = (len(self.data) - get_fields_size(header_field_defs)) / struct.calcsize('3H')
        else:
            num_faces = len(self.data) / struct.calcsize('3H')
        print 'FaceCount: {0}'.format(num_faces)
        for face_index in xrange(num_faces):
            self.read_face(reader, face_index).format(pos)

    def read_face(self, reader, face_index):
        return read_fields(None, self.bigendian, [FieldDef('face[{0}]'.format(face_index), '3H')], reader)
