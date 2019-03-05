# Embedded file name: chunkfile\bone_anim_chunk.pyc
from chunk import Chunk, VersionError, DataReader
from chunk_utils import *
import struct
import knownbonenames


class BoneAnimChunk(Chunk):

    def format(self, pos):
        if self.version != 656:
            raise VersionError
        reader = DataReader(self.data)
        header = self.read_header(reader)
        header.format(pos)
        num_bones = header.find_field("nBones").value
        for bone_index in xrange(num_bones):
            self.read_bone(reader, bone_index).format(pos)

    def read_header(self, reader):
        field_defs = []
        if not self.withoutheader:
            add_chunk_header_fields(field_defs)
        field_defs.extend((FieldDef("nBones", "i"),))
        return read_fields("", self.bigendian, field_defs, reader)

    def read_bone(self, reader, bone_index):
        field_defs = [
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
        return read_fields(
            "Bone Entity (%d)" % bone_index, self.bigendian, field_defs, reader
        )
