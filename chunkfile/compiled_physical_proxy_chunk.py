#Embedded file name: chunkfile\compiled_physical_proxy_chunk.pyc
from chunk import Chunk, VersionError, DataReader
from chunk_utils import *
import struct

class CompiledPhysicalProxyChunk(Chunk):

    def format(self, pos):
        if self.version != 2048:
            raise VersionError
        reader = DataReader(self.data)
        if not self.withoutheader:
            field_defs = []
            add_chunk_header_fields(field_defs)
            header = read_fields('', self.bigendian, field_defs, reader)
            header.format(pos)
        header = read_fields('', self.bigendian, (FieldDef('numPhysicalProxies', 'I'),), reader)
        header.format(pos)
        num_proxies = header.find_field('numPhysicalProxies').value
        if self.bigendian and num_proxies > 65535:
            num_proxies = ((num_proxies >> 0 & 255) << 24) + ((num_proxies >> 8 & 255) << 16) + ((num_proxies >> 16 & 255) << 8) + ((num_proxies >> 24 & 255) << 0)
            print 'Converting old broken little-endian numPhysicalProxies to big-endian: numPhysicalProxies = {0}'.format(num_proxies)
        for proxy_index in xrange(num_proxies):
            proxy_header = self.read_proxy_header(reader, proxy_index)
            proxy_header.format(pos)
            num_points = proxy_header.find_field('numPoints').value
            for point_index in xrange(num_points):
                self.read_point(reader, point_index).format(pos)

            num_indices = proxy_header.find_field('numIndices').value
            for index_index in xrange(num_indices):
                self.read_index(reader, index_index).format(pos)

            num_materials = proxy_header.find_field('numMaterials').value
            for material_index in xrange(num_materials):
                self.read_material(reader, material_index).format(pos)

    def read_proxy_header(self, reader, index):
        field_defs = [FieldDef('ChunkID', 'I'),
         FieldDef('numPoints', 'I'),
         FieldDef('numIndices', 'I'),
         FieldDef('numMaterials', 'I')]
        return read_fields('SMeshPhysicalProxyHeader[%d]' % index, self.bigendian, field_defs, reader)

    def read_point(self, reader, index):
        return read_fields(None, self.bigendian, [FieldDef('pos[{0}]'.format(index), '3f')], reader)

    def read_index(self, reader, index):
        return read_fields(None, self.bigendian, [FieldDef('index[{0}]'.format(index), 'H')], reader)

    def read_material(self, reader, index):
        return read_fields(None, self.bigendian, [FieldDef('material[{0}]'.format(index), 'B')], reader)
