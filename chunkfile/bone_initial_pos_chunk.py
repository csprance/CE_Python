# Embedded file name: chunkfile\bone_initial_pos_chunk.pyc
from chunk import Chunk, VersionError, DataReader
from chunk_utils import *
import struct


class BoneInitialPosChunk(Chunk):

    def format(self, pos):
        if self.version != 1:
            raise VersionError
        reader = DataReader(self.data)
        header = self.read_header(reader)
        header.format(pos)
        num_bones = header.find_field("numBones").value
        for bone_index in xrange(num_bones):
            self.read_bone(reader, bone_index).format(pos)

    def read_header(self, reader):
        field_defs = [FieldDef("nChunkIdMesh", "I"), FieldDef("numBones", "I")]
        return read_fields("", self.bigendian, field_defs, reader)

    def read_bone(self, reader, bone_index):
        field_defs = [
            FieldDef("transform row 1", "3f"),
            FieldDef("transform row 2", "3f"),
            FieldDef("transform row 3", "3f"),
            FieldDef("transform row 4", "3f"),
        ]
        return read_fields(
            "Bone Initial Transform (%d)" % bone_index,
            self.bigendian,
            field_defs,
            reader,
        )
