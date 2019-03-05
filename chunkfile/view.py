#Embedded file name: chunkfile\view.pyc
import chunkfile
from chunk import VersionError

def view_chunk(chunk, pos):
    print '%s' % chunk.name
    print ''
    print 'id = 0x%.4X (%d)' % (chunk.id, chunk.id)
    print 'type = 0x%.8X' % chunk.typecode
    print 'pos = 0x%.8X (%d)' % (pos, pos)
    print 'version = 0x%.4X' % chunk.version
    print 'size = 0x%.8X (%d)' % (chunk.size, chunk.size)
    print 'endianness = {0}'.format(['little-endian', 'big-endian'][chunk.bigendian])
    print ''
    if hasattr(chunk, 'format'):
        try:
            chunk.format(pos)
        except VersionError:
            print '<CHUNK VERSION NOT UNDERSTOOD>'

    else:
        print '<CHUNK NOT UNDERSTOOD>'


def view_chunk_by_id(filename, chunk_id):
    chunk_file = chunkfile.load_chunk_file(filename)
    try:
        pos, chunk = chunk_file.get_chunk(chunk_id)
    except chunkfile.IDError:
        print 'Invalid chunk id.'
    except:
        print 'Unknown error.'
    else:
        view_chunk(chunk, pos)
