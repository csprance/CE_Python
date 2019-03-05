# Embedded file name: chunkfile\mesh_subsets_chunk.pyc
from chunk import Chunk, VersionError, DataReader
from chunk_utils import *
import struct


class MeshSubsetsChunk(Chunk):

    def format(self, pos):
        if self.version == 2048:
            reader = DataReader(self.data)
            header = self.read_header_800(reader)
            header.format(pos)
            hasDecompMatrices = header.find_field("flags").flag_set(
                "SH_HAS_DECOMPR_MAT"
            )
            hasBoneIndices = header.find_field("flags").flag_set("BONEINDICES")
            hasSubsetTexelDensity = header.find_field("flags").flag_set(
                "HAS_SUBSET_TEXEL_DENSITY"
            )
            subsetCount = header.find_field("nCount").value
            for subsetIndex in xrange(subsetCount):
                self.read_subset(reader, subsetIndex).format(pos)

            if hasDecompMatrices:
                for subsetIndex in xrange(subsetCount):
                    self.read_decomp_matrix(reader, subsetIndex).format(pos)

            if hasBoneIndices:
                for subsetIndex in xrange(subsetCount):
                    self.read_bone_indices(reader, subsetIndex).format(pos)

            if hasSubsetTexelDensity:
                for subsetIndex in xrange(subsetCount):
                    self.read_subset_texel_density(reader, subsetIndex).format(pos)

        else:
            raise VersionError

    def read_header_800(self, reader):
        field_defs = []
        if not self.withoutheader:
            add_chunk_header_fields(field_defs)
        field_defs.extend(
            (
                FlagsDef(
                    "flags",
                    "I",
                    ["SH_HAS_DECOMPR_MAT", "BONEINDICES", "HAS_SUBSET_TEXEL_DENSITY"],
                ),
                FieldDef("nCount", "i"),
                FieldDef("reserved", "8s", hex_dump),
            )
        )
        return read_fields("", self.bigendian, field_defs, reader)

    def read_subset(self, reader, index):
        field_defs = [
            FieldDef("nFirstIndexId", "i"),
            FieldDef("nNumIndices", "i"),
            FieldDef("nFirstVertId", "i"),
            FieldDef("nNumVerts", "i"),
            FieldDef("nMatID", "i"),
            FieldDef("fRadius", "f"),
            FieldDef("vCenter", "3f"),
        ]
        return read_fields(
            "Mesh Subset (%d)" % index, self.bigendian, field_defs, reader
        )

    def read_decomp_matrix(self, reader, index):
        field_defs = [
            FieldDef("offset0", "4f"),
            FieldDef("offset1", "4f"),
            FieldDef("scale0", "4f"),
            FieldDef("scale1", "4f"),
        ]
        return read_fields(
            "Decompression Matrix (%d)" % index, self.bigendian, field_defs, reader
        )

    def read_bone_indices(self, reader, index):

        def format_index_array(indices):
            values = [x for x in indices]
            s = ""
            while values:
                s += "\n\t\t"
                for line in xrange(4):
                    if values:
                        val = values.pop(0)
                        s += "%-10s" % ("%u," % val)

            return s

        field_defs = [
            FieldDef("numBoneIDs", "I"),
            FieldDef("arrBoneIDs", "128H", format_index_array),
        ]
        return read_fields(
            "Decompression Matrix (%d)" % index, self.bigendian, field_defs, reader
        )

    def read_subset_texel_density(self, reader, index):
        return read_fields(
            None,
            self.bigendian,
            [FieldDef("texelDensity[{0}]".format(index), "f")],
            reader,
        )
