#Embedded file name: chunkfile\node_chunk.pyc
from chunk import Chunk, VersionError, DataReader
from chunk_utils import *
import struct

class NodeChunk(Chunk):

    def format(self, pos):
        if self.version == 2083 or self.version == 2084:
            reader = DataReader(self.data)
            header = self.read_header(reader)
            header.format(pos)
            prop_str_len = header.find_field('PropStrLen').value
            prop_str = reader.read(prop_str_len)
            print prop_str
        else:
            raise VersionError

    def get_props(self):
        reader = DataReader(self.data)
        header = self.read_header(reader)
        prop_str_len = header.find_field('PropStrLen').value
        prop_str = reader.read(prop_str_len)
        return prop_str

    def get_node_name(self):
        reader = DataReader(self.data)
        header = self.read_header(reader)
        name = header.find_field('name').value
        return name

    def get_node_pos(self):
        reader = DataReader(self.data)
        header = self.read_header(reader)
        pos = header.find_field('pos').value
        return pos

    def read_header(self, reader):
        field_defs = []
        if not self.withoutheader:
            add_chunk_header_fields(field_defs)
        field_defs.extend((FieldDef('name', '64s', strz_add_quotes),
         FieldDef('ObjectID', 'i'),
         FieldDef('ParentID', 'i'),
         FieldDef('nChildren', 'i'),
         FieldDef('MatID', 'i')))
        if self.version == 2083:
            field_defs.extend((FieldDef('IsGroupHead', 'b'), FieldDef('IsGroupMember', 'b'), FieldDef('_padding_', '2B', hex_dump)))
        else:
            field_defs.extend((FieldDef('_obsoleteA_', '4b'),))
        field_defs.extend((FieldDef('tm[0]', '4f'),
         FieldDef('tm[1]', '4f'),
         FieldDef('tm[2]', '4f'),
         FieldDef('tm[3]', '4f')))
        if self.version == 2083:
            field_defs.extend((FieldDef('pos', '3f'), FieldDef('rot', '4f'), FieldDef('scl', '3f')))
        else:
            field_defs.extend((FieldDef('_obsoleteB_', '3f'), FieldDef('_obsoleteC_', '4f'), FieldDef('_obsoleteD_', '3f')))
        field_defs.extend((FieldDef('pos_cont_id', 'i'),
         FieldDef('rot_cont_id', 'i'),
         FieldDef('scl_cont_id', 'i'),
         FieldDef('PropStrLen', 'i')))
        return read_fields('', self.bigendian, field_defs, reader)

    def read_bone(self, reader, bone_index):
        field_defs = [FieldDef('transform row 1', '3f'),
         FieldDef('transform row 2', '3f'),
         FieldDef('transform row 3', '3f'),
         FieldDef('transform row 4', '3f')]
        return read_fields('Bone Initial Transform (%d)' % bone_index, self.bigendian, field_defs, reader)
