#Embedded file name: chunkfile\controller_chunk.pyc
from chunk import Chunk, VersionError, DataReader
from chunk_utils import *
import struct
import math
import knownbonenames

def readHeader827(self, reader):
    field_defs = [FieldDef('numKeys', 'i'), FieldDef('nControllerId', 'I', knownbonenames.getBoneInfoByCrc32)]
    return read_fields('', self.bigendian, field_defs, reader)


def readHeader826(self, reader, type_strings):
    field_defs = []
    if not self.withoutheader:
        add_chunk_header_fields(field_defs)
    field_defs.extend((EnumDef('type', 'i', type_strings),
     FieldDef('nKeys', 'i'),
     FlagsDef('flags', 'I', ['CTRL_ORT_CYCLE', 'CTRL_ORT_LOOP']),
     FieldDef('nControllerId', 'I', knownbonenames.getBoneInfoByCrc32)))
    return read_fields('', self.bigendian, field_defs, reader)


def readCryKeyPos(self, reader, index):
    field_defs = [FieldDef('vPos', '3f')]
    return read_fields('CryKeyPos (%d)' % index, self.bigendian, field_defs, reader)


def readCryKeyPQLog(self, reader, index):
    field_defs = [FieldDef('nTime', 'i'), FieldDef('vPos', '3f'), FieldDef('vRotLog', '3f')]
    return read_fields('CryKeyPQLog (%d)' % index, self.bigendian, field_defs, reader)


def formatController826(self, pos):
    typeDefEntries = [('CTRL_NONE', None),
     ('CTRL_CRYBONE', None),
     ('CTRL_LINEER1', None),
     ('CTRL_LINEER3', None),
     ('CTRL_LINEERQ ', None),
     ('CTRL_BEZIER1', None),
     ('CTRL_BEZIER3', None),
     ('CTRL_BEZIERQ', None),
     ('CTRL_TCB1', None),
     ('CTRL_TCB3', ('TCB3', [FieldDef('time', 'i'),
        FieldDef('BaseKey3', '3f'),
        FieldDef('t', 'f'),
        FieldDef('c', 'f'),
        FieldDef('b', 'f'),
        FieldDef('ein', 'f'),
        FieldDef('eout', 'f')])),
     ('CTRL_TCBQ', ('TCBQ', [FieldDef('time', 'i'),
        FieldDef('BasekeyQ', '4f'),
        FieldDef('t', 'f'),
        FieldDef('c', 'f'),
        FieldDef('b', 'f'),
        FieldDef('ein', 'f'),
        FieldDef('eout', 'f')])),
     ('CTRL_BSPLINE_2O', None),
     ('CTRL_BSPLINE_1O', None),
     ('CTRL_BSPLINE_2C', None),
     ('CTRL_BSPLINE_1C', None)]
    typeDefs = dict(typeDefEntries)
    reader = DataReader(self.data)
    header = readHeader826(self, reader, [ x for x, y in typeDefEntries ])
    header.format(pos)
    typeString = header.find_field('type').get_enum_string()
    if typeString in typeDefs and typeDefs[typeString]:
        keyHeader, fieldDefs = typeDefs[typeString]
        count = header.find_field('nKeys').value
        for key in xrange(count):
            read_fields('%s (%d)' % (keyHeader, key), self.bigendian, fieldDefs, reader).format(pos)


def formatController827(self, pos):
    reader = DataReader(self.data)
    header = readHeader827(self, reader)
    header.format(pos)
    elementCount = header.find_field('numKeys').value
    for i in xrange(elementCount):
        readCryKeyPQLog(self, reader, i).format(pos)


def readHeader829(self, reader):
    field_defs = []
    if not self.withoutheader:
        add_chunk_header_fields(field_defs)
    field_defs.extend((FieldDef('nControllerId', 'I', knownbonenames.getBoneInfoByCrc32),
     FieldDef('numRotationKeys', 'H'),
     FieldDef('numPositionKeys', 'H'),
     FieldDef('RotationFormat', 'B'),
     FieldDef('RotationTimeFormat', 'B'),
     FieldDef('PositionFormat', 'B'),
     FieldDef('PositionKeysInfo', 'B'),
     FieldDef('PositionTimeFormat', 'B')))
    return read_fields('', self.bigendian, field_defs, reader)


def formatController829(self, pos):
    reader = DataReader(self.data)
    header = readHeader829(self, reader)
    header.format(pos)


def readHeader905(self, reader):
    field_defs = []
    if not self.withoutheader:
        add_chunk_header_fields(field_defs)
    field_defs.extend((FieldDef('numKeyPos', 'I'),
     FieldDef('numKeyRot', 'I'),
     FieldDef('numKeyTime', 'I'),
     FieldDef('numAnims', 'I')))
    return read_fields('', self.bigendian, field_defs, reader)


def formatController905(self, pos):
    reader = DataReader(self.data)
    header = readHeader905(self, reader)
    header.format(pos)
    print 'proper data output is not implemented yet'


formaters = {2086: formatController826,
 2087: formatController827,
 2089: formatController829,
 2309: formatController905}

class ControllerChunk(Chunk):

    def format(self, pos):
        if formaters.has_key(self.version):
            formaters[self.version](self, pos)
        else:
            raise VersionError

    def read_controller_id(self):
        reader = DataReader(self.data)
        if self.version != 2087:
            return None
        header = readHeader827(self, reader)
        return header.find_field('nControllerId').value

    def read_keys(self):
        if self.version == 2087:
            reader = DataReader(self.data)
            header = readHeader827(self, reader)
            elementCount = header.find_field('numKeys').value
            return [ readCryKeyPQLog(self, reader, i) for i in xrange(elementCount) ]
        else:
            return []
