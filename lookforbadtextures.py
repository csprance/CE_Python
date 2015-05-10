# Chris Sprance
# Look For textures with /ser=1 Supress Engine Reduce Checked on (This is
# BAD!!!!)
from __future__ import print_function

from PIL import TiffImagePlugin
import os
import re
import sys


def strip_control_characters(input):

    if input:


        # unicode invalid characters
        RE_XML_ILLEGAL = u'([\u0000-\u0008\u000b-\u000c\u000e-\u001f\ufffe-\uffff])' + \
                         u'|' + \
                         u'([%s-%s][^%s-%s])|([^%s-%s][%s-%s])|([%s-%s]$)|(^[%s-%s])' % \
            (unichr(0xd800), unichr(0xdbff), unichr(0xdc00), unichr(0xdfff),
             unichr(0xd800), unichr(0xdbff), unichr(
                0xdc00), unichr(0xdfff),
             unichr(0xd800), unichr(0xdbff), unichr(
                0xdc00), unichr(0xdfff),
             )
        input = re.sub(RE_XML_ILLEGAL, "", input)

        # ascii control characters
        input = re.sub(r"[\x01-\x1F\x7F]", "", input)

        input = re.sub(r"(8BIM...)", "", input)

    return input

# return raw values from a tag


def retraw(img):
    # Load the image into the metadata
    # grab the iptc data

    # some stuff doesn't have metadata for whatever reason ()
    try:
        im = TiffImagePlugin.TiffImageFile(img)
        # set up our regex
        iptc = im.tag.tagdata[TiffImagePlugin.PHOTOSHOP_CHUNK]
        regex = re.findall(r'\/ser=1', iptc)
        # if regex is true it will return back a value so check that and then
        # return
        if regex:
            print(img, strip_control_characters(iptc))
            # extract the data from the tag and return it and the i mage path
            # in a tuple
    except:
        # just fugettahboutit
        return

# main


def main():
    # recurse through all directors only finding files with .tif
    if len(sys.argv) > 1:
    	directory = sys.argv[1]
    else:
    	directory = "d:/perforce/gamesdk/textures"
    	pass
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".tif"):
                retraw(os.path.join(root, file))

# run the shizzle
if __name__ == '__main__':
    main()
