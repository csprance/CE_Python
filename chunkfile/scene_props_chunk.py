# Embedded file name: chunkfile\scene_props_chunk.pyc
from chunk import Chunk, VersionError, DataReader
from chunk_utils import *
import struct


class ScenePropsChunk(Chunk):

    def format(self, pos):
        if self.version != 1860:
            raise VersionError
        reader = DataReader(self.data)
        header = self.read_header(reader)
        header.format(pos)
        num = header.find_field("propCount").value
        for i in xrange(num):
            r = read_fields(
                None,
                self.bigendian,
                [
                    FieldDef("name[{0}]".format(i), "32s", strz_add_quotes),
                    FieldDef("value[{0}]".format(i), "64s", strz_add_quotes),
                ],
                reader,
            )
            r.format(pos)

    def read_header(self, reader):
        field_defs = []
        if not self.withoutheader:
            add_chunk_header_fields(field_defs)
        field_defs.extend((FieldDef("propCount", "i"),))
        return read_fields("", self.bigendian, field_defs, reader)
