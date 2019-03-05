# Embedded file name: chunkfile\mtl_name_chunk.pyc
from chunk import Chunk, VersionError, DataReader
from chunk_utils import *
import struct


class MtlNameChunk(Chunk):

    def format(self, pos):
        if self.version == 2048:
            reader = DataReader(self.data)
            header = self.read_header_800(reader)
            header.format(pos)
        elif self.version == 2050:
            reader = DataReader(self.data)
            header = self.read_header_802(reader)
            header.format(pos)
            num_submaterials = header.find_field("nSubMaterials").value
            if num_submaterials == 0:
                num_submaterials = 1
            for submat_index in xrange(num_submaterials):
                self.read_submaterial(reader, submat_index).format(pos)

        else:
            raise VersionError

    def read_header_800(self, reader):
        field_defs = []
        field_defs.extend(
            (FieldDef("MTL_NAME_CHUNK_DESC_0800", None), FieldDef("", None))
        )
        if not self.withoutheader:
            add_chunk_header_fields(field_defs)
        field_defs.extend(
            (
                FlagsDef(
                    "flags1",
                    "I",
                    [
                        "FLAG_MULTI_MATERIAL",
                        "FLAG_SUB_MATERIAL",
                        "FLAG_SH_COEFFS",
                        "FLAG_SH_2SIDED",
                        "FLAG_SH_AMBIENT",
                    ],
                ),
                FieldDef("flags2", "i"),
                FieldDef("name", "128s", strz_add_quotes),
                EnumDef(
                    "nPhysicalizeType",
                    "i",
                    {
                        -1: "PHYS_GEOM_TYPE_NONE",
                        0: "PHYS_GEOM_TYPE_DEFAULT(old)",
                        1: "PHYS_GEOM_TYPE_NO_COLLIDE(old)",
                        2: "PHYS_GEOM_TYPE_OBSTRUCT(old)",
                        4096: "PHYS_GEOM_TYPE_DEFAULT",
                        4097: "PHYS_GEOM_TYPE_NO_COLLIDE",
                        4098: "PHYS_GEOM_TYPE_OBSTRUCT",
                        4352: "PHYS_GEOM_TYPE_DEFAULT_PROXY",
                    },
                ),
                FieldDef("nSubMaterials", "i"),
                FieldDef("nSubMatChunkId", "32i"),
                FieldDef("nAdvancedDataChunkId", "i"),
                FieldDef("sh_opacity", "f"),
                FieldDef("reserve", "128s", hex_dump),
            )
        )
        return read_fields("", self.bigendian, field_defs, reader)

    def read_header_802(self, reader):
        field_defs = []
        field_defs.extend(
            (FieldDef("MTL_NAME_CHUNK_DESC_0802", None), FieldDef("", None))
        )
        if not self.withoutheader:
            add_chunk_header_fields(field_defs)
        field_defs.extend(
            (FieldDef("name", "128s", strz_add_quotes), FieldDef("nSubMaterials", "i"))
        )
        return read_fields("", self.bigendian, field_defs, reader)

    def read_submaterial(self, reader, index):
        field_defs = [
            EnumDef(
                "submatPhysicalizeType[{0}]".format(index),
                "i",
                {
                    -1: "PHYS_GEOM_TYPE_NONE",
                    4096: "PHYS_GEOM_TYPE_DEFAULT",
                    4097: "PHYS_GEOM_TYPE_NO_COLLIDE",
                    4098: "PHYS_GEOM_TYPE_OBSTRUCT",
                    4352: "PHYS_GEOM_TYPE_DEFAULT_PROXY",
                },
            )
        ]
        return read_fields(None, self.bigendian, field_defs, reader)
