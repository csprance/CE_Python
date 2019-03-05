# Embedded file name: chunkfile\timing_chunk.pyc
from chunk import Chunk, VersionError, DataReader
from chunk_utils import *
import struct


class TimingChunk(Chunk):

    def format(self, pos):
        if self.version == 2328:
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
                FieldDef("SecsPerTick", "f"),
                FieldDef("TicksPerFrame", "i"),
                FieldDef("global_range.name", "32s", strz_add_quotes),
                FieldDef("global_range.start", "i"),
                FieldDef("global_range.end", "i"),
                FieldDef("nSubRanges", "i"),
            )
        )
        return read_fields("", self.bigendian, field_defs, reader)
