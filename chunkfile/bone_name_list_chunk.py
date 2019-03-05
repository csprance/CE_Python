# Embedded file name: chunkfile\bone_name_list_chunk.pyc
from chunk import Chunk, VersionError, DataReader
from chunk_utils import *
import struct


class BoneNameListChunk(Chunk):

    def format(self, pos):
        if self.version == 1860:
            reader = DataReader(self.data)
            header = self.read_header(reader)
            header.format(pos)
            num_bones = header.find_field("nEntities").value
            for bone_index in xrange(num_bones):
                self.read_bone(reader, bone_index).format(pos)

        elif self.version == 1861:
            reader = DataReader(self.data)
            header = self.read_header_745(reader)
            header.format(pos)
            num_bones = header.find_field("numEntities").value
            for bone_index in xrange(num_bones):
                self.read_packed_bone(reader, bone_index).format(pos)

        else:
            raise VersionError

    def read_header(self, reader):
        field_defs = []
        if not self.withoutheader:
            add_chunk_header_fields(field_defs)
        field_defs.extend((FieldDef("nEntities", "I"),))
        return read_fields("", self.bigendian, field_defs, reader)

    def read_header_745(self, reader):
        field_defs = [FieldDef("numEntities", "I")]
        return read_fields("", self.bigendian, field_defs, reader)

    def read_bone(self, reader, bone_index):
        field_defs = [FieldDef("name", "64s")]
        return read_fields(
            "Bone Name (%d)" % bone_index, self.bigendian, field_defs, reader
        )

    def read_packed_bone(self, reader, bone_index):
        term = reader.find("\x00")
        if term < 0:
            fmt = ""
        else:
            fmt = "{0}s".format(term - reader.position + 1)
        return read_fields(
            None,
            self.bigendian,
            [FieldDef("boneName[{0}]".format(bone_index), fmt, strz_add_quotes)],
            reader,
        )
