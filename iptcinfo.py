#
# read IPTC info fields from PhotoShop TIFF and JPEG files
#
# by Fredrik Lundh, November 2001
#

import Image
import TiffImagePlugin
import JpegImagePlugin
import IptcImagePlugin
import StringIO


class FakeImage:
    pass


def getiptcinfo(im):
    # extract IPTC data from a PhotoShop JPEG or TIFF file

    data = None

    if isinstance(im, JpegImagePlugin.JpegImageFile):
        # extract the IPTC/NAA resource
        try:
            app = im.app["APP13"]
            if app[:14] == "Photoshop 3.0\x00":
                app = app[14:]
                # parse the image resource block
                offset = 0
                while app[offset:offset + 4] == "8BIM":
                    offset = offset + 4
                    # resource code
                    code = JpegImagePlugin.i16(app, offset)
                    offset = offset + 2
                    # resource name (usually empty)
                    name_len = ord(app[offset])
                    name = app[offset + 1:offset + 1 + name_len]
                    offset = 1 + offset + name_len
                    if offset & 1:
                        offset = offset + 1
                    # resource data block
                    size = JpegImagePlugin.i32(app, offset)
                    offset = offset + 4
                    if code == 0x0404:
                        # 0x0404 contains IPTC/NAA data
                        data = app[offset:offset + size]
                        break
                    offset = offset + size
                    if offset & 1:
                        offset = offset + 1
        except (AttributeError, KeyError):
            pass

    elif isinstance(im, TiffImagePlugin.TiffImageFile):
        # get raw data from the IPTC/NAA tag (PhotoShop tags the data
        # as 4-byte integers, so we cannot use the get method...)
        try:
            type, data = im.tag.tagdata[TiffImagePlugin.IPTC_NAA_CHUNK]
        except (AttributeError, KeyError):
            pass

    if data is None:
        return None  # no properties

    # create an IptcImagePlugin object without initializing it
    im = FakeImage()
    im.__class__ = IptcImagePlugin.IptcImageFile

    # parse the IPTC information chunk
    im.info = {}
    im.fp = StringIO.StringIO(data)

    try:
        im._open()
    except (IndexError, KeyError):
        pass  # expected failure

    return im.info

if __name__ == "__main__":

    import sys

    for file in sys.argv[1:]:
        print file, "..."
        im = Image.open(sys.argv[1])
        info = getiptcinfo(im)
        if info:
            # extract caption
            print "  CAPTION", info.get((2, 120))
            # print all available fields
            for k, v in info.items():
                print "  %s %s" % (k, repr(v))
        else:
            print "  no info"
