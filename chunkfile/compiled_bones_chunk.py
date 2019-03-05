# Embedded file name: chunkfile\compiled_bones_chunk.pyc
from chunk import Chunk, VersionError, DataReader
from chunk_utils import *
import struct
import knownbonenames

bone_field_defs = [
    FieldDef("m_nControllerID", "I", knownbonenames.getBoneInfoByCrc32),
    FieldDef("m_PhysInfo[0].nPhysGeom", "i"),
    FlagsDef(
        "m_PhysInfo[0].flags",
        "I",
        [
            "angle0_locked",
            "angle1_locked",
            "angle2_locked",
            "angle0_limit_reached",
            "angle1_limit_reached",
            "angle2_limit_reached",
            "angle0_auto_kd",
            "angle1_auto_kd",
            "angle2_auto_kd",
            "joint_no_gravity",
            "joint_isolated_accelerations",
            "joint_expand_hinge",
            "angle0_gimbal_locked",
            "angle1_gimbal_locked",
            "angle2_gimbal_locked",
            "joint_dashpot_reached",
            "joint_ignore_impulses",
        ],
    ),
    FieldDef("m_PhysInfo[0].min", "3f"),
    FieldDef("m_PhysInfo[0].max", "3f"),
    FieldDef("m_PhysInfo[0].spring_angle", "3f"),
    FieldDef("m_PhysInfo[0].spring_tension", "3f"),
    FieldDef("m_PhysInfo[0].damping", "3f"),
    FieldDef("m_PhysInfo[0].framemtx[0]", "3f"),
    FieldDef("m_PhysInfo[0].framemtx[1]", "3f"),
    FieldDef("m_PhysInfo[0].framemtx[2]", "3f"),
    FieldDef("m_PhysInfo[1].nPhysGeom", "i"),
    FlagsDef(
        "m_PhysInfo[1].flags",
        "I",
        [
            "angle0_locked",
            "angle1_locked",
            "angle2_locked",
            "angle0_limit_reached",
            "angle1_limit_reached",
            "angle2_limit_reached",
            "angle0_auto_kd",
            "angle1_auto_kd",
            "angle2_auto_kd",
            "joint_no_gravity",
            "joint_isolated_accelerations",
            "joint_expand_hinge",
            "angle0_gimbal_locked",
            "angle1_gimbal_locked",
            "angle2_gimbal_locked",
            "joint_dashpot_reached",
            "joint_ignore_impulses",
        ],
    ),
    FieldDef("m_PhysInfo[1].min", "3f"),
    FieldDef("m_PhysInfo[1].max", "3f"),
    FieldDef("m_PhysInfo[1].spring_angle", "3f"),
    FieldDef("m_PhysInfo[1].spring_tension", "3f"),
    FieldDef("m_PhysInfo[1].damping", "3f"),
    FieldDef("m_PhysInfo[1].framemtx[0]", "3f"),
    FieldDef("m_PhysInfo[1].framemtx[1]", "3f"),
    FieldDef("m_PhysInfo[1].framemtx[2]", "3f"),
    FieldDef("m_fMass", "f"),
    FieldDef("m_DefaultW2B[0]", "4f"),
    FieldDef("m_DefaultW2B[1]", "4f"),
    FieldDef("m_DefaultW2B[2]", "4f"),
    FieldDef("m_DefaultB2W[0]", "4f"),
    FieldDef("m_DefaultB2W[1]", "4f"),
    FieldDef("m_DefaultB2W[2]", "4f"),
    FieldDef("m_arrBoneName", "256s", null_termin),
    FieldDef("m_nLimbId", "i"),
    FieldDef("m_nOffsetParent", "i"),
    FieldDef("m_numChildren", "I"),
    FieldDef("m_nOffsetChildren", "i"),
]


class CompiledBonesChunk(Chunk):

    def format(self, pos):
        if self.version != 2048:
            raise VersionError
        reader = DataReader(self.data)
        header_field_defs = []
        if not self.withoutheader:
            add_chunk_header_fields(header_field_defs)
        header_field_defs.extend((FieldDef("reserved", "32s", hex_dump),))
        header = read_fields("", self.bigendian, header_field_defs, reader)
        header.format(pos)
        num_bones = (
            len(self.data) - get_fields_size(header_field_defs)
        ) / get_fields_size(bone_field_defs)
        for bone_index in xrange(num_bones):
            self.read_bone(reader, bone_index).format(pos)

    def read_bone(self, reader, bone_index):
        return read_fields(
            "Bone Name (%d)" % bone_index, self.bigendian, bone_field_defs, reader
        )
