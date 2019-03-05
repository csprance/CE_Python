#Embedded file name: chunkfile\source_info_chunk.pyc
from chunk import Chunk, VersionError, DataReader
from chunk_utils import *

def read_string(reader):
    result = ''
    while True:
        try:
            c = reader.read(1)
        except:
            break

        if c == '\x00':
            break
        result += c

    return result


class SourceInfoChunk(Chunk):

    def format(self, pos):
        reader = DataReader(self.data)
        sourcefilename = read_string(reader)
        datetime = read_string(reader)
        user = ''
        host = ''
        if datetime.endswith('\n'):
            datetime = datetime[:-1]
            user, host = read_string(reader).split('@')
        else:
            datetime, user = datetime.split('\n')
            user, host = user.split('@')
        print "sourcefilename = '%s'" % sourcefilename
        print "datetime = '%s'" % datetime
        print "user = '%s'" % user
        print "host = '%s'" % host

    def get_source_filename(self):
        return self.get_info()[0]

    def get_date_time(self):
        return self.get_info()[1]

    def get_user(self):
        return self.get_info()[2]

    def get_host(self):
        return self.get_info()[3]

    def get_info(self):
        reader = DataReader(self.data)
        sourcefilename = read_string(reader)
        datetime = read_string(reader)
        user = ''
        host = ''
        if datetime.endswith('\n'):
            datetime = datetime[:-1]
            user, host = read_string(reader).split('@')
        else:
            datetime, user = datetime.split('\n')
            user, host = user.split('@')
        return (sourcefilename,
         datetime,
         user,
         host)
