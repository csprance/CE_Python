#Embedded file name: chunkfile\chunks.pyc
from chunk import Chunk, UnknownChunkError
import bone_anim_chunk
import bone_initial_pos_chunk
import bone_mesh_chunk
import bone_name_list_chunk
import breakable_physics_chunk
import compiled_bone_boxes_chunk
import compiled_bones_chunk
import compiled_ext2int_map_chunk
import compiled_int_faces_chunk
import compiled_int_skin_vertices_chunk
import compiled_morph_targets_chunk
import compiled_physical_bones_chunk
import compiled_physical_proxy_chunk
import controller_chunk
import datastream_chunk
import export_flags_chunk
import foliage_info_chunk
import global_animation_header_caf_chunk
import global_animation_header_aim_chunk
import helper_chunk
import knownbonenames
import mesh_chunk
import mesh_physics_data_chunk
import mesh_subsets_chunk
import morph_target_chunk
import motion_parameters_chunk
import mtl_name_chunk
import node_chunk
import source_info_chunk
import scene_props_chunk
import timing_chunk
chunk_types = (('Mesh', 3435921408L, 4096L),
 ('Helper', 3435921409L, 4097L),
 ('VertAnim', 3435921410L, 4098L),
 ('BoneAnim', 3435921411L, 4099L),
 ('GeomNameList', 3435921412L, 4100L),
 ('BoneNameList', 3435921413L, 4101L),
 ('MtlList', 3435921414L, 4102L),
 ('MRM', 3435921415L, 4103L),
 ('SceneProps', 3435921416L, 4104L),
 ('Light', 3435921417L, 4105L),
 ('PatchMesh', 3435921418L, 4106L),
 ('Node', 3435921419L, 4107L),
 ('Mtl', 3435921420L, 4108L),
 ('Controller', 3435921421L, 4109L),
 ('Timing', 3435921422L, 4110L),
 ('BoneMesh', 3435921423L, 4111L),
 ('BoneLightBinding', 3435921424L, 4112L),
 ('MorphTarget', 3435921425L, 4113L),
 ('BoneInitialPos', 3435921426L, 4114L),
 ('SourceInfo', 3435921427L, 4115L),
 ('MtlName', 3435921428L, 4116L),
 ('ExportFlags', 3435921429L, 4117L),
 ('DataStream', 3435921430L, 4118L),
 ('MeshSubsets', 3435921431L, 4119L),
 ('MeshPhysicsData', 3435921432L, 4120L),
 ('CompiledBones', 2900099072L, 8192L),
 ('CompiledPhysicalBones', 2900099073L, 8193L),
 ('CompiledMorphTargets', 2900099074L, 8194L),
 ('CompiledPhysicalProxy', 2900099075L, 8195L),
 ('CompiledIntFaces', 2900099076L, 8196L),
 ('CompiledIntSkinVertices', 2900099077L, 8197L),
 ('CompiledExt2intMap', 2900099078L, 8198L),
 ('BreakablePhysics', 2868641792L, 12288L),
 ('FaceMap', 2868641793L, 12289L),
 ('MotionParameters', 2868641794L, 12290L),
 ('ChunkType_FootPlantInfo', 2868641795L, 12291L),
 ('CompiledBoneBoxes', 2868641796L, 12292L),
 ('FoliageInfo', 2868641797L, 12293L),
 ('Timestamp', 2868641798L, 12294L),
 ('GlobalAnimationHeaderAim', 2868641800L, 12296L),
 ('GlobalAnimationHeaderCaf', 2868641799L, 12295L))

def get_possible_chunk_module_names(name):
    word_starts = []
    if not name or not name[0].isupper():
        word_starts.append(0)
    word_starts.extend([ i for i in xrange(len(name)) if name[i].isupper() ])
    word_starts.append(len(name))
    tmp = ''
    for i in xrange(len(word_starts) - 1):
        tmp += name[word_starts[i]:word_starts[i + 1]].lower()
        tmp += '_'

    return ('chunkfile.' + tmp + 'chunk', 'chunkfile.' + name.lower() + '_chunk')


import importlib

def get_chunk_class(name):
    class_name = name + 'Chunk'
    for module_name in get_possible_chunk_module_names(name):
        try:
            module = importlib.import_module(module_name)
        except ImportError as imperr:
            continue

        attr = getattr(module, class_name)
        if attr:
            return attr


def create_chunk_typecode_to_class_map():
    m = {}
    for ct in chunk_types:
        attr = get_chunk_class(ct[0])
        if attr:
            m[ct[1]] = attr
            m[ct[2]] = attr

    return m


def create_chunk_typecode_to_name_map():
    m = {}
    for ct in chunk_types:
        m[ct[1]] = ct[0]
        m[ct[2]] = ct[0]

    return m


def get_chunk_name_by_typecode(typecode):
    if typecode in chunk_typecode_to_name_map:
        return chunk_typecode_to_name_map[typecode]
    return '[UNKNOWN CHUNK TYPE: 0x%08x]' % typecode


chunk_typecode_to_class_map = create_chunk_typecode_to_class_map()
chunk_typecode_to_name_map = create_chunk_typecode_to_name_map()

def create_chunk(id, typecode, version, bigendian, withoutheader, data):
    name = get_chunk_name_by_typecode(typecode)
    try:
        return chunk_typecode_to_class_map[typecode](name, id, typecode, version, bigendian, withoutheader, data)
    except KeyError as ke:
        return Chunk(name, id, typecode, version, bigendian, withoutheader, data)
