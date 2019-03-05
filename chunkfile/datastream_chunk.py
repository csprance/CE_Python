# Embedded file name: chunkfile\datastream_chunk.pyc
from chunk import Chunk, VersionError, DataReader
from chunk_utils import *
import struct
import copy


class DataStreamChunk(Chunk):
    typeDefEntries = [
        ("CGF_STREAM_POSITIONS", ("Position", [])),
        ("CGF_STREAM_NORMALS", ("Normal", [FieldDef("normal", "3f")])),
        ("CGF_STREAM_TEXCOORDS", ("UV", [FieldDef("uv", "2f")])),
        ("CGF_STREAM_COLORS", ("Color", [FieldDef("rgba", "4B", hex_list)])),
        ("CGF_STREAM_COLORS2", ("Color 2", [FieldDef("rgba", "4B", hex_list)])),
        ("CGF_STREAM_INDICES", ("Index", [])),
        (
            "CGF_STREAM_TANGENTS",
            (
                "Tangent",
                [
                    FieldDef("Tangent", "4h", normalizedint16_to_str),
                    FieldDef("Binormal", "4h", normalizedint16_to_str),
                ],
            ),
        ),
        ("CGF_STREAM_SHCOEFFS", ("SH Coeff", [FieldDef("coeffs", "8B")])),
        (
            "CGF_STREAM_SHAPEDEFORMATION",
            (
                "Shape Deformation",
                [
                    FieldDef("thin", "3f"),
                    FieldDef("fat", "3f"),
                    FieldDef("index", "I", hex),
                ],
            ),
        ),
        ("CGF_STREAM_BONEMAPPING", ("Bone Mapping", [])),
        ("CGF_STREAM_FACEMAP", ("Facemap", [FieldDef("mapping", "H")])),
        ("CGF_STREAM_VERT_MATS", ("Vert Mats", [FieldDef("mat", "I")])),
        (
            "CGF_STREAM_QTANGENTS",
            ("QTangent", [FieldDef("TangentBinormal", "4h", normalizedint16_to_str)]),
        ),
        (
            "CGF_STREAM_SKINDATA",
            (
                "Skin Data",
                [
                    FieldDef("bVolumetric", "I"),
                    FieldDef("idx", "4I"),
                    FieldDef("w", "4f"),
                    FieldDef("matrix", "9f"),
                ],
            ),
        ),
        ("CGF_STREAM_PS3EDGEDATA", ("PS3 Edge Data", [FieldDef("data", "B")])),
        (
            "CGF_STREAM_P3S_C4B_T2S",
            (
                "P3S_C4B_T2S",
                [
                    FieldDef("pos", "4H", halffloat_to_str),
                    FieldDef("bgra", "4B", hex_list),
                    FieldDef("uv", "2H", halffloat_to_str),
                ],
            ),
        ),
    ]
    typeDefs = dict(typeDefEntries)
    streamTypeStrings = [x for x, y in typeDefEntries]

    def format(self, pos):
        if self.version != 2048:
            raise VersionError
        reader = DataReader(self.data)
        header = self.read_header(reader, self.streamTypeStrings)
        header.format(pos)
        typeString = header.find_field("nStreamType").get_enum_string()
        elementHeader, fieldDefs = self.typeDefs[typeString]
        fieldDefs = copy.deepcopy(fieldDefs)
        if elementHeader == "Position":
            if header.find_field("nElementSize").value == 8:
                fieldDefs = [FieldDef("pos", "4H", halffloat_to_str)]
            else:
                fieldDefs = [FieldDef("pos", "3f")]
        if elementHeader == "Index":
            if header.find_field("nElementSize").value == 2:
                fieldDefs = [FieldDef("index", "H")]
            else:
                fieldDefs = [FieldDef("index", "I")]
        if elementHeader == "Bone Mapping":
            if header.find_field("nElementSize").value == 8:
                fieldDefs = [
                    FieldDef("boneIDs", "4B"),
                    FieldDef("weights", "4B", normalizeduint8_to_str),
                ]
            else:
                fieldDefs = [
                    FieldDef("boneIDs", "4H"),
                    FieldDef("weights", "4B", normalizeduint8_to_str),
                ]
        fieldNames = [fd.name for fd in fieldDefs]
        elementCount = header.find_field("nCount").value
        for elementIndex in xrange(elementCount):
            for i in xrange(len(fieldDefs)):
                fieldDefs[i].name = fieldNames[i] + "[{0}]".format(elementIndex)

            read_fields(None, self.bigendian, fieldDefs, reader).format(pos)

    def read_header(self, reader, type_strings):
        field_defs = []
        if not self.withoutheader:
            add_chunk_header_fields(field_defs)
        field_defs.extend(
            (
                FieldDef("nFlags", "i", hex),
                EnumDef("nStreamType", "i", type_strings),
                FieldDef("nCount", "i"),
                FieldDef("nElementSize", "i"),
                FieldDef("reserved", "8s", hex_dump),
            )
        )
        return read_fields("", self.bigendian, field_defs, reader)

    def get_stream_type(self):
        reader = DataReader(self.data)
        header = self.read_header(reader, self.streamTypeStrings)
        return header.find_field("nStreamType").value

    def get_count(self):
        reader = DataReader(self.data)
        header = self.read_header(reader, self.streamTypeStrings)
        return header.find_field("nCount").value
