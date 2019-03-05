# Embedded file name: chunkfile\compiled_physical_bones_chunk.pyc
from chunk import Chunk, VersionError, DataReader
from chunk_utils import *
import binascii
import struct
import knownbonenames

bone_entity_field_defs = [
    FieldDef("BoneID", "i"),
    FieldDef("ParentID", "i"),
    FieldDef("nChildren", "i"),
    FieldDef("ControllerID", "I", knownbonenames.getBoneInfoByCrc32),
    FieldDef("prop", "32s", null_termin),
    FieldDef("phys.nPhysGeom", "i"),
    FlagsDef(
        "phys.flags",
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
    FieldDef("phys.min", "3f"),
    FieldDef("phys.max", "3f"),
    FieldDef("phys.spring_angle", "3f"),
    FieldDef("phys.spring_tension", "3f"),
    FieldDef("phys.damping", "3f"),
    FieldDef("phys.framemtx[0]", "3f"),
    FieldDef("phys.framemtx[1]", "3f"),
    FieldDef("phys.framemtx[2]", "3f"),
]


class CompiledPhysicalBonesChunk(Chunk):

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
        ) / get_fields_size(bone_entity_field_defs)
        for bone_index in xrange(num_bones):
            self.read_bone_entity(reader, bone_index).format(pos)

    def read_bone_entity(self, reader, index):
        return read_fields(
            "BONE_ENTITY (%d)" % index, self.bigendian, bone_entity_field_defs, reader
        )
