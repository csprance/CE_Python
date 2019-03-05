# Embedded file name: chunkfile\motion_parameters_chunk.pyc
from chunk import Chunk, VersionError, DataReader
from chunk_utils import *
import struct


class MotionParametersChunk(Chunk):

    def format(self, pos):
        if self.version == 2341:
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
                FieldDef("assetFlags", "i", hex),
                FieldDef("compression", "i"),
                FieldDef("ticksPerFrame", "i"),
                FieldDef("secsPerTick", "f"),
                FieldDef("start", "i"),
                FieldDef("end", "i"),
                FieldDef("moveSpeed", "f"),
                FieldDef("turnSpeed", "f"),
                FieldDef("assetTurn", "f"),
                FieldDef("distance", "f"),
                FieldDef("slope", "f"),
                FieldDef("startLocation_quat", "4f"),
                FieldDef("startLocation_pos", "3f"),
                FieldDef("lastLocation_quat", "4f"),
                FieldDef("lastLocation_pos", "3f"),
                FieldDef("LHeel", "2f"),
                FieldDef("LToe", "2f"),
                FieldDef("RHeel", "2f"),
                FieldDef("RToe", "2f"),
            )
        )
        return read_fields("", self.bigendian, field_defs, reader)
