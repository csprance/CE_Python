# Embedded file name: chunkfile\global_animation_header_caf_chunk.pyc
from chunk import Chunk, VersionError, DataReader
from chunk_utils import *
import struct


class GlobalAnimationHeaderCafChunk(Chunk):

    def format(self, pos):
        if self.version != 2417:
            raise VersionError
        reader = DataReader(self.data)
        header = self.read_header(reader)
        header.format(pos)

    def read_header(self, reader):
        field_defs = []
        if not self.withoutheader:
            add_chunk_header_fields(field_defs)
        field_defs.extend(
            (
                FieldDef("m_Flags", "I"),
                FieldDef("m_FilePath", "256s", null_termin),
                FieldDef("m_FilePathCRC32", "I"),
                FieldDef("m_FilePathDBACRC32", "I"),
                FieldDef("m_LHeelStart,m_LHeelEnd", "2f"),
                FieldDef("m_LToe0Start,m_LToe0End", "2f"),
                FieldDef("m_RHeelStart,m_RHeelEnd", "2f"),
                FieldDef("m_RToe0Start,m_RToe0End", "2f"),
                FieldDef("m_fStartSec", "f"),
                FieldDef("m_fEndSec", "f"),
                FieldDef("m_fTotalDuration", "f"),
                FieldDef("m_nControllers", "I"),
                FieldDef("m_StartLocation(quat)", "4f"),
                FieldDef("m_StartLocation(pos)", "3f"),
                FieldDef("m_LastLocatorKey(quat)", "4f"),
                FieldDef("m_LastLocatorKey(pos)", "3f"),
                FieldDef("m_vVelocity", "3f"),
                FieldDef("m_fDistance", "f"),
                FieldDef("m_fSlope", "f"),
                FieldDef("m_fTurnSpeed", "f"),
                FieldDef("m_fAssetTurn", "f"),
            )
        )
        return read_fields("", self.bigendian, field_defs, reader)
