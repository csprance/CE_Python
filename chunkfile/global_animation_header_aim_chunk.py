#Embedded file name: chunkfile\global_animation_header_aim_chunk.pyc
from chunk import Chunk, VersionError, DataReader
from chunk_utils import *
import struct

class GlobalAnimationHeaderAimChunk(Chunk):

    def format(self, pos):
        if self.version != 2416:
            raise VersionError
        reader = DataReader(self.data)
        header = self.read_header(reader)
        header.format(pos)
        print 'parsing of remaining data is not implemented yet'

    def read_header(self, reader):
        field_defs = []
        if not self.withoutheader:
            add_chunk_header_fields(field_defs)
        field_defs.extend((FieldDef('m_Flags', 'I'),
         FieldDef('m_FilePath', '256s', null_termin),
         FieldDef('m_FilePathCRC32', 'I'),
         FieldDef('m_fStartSec', 'f'),
         FieldDef('m_fEndSec', 'f'),
         FieldDef('m_fTotalDuration', 'f'),
         FieldDef('m_AnimTokenCRC32', 'I'),
         FieldDef('m_nExist', 'I'),
         FieldDef('m_MiddleAimPoseRot(quat)', '4f'),
         FieldDef('m_MiddleAimPose(quat)', '4f')))
        return read_fields('', self.bigendian, field_defs, reader)
