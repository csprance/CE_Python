# Chris Sprance
# Look For textures with /ser=1 Supress Engine Reduce Checked on (This is BAD!!!!)
from __future__ import print_function
# This is our library for reading image metadata
# https://github.com/bendavis78/pyexiv2
import pyexiv2
import os
import re


# return raw values from a tag
def retraw(img):
	# Load the image into the metadata
	metadata = pyexiv2.ImageMetadata(img)

	# Read the metadata from our image
	metadata.read()

	# read the iptc_keys out
	metadata.iptc_keys

	# some stuff doesn't have metadata for whatever reason ()
	try:
	# set the tag 
		tag = metadata['Iptc.Application2.SpecialInstructions']
		#set up our regex
		regex = re.findall(r'\/ser=1',tag._raw_values[0])
		# if regex is true it will return back a value so check that and then return
		if regex:
			print(img,tag._raw_values[0])
			#extract the data from the tag and return it and the i mage path in a tuple
	except:
		# just fugettahboutit
		return

# main 
def main():
	# recurse through all directors only finding files with .tif
	for root, dirs, files in os.walk("d:/perforce/gamesdk/objects"):
		for file in files:
			if file.endswith(".tif"):
				retraw(os.path.join(root, file))

# run the shizzle
if __name__ == '__main__':
	main()