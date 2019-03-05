# Embedded file name: chunkfile\helper_chunk.pyc
from chunk import Chunk, VersionError, DataReader
from chunk_utils import *
import struct


class HelperChunk(Chunk):

    def format(self, pos):
        if self.version == 1860:
            reader = DataReader(self.data)
            header = self.read_header(reader)
            header.format(pos)
        else:
            raise VersionError

    def read_header(self, reader):
        field_defs = []
        if not self.withoutheader:
            add_chunk_header_fields(field_defs)
        field_defs.extend(
            (
                EnumDef(
                    "type",
                    "i",
                    ["HP_POINT", "HP_DUMMY", "HP_XREF", "HP_CAMERA", "HP_GEOMETRY"],
                ),
                FieldDef("size", "3f"),
            )
        )
        return read_fields("", self.bigendian, field_defs, reader)
