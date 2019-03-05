# Embedded file name: chunkfile\breakable_physics_chunk.pyc
from chunk import Chunk, VersionError, DataReader
from chunk_utils import *
import struct


class BreakablePhysicsChunk(Chunk):

    def format(self, pos):
        if self.version == 1:
            reader = DataReader(self.data)
            header = self.read_header(reader)
            header.format(pos)
            num_vtx = header.find_field("nRetVtx").value
            num_tets = header.find_field("nRetTets").value
            for i in xrange(num_vtx):
                read_fields(
                    None,
                    self.bigendian,
                    (FieldDef("vtx[{0}]".format(i), "3f"),),
                    reader,
                ).format(pos)

            for i in xrange(num_tets):
                read_fields(
                    None,
                    self.bigendian,
                    (FieldDef("tets[{0}]".format(i), "4i"),),
                    reader,
                ).format(pos)

        else:
            raise VersionError

    def read_header(self, reader):
        field_defs = []
        if not self.withoutheader:
            add_chunk_header_fields(field_defs)
        field_defs.extend(
            [
                FieldDef("granularity", "I", hex),
                FieldDef("nMode", "i"),
                FieldDef("nRetVtx", "i"),
                FieldDef("nRetTets", "i"),
                FieldDef("nReserved", "10i"),
            ]
        )
        return read_fields("", self.bigendian, field_defs, reader)
