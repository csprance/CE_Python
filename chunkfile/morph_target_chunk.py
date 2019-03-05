# Embedded file name: chunkfile\morph_target_chunk.pyc
from chunk import Chunk, VersionError, DataReader
from chunk_utils import *
import struct


class MorphTargetChunk(Chunk):

    def format(self, pos):
        if self.version == 1:
            reader = DataReader(self.data)
            header = self.read_header_v1(reader)
            header.format(pos)
            num_target_vertices = header.find_field("numMorphVertices").value
            for target_vertex_index in xrange(num_target_vertices):
                self.read_mesh_morph_target_vertex(reader, target_vertex_index).format(
                    pos
                )

            string_length = self.size - reader.position
            self.read_name(reader, string_length).format(pos)
        else:
            raise VersionError

    def read_header_v1(self, reader):
        field_defs = [
            FieldDef("nChunkIdMesh", "I", hex),
            FieldDef("numMorphVertices", "I"),
        ]
        return read_fields("", self.bigendian, field_defs, reader)

    def read_mesh_morph_target_vertex(self, reader, target_vertex_index):
        field_defs = [
            FieldDef(
                "morphTargetVertex[{0}].nVertexId".format(target_vertex_index), "I"
            ),
            FieldDef(
                "morphTargetVertex[{0}].ptVertex".format(target_vertex_index), "3f"
            ),
        ]
        return read_fields(None, self.bigendian, field_defs, reader)

    def read_name(self, reader, string_length):
        field_defs = [FieldDef("name", "%ds" % string_length, strz_add_quotes)]
        return read_fields("name", self.bigendian, field_defs, reader)
