#Embedded file name: chunkfile\mesh_physics_data_chunk.pyc
from chunk import Chunk, VersionError, DataReader
from chunk_utils import *
import struct
geom_types = [('GEOM_TRIMESH', 1, 'format_trimesh_primitive_data'),
 ('GEOM_HEIGHTFIELD', 2, None),
 ('GEOM_CYLINDER', 5, None),
 ('GEOM_CAPSULE', 6, None),
 ('GEOM_RAY', 3, None),
 ('GEOM_SPHERE', 4, None),
 ('GEOM_BOX', 0, 'format_box_primitive_data'),
 ('GEOM_VOXELGRID', 7, None)]
bv_tree_types = [('BVT_OBB', 0, 'format_trimesh_obb_tree'),
 ('BVT_AABB', 1, 'format_trimesh_aabb_tree'),
 ('BVT_SINGLEBOX', 2, 'format_trimesh_box_tree'),
 ('BVT_RAY', 3, None),
 ('BVT_HEIGHTFIELD', 4, None),
 ('BVT_VOXEL', 5, None)]
mesh_flag_names = ['mesh_shared_vtx',
 'mesh_shared_idx',
 'mesh_shared_mats',
 'mesh_shared_foreign_idx',
 'mesh_shared_normals',
 'mesh_OBB',
 'mesh_AABB',
 'mesh_SingleBB',
 'mesh_multicontact0',
 'mesh_multicontact1',
 'mesh_multicontact2',
 'mesh_approx_cylinder0',
 'mesh_approx_box',
 'mesh_approx_sphere ',
 'mesh_AABB_plane_optimise',
 'mesh_keep_vtxmap',
 'mesh_keep_vtxmap_for_saving',
 'mesh_no_vtx_merge',
 'mesh_AABB_rotated',
 'mesh_VoxelGrid',
 'mesh_always_static',
 'mesh_approx_capsule',
 'mesh_full_serialization',
 'mesh_transient',
 'mesh_no_booleans',
 'mesh_no_filter']

def has_mesh_flag(flags, name):
    return flags & 1 << mesh_flag_names.index(name) != 0


class MeshPhysicsDataChunk(Chunk):

    def format(self, pos):
        if self.version != 2048:
            raise VersionError
        reader = DataReader(self.data)
        header = self.read_header(reader)
        header.format(pos)
        data_length = header.find_field('nDataSize').value
        physics_data_header = self.read_physics_data(reader, data_length)
        physics_data_header.format(pos)
        geom_type = physics_data_header.find_field('GeomType').get_enum_string()
        geom_readers = dict([ (name, func) for name, index, func in geom_types ])
        if geom_type in geom_readers:
            func = geom_readers[geom_type]
            if func:
                getattr(self, func)(reader, pos)
            else:
                print '<PARSER FOR THIS GEOM TYPE IS NOT IMPLEMENTED>'
        else:
            print '<INVALID GEOM TYPE>'

    def read_header(self, reader):
        field_defs = []
        if not self.withoutheader:
            add_chunk_header_fields(field_defs)
        field_defs.extend((FieldDef('nDataSize', 'i'),
         FieldDef('nFlags (unused)', 'i', hex),
         FieldDef('nTetraHedraDataSize', 'i'),
         FieldDef('nTetreHedraChunkId', 'i'),
         FieldDef('reserved', '2i')))
        return read_fields('', self.bigendian, field_defs, reader)

    def read_physics_data(self, reader, length):
        physics_types = dict([ (index, name) for name, index, func in geom_types ])
        field_defs = [FieldDef('version', 'i'),
         FieldDef('dummy0', 'i'),
         FieldDef('Ibody', '3f'),
         FieldDef('q', '4f'),
         FieldDef('origin', '3f'),
         FieldDef('V', 'f'),
         FieldDef('nRefCount', 'i'),
         FieldDef('surface_idx', 'i'),
         FieldDef('dummy1', 'i'),
         FieldDef('nMats', 'i'),
         EnumDef('GeomType', 'i', physics_types)]
        return read_fields('Physics Data', False, field_defs, reader)

    def format_box_primitive_data(self, reader, pos):
        box_size = reader.get_remaining_size()
        self.read_box(reader, 'm_Tree.m_Box').format(pos)
        box_size -= reader.get_remaining_size()
        if reader.get_remaining_size() > box_size:
            self.read_box(reader, 'box (old format, obsolete)').format(pos)
        self.read_prims_count(reader).format(pos)

    def read_prims_count(self, reader):
        field_defs = [FieldDef('m_nPrims', 'i')]
        return read_fields('m_Tree prims count', False, field_defs, reader)

    def read_box(self, reader, title):
        field_defs = [FieldDef('Basis[0]', '3f'),
         FieldDef('Basis[1]', '3f'),
         FieldDef('Basis[2]', '3f'),
         FieldDef('bOriented', 'i'),
         FieldDef('center', '3f'),
         FieldDef('size', '3f')]
        return read_fields(title, False, field_defs, reader)

    def format_trimesh_primitive_data(self, reader, pos):
        header = self.read_trimesh_primitive_header(reader)
        header.format(pos)
        num_vertices = header.find_field('m_nVertices').value
        num_tris = header.find_field('m_nTris').value
        mesh_flags = header.find_field('m_flags').value
        has_vertex_map_header = self.read_trimesh_has_vertex_map_flag(reader)
        has_vertex_map_header.format(pos)
        b_vertex_map = has_vertex_map_header.find_field('bVtxMap').value
        if b_vertex_map:
            for index in xrange(num_vertices):
                self.read_vertex_map_element(reader, index).format(pos)

        has_foreign_idx_header = self.read_trimesh_has_foreign_indices_flag(reader)
        has_foreign_idx_header.format(pos)
        b_foreign_idx = has_foreign_idx_header.find_field('bForeignIdx').value
        if b_foreign_idx and not has_mesh_flag(mesh_flags, 'mesh_full_serialization'):
            for index in xrange(num_tris):
                self.read_foreign_idx(reader, index).format(pos)

        else:
            if b_foreign_idx:
                for index in xrange(num_tris):
                    self.read_foreign_idx(reader, index).format(pos)

            if not has_mesh_flag(mesh_flags, 'mesh_shared_vtx'):
                for index in xrange(num_vertices):
                    self.read_vertex(reader, index).format(pos)

            for index in xrange(num_tris):
                self.read_triangle_indices(reader, index).format(pos)

            has_ids_header = self.read_trimesh_has_ids_flag(reader)
            has_ids_header.format(pos)
            if has_ids_header.find_field('bIds').value:
                for index in xrange(num_tris):
                    self.read_trimesh_id(reader, index).format(pos)

        self.read_trimesh_dummy(reader).format(pos)
        i_header = self.read_trimesh_i_flag(reader)
        i_header.format(pos)
        if i_header.find_field('I').value:
            return
        for index in xrange(4):
            self.read_trimesh_convexity(reader, index).format(pos)

        tree_type_header = self.read_trimesh_tree_type_header(reader)
        tree_type_header.format(pos)
        tree_type = tree_type_header.find_field('Trimesh Tree Type').get_enum_string()
        tree_funcs = dict([ (name, func) for name, index, func in bv_tree_types ])
        if tree_type in tree_funcs:
            func = tree_funcs[tree_type]
            if func:
                getattr(self, func)(reader, pos)
            else:
                print '<TREE TYPE PARSER IS NOT IMPLEMENTED YET>'
        else:
            print '<UNKNOWN TREE TYPE>: ' + tree_type

    def read_trimesh_primitive_header(self, reader):
        field_defs = [FieldDef('m_nVertices', 'i'),
         FieldDef('m_nTris', 'i'),
         FieldDef('m_nMaxVertexValency', 'i'),
         FlagsDef('m_flags', 'I', mesh_flag_names)]
        return read_fields('Trimesh Primitive', False, field_defs, reader)

    def read_trimesh_has_vertex_map_flag(self, reader):
        field_defs = [FieldDef('bVtxMap', 'B')]
        return read_fields('HasVertexMap', False, field_defs, reader)

    def read_trimesh_has_foreign_indices_flag(self, reader):
        field_defs = [FieldDef('bForeignIdx', 'B')]
        return read_fields('HasForeignIdx', False, field_defs, reader)

    def read_vertex_map_element(self, reader, index):
        field_defs = [FieldDef('Vertex Map Element [{0}]'.format(index), 'H')]
        return read_fields(None, False, field_defs, reader)

    def read_foreign_idx(self, reader, index):
        field_defs = [FieldDef('Foreign Idx [{0}]'.format(index), 'H')]
        return read_fields(None, False, field_defs, reader)

    def read_vertex(self, reader, index):
        field_defs = [FieldDef('Vertex[{0}]'.format(index), '3f')]
        return read_fields(None, False, field_defs, reader)

    def read_triangle_indices(self, reader, index):
        field_defs = [FieldDef('Triangle Indices [{0}]'.format(index), '3H')]
        return read_fields(None, False, field_defs, reader)

    def read_trimesh_has_ids_flag(self, reader):
        field_defs = [FieldDef('bIds', 'B')]
        return read_fields('HasIds', False, field_defs, reader)

    def read_trimesh_id(self, reader, index):
        field_defs = [FieldDef('Id [{0}]'.format(index), 'B')]
        return read_fields(None, False, field_defs, reader)

    def read_trimesh_dummy(self, reader):
        field_defs = [FieldDef('dummy', '4i')]
        return read_fields('Dummy', False, field_defs, reader)

    def read_trimesh_i_flag(self, reader):
        field_defs = [FieldDef('I', 'i')]
        return read_fields(None, False, field_defs, reader)

    def read_trimesh_convexity(self, reader, index):
        field_defs = [FieldDef('m_bConvex[{0}]'.format(index), 'i'), FieldDef('m_ConvexityTolerance[{0}]'.format(index), 'f')]
        return read_fields(None, False, field_defs, reader)

    def read_trimesh_tree_type_header(self, reader):
        bv_enum_defs = dict([ (index, name) for name, index, func in bv_tree_types ])
        field_defs = [EnumDef('Trimesh Tree Type', 'i', bv_enum_defs)]
        return read_fields(None, False, field_defs, reader)

    def format_trimesh_box_tree(self, reader, pos):
        self.read_box(reader, 'm_Box').format(pos)
        self.read_prims_count(reader).format(pos)

    def read_num_nodes(self, reader):
        field_defs = [FieldDef('m_nNodes', 'i')]
        return read_fields('Num Nodes', False, field_defs, reader)

    def format_trimesh_obb_tree(self, reader, pos):
        num_nodes_header = self.read_num_nodes(reader)
        num_nodes_header.format(pos)
        num_nodes = num_nodes_header.find_field('m_nNodes').value
        for index in xrange(num_nodes):
            self.read_obb_node(reader, index).format(pos)

        self.read_obb_data(reader).format(pos)

    def read_obb_node(self, reader, index):
        field_defs = [FieldDef('axes[0]', '3f'),
         FieldDef('axes[1]', '3f'),
         FieldDef('axes[2]', '3f'),
         FieldDef('center', '3f'),
         FieldDef('size', '3f'),
         FieldDef('iparent', 'i'),
         FieldDef('ichild', 'i'),
         FieldDef('ntris', 'i')]
        return read_fields('OBB Node (%d)' % index, False, field_defs, reader)

    def read_obb_data(self, reader):
        field_defs = [FieldDef('m_nMaxTrisInNode', 'i'),
         FieldDef('m_nMinTrisPerNode', 'i'),
         FieldDef('m_nMaxTrisPerNode', 'i'),
         FieldDef('m_maxSkipDim', 'f')]
        return read_fields('OBB Data', False, field_defs, reader)

    def format_trimesh_aabb_tree(self, reader, pos):
        version_header = self.read_aabb_tree_version(reader)
        version_header.format(pos)
        version = version_header.find_field('ver').value
        if version >= 0:
            num_nodes = version
        else:
            num_nodes_header = self.read_num_nodes(reader)
            num_nodes_header.format(pos)
            num_nodes = num_nodes_header.find_field('m_nNodes').value
        if version == -1:
            for index in xrange(num_nodes):
                self.read_aabb_node(reader, index).format(pos)

        elif version >= 0:
            print '<AABB TREE VERSION NOT SUPPORTED>'
            return
        self.read_aabb_data(reader).format(pos)

    def read_aabb_tree_version(self, reader):
        field_defs = [FieldDef('ver', 'i')]
        return read_fields('AABB Tree Version', False, field_defs, reader)

    def read_aabb_node(self, reader, index):
        field_defs = [FieldDef('ichild', 'i'),
         FieldDef('minx', 'B'),
         FieldDef('maxx', 'B'),
         FieldDef('miny', 'B'),
         FieldDef('maxy', 'B'),
         FieldDef('minz', 'B'),
         FieldDef('maxz', 'B'),
         FieldDef('ntris', 'B'),
         FieldDef('bSingleColl', 'B')]
        return read_fields('AABB Node (%d)' % index, False, field_defs, reader)

    def read_aabb_data(self, reader):
        field_defs = [FieldDef('m_center', '3f'),
         FieldDef('m_size', '3f'),
         FieldDef('m_Basis[0]', '3f'),
         FieldDef('m_Basis[1]', '3f'),
         FieldDef('m_Basis[2]', '3f'),
         FieldDef('m_nMaxTrisInNode', 'i'),
         FieldDef('m_nMinTrisPerNode', 'i'),
         FieldDef('m_nMaxTrisPerNode', 'i'),
         FieldDef('m_maxSkipDim', 'f')]
        return read_fields('AABB Data', False, field_defs, reader)
