# Embedded file name: chunkfile\bone_mesh_chunk.pyc
from chunk import Chunk, VersionError, DataReader
from chunk_utils import *
import struct


class BoneMeshChunk(Chunk):

    def format(self, pos):
        if self.version != 1860:
            raise VersionError
        reader = DataReader(self.data)
        header = self.read_header(reader)
        header.format(pos)
        num_vertices = header.find_field("nVerts").value
        for vertex_index in xrange(num_vertices):
            self.read_vertex(reader, vertex_index).format(pos)

        num_faces = header.find_field("nFaces").value
        for face_index in xrange(num_faces):
            self.read_face(reader, face_index).format(pos)

    def read_header(self, reader):
        field_defs = []
        if not self.withoutheader:
            add_chunk_header_fields(field_defs)
        field_defs.extend(
            (
                FlagsDef("flags1", "B", ["FLAG1_BONE_INFO"]),
                FlagsDef(
                    "flags2", "B", ["FLAG2_HAS_VERTEX_COLOR", "FLAG2_HAS_VERTEX_ALPHA"]
                ),
                FieldDef("nVerts", "i"),
                FieldDef("nTVerts", "i"),
                FieldDef("nFaces", "i"),
                FieldDef("VertAnimID", "i"),
            )
        )
        return read_fields("", self.bigendian, field_defs, reader)

    def read_vertex(self, reader, index):
        field_defs = [
            FieldDef("position[{0}]".format(index), "3f"),
            FieldDef("normal[{0}]".format(index), "3f"),
        ]
        return read_fields(None, self.bigendian, field_defs, reader)

    def read_face(self, reader, index):
        field_defs = [
            FieldDef("vert_indices[{0}]".format(index), "3i"),
            FieldDef("mat_id[{0}]".format(index), "i"),
        ]
        return read_fields(None, self.bigendian, field_defs, reader)
