# Embedded file name: chunkfile\compiled_morph_targets_chunk.pyc
from chunk import Chunk, VersionError, DataReader
from chunk_utils import *
import struct


class CompiledMorphTargetsChunk(Chunk):

    def format(self, pos):
        if self.version == 2048 or self.version == 2049:
            reader = DataReader(self.data)
            header = self.read_header(reader)
            header.format(pos)
            num_morph_targets = header.find_field("numMorphTargets").value
            for morph_target_index in xrange(num_morph_targets):
                morph_target_header = self.read_morph_target_header_v1(
                    reader, morph_target_index
                )
                morph_target_header.format(pos)
                name_length = morph_target_header.find_field("NameLength").value
                self.read_morph_target_name(reader, name_length).format(pos)
                int_vertex_count = morph_target_header.find_field(
                    "numIntVertices"
                ).value
                for target_vertex_index in xrange(int_vertex_count):
                    self.read_morph_target_int_vertex(
                        reader, target_vertex_index
                    ).format(pos)

                ext_vertex_count = morph_target_header.find_field(
                    "numExtVertices"
                ).value
                for target_vertex_index in xrange(ext_vertex_count):
                    self.read_morph_target_ext_vertex(
                        reader, target_vertex_index
                    ).format(pos)

        else:
            raise VersionError

    def read_header(self, reader):
        field_defs = []
        if not self.withoutheader:
            add_chunk_header_fields(field_defs)
        field_defs.extend((FieldDef("numMorphTargets", "I"),))
        return read_fields("", self.bigendian, field_defs, reader)

    def read_morph_target_header_v1(self, reader, morph_target_index):
        field_defs = [
            FieldDef("MeshID", "I", hex),
            FieldDef("NameLength", "I"),
            FieldDef("numIntVertices", "I"),
            FieldDef("numExtVertices", "I"),
        ]
        return read_fields(
            "MorphTarget[{0}]".format(morph_target_index),
            self.bigendian,
            field_defs,
            reader,
        )

    def read_morph_target_name(self, reader, string_length):
        field_defs = [FieldDef("name", "%ds" % string_length, strz_add_quotes)]
        return read_fields("name", self.bigendian, field_defs, reader)

    def read_morph_target_int_vertex(self, reader, target_vertex_index):
        field_defs = [
            FieldDef("IntVertex[{0}].nVertexId".format(target_vertex_index), "I"),
            FieldDef("IntVertex[{0}].ptVertex".format(target_vertex_index), "3f"),
        ]
        return read_fields(None, self.bigendian, field_defs, reader)

    def read_morph_target_ext_vertex(self, reader, target_vertex_index):
        field_defs = [
            FieldDef("ExtVertex[{0}].nVertexId".format(target_vertex_index), "I"),
            FieldDef("ExtVertex[{0}].ptVertex".format(target_vertex_index), "3f"),
        ]
        return read_fields(None, self.bigendian, field_defs, reader)
