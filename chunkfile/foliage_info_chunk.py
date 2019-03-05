# Embedded file name: chunkfile\foliage_info_chunk.pyc
from chunk import Chunk, VersionError, DataReader
from chunk_utils import *
import binascii
import struct

spine_field_defs = [
    FieldDef("nVtx", "B"),
    FieldDef("_paddingA_", "3s", hex_dump),
    FieldDef("len", "f"),
    FieldDef("navg", "3f"),
    FieldDef("iAttachSpine", "B"),
    FieldDef("iAttachSeg", "B"),
    FieldDef("_paddingB_", "2s", hex_dump),
]


class FoliageInfoChunk(Chunk):

    def format(self, pos):
        if self.version != 1:
            raise VersionError
        reader = DataReader(self.data)
        header_field_defs = []
        if not self.withoutheader:
            add_chunk_header_fields(header_field_defs)
        header_field_defs.extend(
            (
                FieldDef("nSpines", "i"),
                FieldDef("nSpineVtx", "i"),
                FieldDef("nSkinnedVtx", "i"),
                FieldDef("nBoneIds", "i"),
            )
        )
        header = read_fields("", self.bigendian, header_field_defs, reader)
        header.format(pos)
        n = header.find_field("nSpines").value
        for i in xrange(n):
            r = read_fields("spine (%d)" % i, self.bigendian, spine_field_defs, reader)
            r.format(pos)

        n = header.find_field("nSpineVtx").value
        for i in xrange(n):
            r = read_fields(
                None,
                self.bigendian,
                [FieldDef("spineVtx[{0}]".format(i), "3f")],
                reader,
            )
            r.format(pos)

        n = header.find_field("nSpineVtx").value
        for i in xrange(n):
            r = read_fields(
                None,
                self.bigendian,
                [FieldDef("spineSegDim[{0}]".format(i), "4f")],
                reader,
            )
            r.format(pos)

        n = header.find_field("nSkinnedVtx").value
        for i in xrange(n):
            r = read_fields(
                None,
                self.bigendian,
                [
                    FieldDef("boneMapping[{0}].boneIDs".format(i), "4B"),
                    FieldDef("boneMapping[{0}].weights".format(i), "4B"),
                ],
                reader,
            )
            r.format(pos)

        n = header.find_field("nBoneIds").value
        for i in xrange(n):
            r = read_fields(
                None,
                self.bigendian,
                [FieldDef("chunkBoneIds[{0}]".format(i), "H")],
                reader,
            )
            r.format(pos)
