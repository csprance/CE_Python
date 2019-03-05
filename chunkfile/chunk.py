# Embedded file name: chunkfile\chunk.pyc


class UnknownChunkError(Exception):
    pass


class VersionError(Exception):
    pass


class Chunk(object):

    def __init__(self, name, id, typecode, version, bigendian, withoutheader, data):
        self.name = name
        self.id = id
        self.typecode = typecode
        self.version = version
        self.bigendian = bigendian
        self.withoutheader = withoutheader
        self.data = data
        self.size = len(data)


class DataReader(object):

    def __init__(self, data):
        self.data = data
        self.position = 0

    def read(self, size):
        value = self.data[self.position : self.position + size]
        self.position += size
        return value

    def get_remaining_size(self):
        return len(self.data) - self.position

    def find(self, string):
        return self.data.find(string, self.position)
