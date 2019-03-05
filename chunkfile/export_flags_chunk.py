# Embedded file name: chunkfile\export_flags_chunk.pyc
from chunk import Chunk, VersionError, DataReader
from chunk_utils import *
import struct


class ExportFlagsChunk(Chunk):

    def format(self, pos):
        if self.version == 1:
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
                FlagsDef(
                    "flags",
                    "I",
                    [
                        "MERGE_ALL_NODES",
                        "HAVE_AUTO_LODS",
                        "USE_CUSTOM_NORMALS",
                        "WANT_F32_VERTICES",
                        "EIGHT_WEIGHTS_PER_VERTEX",
                    ],
                ),
                FieldDef("rc_version", "4I"),
                FieldDef("rc_version_string", "16s", strz_add_quotes),
                FieldDef("assetAuthorTool", "I", hex),
                FieldDef("authorToolVersion", "I"),
                FieldDef("reserved", "120s", hex_dump),
            )
        )
        return read_fields("", self.bigendian, field_defs, reader)
