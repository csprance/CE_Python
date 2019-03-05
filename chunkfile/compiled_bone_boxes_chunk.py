# Embedded file name: chunkfile\compiled_bone_boxes_chunk.pyc
from chunk import Chunk, VersionError, DataReader
from chunk_utils import *
import struct


class CompiledBoneBoxesChunk(Chunk):

    def format(self, pos):
        if self.version != 2048 and self.version != 2049:
            raise VersionError
        reader = DataReader(self.data)
        header = self.read_header(reader)
        header.format(pos)
        num_indices = header.find_field("indexCount").value
        for i in xrange(num_indices):
            r = read_fields(
                None, self.bigendian, [FieldDef("index[{0}]".format(i), "h")], reader
            )
            r.format(pos)

    def read_header(self, reader):
        field_defs = []
        if not self.withoutheader:
            add_chunk_header_fields(field_defs)
        field_defs.extend(
            (
                FieldDef("boneId", "i"),
                FieldDef("AABBmin", "3f"),
                FieldDef("AABBmax", "3f"),
                FieldDef("indexCount", "i"),
            )
        )
        return read_fields("", self.bigendian, field_defs, reader)
