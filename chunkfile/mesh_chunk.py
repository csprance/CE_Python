#Embedded file name: chunkfile\mesh_chunk.pyc
from chunk import Chunk, VersionError, DataReader
from chunk_utils import *
import struct

class MeshChunk(Chunk):

    def format(self, pos):
        if self.version == 2048 or self.version == 2049:
            reader = DataReader(self.data)
            header = self.read_header_801(reader)
            header.format(pos)
        elif self.version == 1860 or self.version == 1861:
            reader = DataReader(self.data)
            header = self.read_header_745(reader)
            header.format(pos)
            has_topology_ids = header.find_field('flags2').flag_set('FLAG2_HAS_TOPOLOGY_IDS')
            num_vertices = header.find_field('nVerts').value
            for vertex_index in xrange(num_vertices):
                self.read_vertex(reader, vertex_index).format(pos)

            num_faces = header.find_field('nFaces').value
            for face_index in xrange(num_faces):
                self.read_face(reader, not has_topology_ids, face_index).format(pos)

            if has_topology_ids:
                for vertex_index in xrange(num_vertices):
                    self.read_topology_id(reader, vertex_index).format(pos)

            num_texverts = header.find_field('nTVerts').value
            if num_texverts:
                for uv_index in xrange(num_texverts):
                    self.read_uv(reader, uv_index).format(pos)

                if not has_topology_ids:
                    for tex_face_index in xrange(num_faces):
                        self.read_tex_face(reader, tex_face_index).format(pos)

            if header.find_field('flags1').flag_set('FLAG1_BONE_INFO'):
                print 'Bone links count: {0} (same as vertex count)'.format(num_vertices)
                for vertex_index in xrange(num_vertices):
                    num_links_object = self.read_num_bone_links(reader, vertex_index)
                    num_links_object.format(pos)
                    num_links = num_links_object.find_field('num_links[{0}]'.format(vertex_index)).value
                    for link_index in xrange(num_links):
                        self.read_bone_link(reader).format(pos)

            if header.find_field('flags2').flag_set('FLAG2_HAS_VERTEX_COLOR'):
                print 'Color count: {0} (same as vertex count)'.format(num_vertices)
                for vertex_index in xrange(num_vertices):
                    self.read_vertex_color(reader, vertex_index).format(pos)

            if header.find_field('flags2').flag_set('FLAG2_HAS_VERTEX_ALPHA'):
                print 'Alpha count: {0} (same as vertex count)'.format(num_vertices)
                for vertex_index in xrange(num_vertices):
                    self.read_alpha(reader, vertex_index).format(pos)

        else:
            raise VersionError

    def read_header_801(self, reader):
        field_defs = []
        if not self.withoutheader:
            add_chunk_header_fields(field_defs)
        field_defs.extend((FlagsDef('flags1', 'I', ['MESH_IS_EMPTY',
          'HAS_TEX_MAPPING_DENSITY',
          'HAS_EXTRA_WEIGHTS',
          'HAS_FACE_AREA']),
         FieldDef('flags2', 'I', hex),
         FieldDef('nVerts', 'i'),
         FieldDef('nIndices', 'i'),
         FieldDef('nSubSets', 'i'),
         FieldDef('nSubsetsChunkId', 'i'),
         FieldDef('nVertAnimID', 'i'),
         FieldDef('nStreamChunkID', '16i'),
         FieldDef('nPhysicsDataChunk', '4i'),
         FieldDef('bboxMin', '3f'),
         FieldDef('bboxMax', '3f'),
         FieldDef('texMappingDensity', 'f'),
         FieldDef('geometricMeanFaceArea', 'f'),
         FieldDef('reserved', '120B', hex_dump)))
        return read_fields('', self.bigendian, field_defs, reader)

    def read_header_745(self, reader):
        field_defs = []
        if not self.withoutheader:
            add_chunk_header_fields(field_defs)
        field_defs.extend((FlagsDef('flags1', 'B', ['FLAG1_BONE_INFO']),
         FlagsDef('flags2', 'B', ['FLAG2_HAS_VERTEX_COLOR', 'FLAG2_HAS_VERTEX_ALPHA', 'FLAG2_HAS_TOPOLOGY_IDS']),
         FieldDef('_padding_', '2B', hex_dump),
         FieldDef('nVerts', 'i'),
         FieldDef('nTVerts', 'i'),
         FieldDef('nFaces', 'i'),
         FieldDef('VertAnimID', 'i')))
        return read_fields('', self.bigendian, field_defs, reader)

    def read_vertex(self, reader, vertex_index):
        field_defs = [FieldDef('position[{0}]'.format(vertex_index), '3f'), FieldDef('normal[{0}]'.format(vertex_index), '3f')]
        return read_fields(None, self.bigendian, field_defs, reader)

    def read_face(self, reader, has_smoothing_group, face_index):
        field_defs = [FieldDef('vert_indices[{0}]'.format(face_index), '3i'), FieldDef('mat_id[{0}]'.format(face_index), 'i')]
        if has_smoothing_group:
            field_defs.append(FieldDef('smoothing_group[{0}]'.format(face_index), 'i'))
        return read_fields(None, self.bigendian, field_defs, reader)

    def read_topology_id(self, reader, vertex_index):
        field_defs = [FieldDef('topology_id[{0}]'.format(vertex_index), 'i')]
        return read_fields(None, self.bigendian, field_defs, reader)

    def read_uv(self, reader, tex_face_index):
        field_defs = [FieldDef('uv[{0}]'.format(tex_face_index), '2f')]
        return read_fields(None, self.bigendian, field_defs, reader)

    def read_tex_face(self, reader, tex_face_index):
        field_defs = [FieldDef('tex_face_vert_indices[{0}]'.format(tex_face_index), '3i')]
        return read_fields(None, self.bigendian, field_defs, reader)

    def read_num_bone_links(self, reader, bone_index):
        field_defs = [FieldDef('num_links[{0}]'.format(bone_index), 'I')]
        return read_fields(None, self.bigendian, field_defs, reader)

    def read_bone_link(self, reader):
        field_defs = [FieldDef('bone_id', 'i'), FieldDef('offset', '3f'), FieldDef('blending', 'f')]
        return read_fields(None, self.bigendian, field_defs, reader)

    def read_vertex_color(self, reader, vertex_index):
        field_defs = [FieldDef('rgb[{0}]'.format(vertex_index), '3B')]
        return read_fields(None, self.bigendian, field_defs, reader)

    def read_alpha(self, reader, vertex_index):
        field_defs = [FieldDef('alpha[{0}]'.format(vertex_index), 'B')]
        return read_fields(None, self.bigendian, field_defs, reader)

    def get_streams_chunk_ids(self):
        reader = DataReader(self.data)
        header = self.read_header_801(reader)
        ids = header.find_field('nStreamChunkID').value
        return ids

    def get_vertex_count(self):
        reader = DataReader(self.data)
        if self.version == 2048 or self.version == 2049:
            header = self.read_header_801(reader)
        elif self.version == 1860 or self.version == 1861:
            header = self.read_header_745(reader)
        return header.find_field('nVerts').value
