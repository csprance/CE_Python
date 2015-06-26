# usr/bin/python
# This accepts a list of textures to go through and perform a batch operation on it's Crytiff IPTC RC instructions then spits out a bat file to run the operation



import tifffile
import re


# batch is a list of textures to check out and create a batch command for
def main():
	batch = ["D:/Perforce/GameSDK/Objects/natural/trees/white_fir/white_fir_leaves_diff.tif",
"D:/Perforce/GameSDK/Objects/natural/vegetation/ground_plants/heather/heather.tif",
"D:/Perforce/GameSDK/Objects/natural/vegetation/ground_plants/heather/heather_ddna.tif",
"D:/Perforce/GameSDK/Objects/natural/vegetation/Ivys/Vines_ddn.tif",
"D:/Perforce/GameSDK/Objects/natural/vegetation/veg_ivy/ivy_1_ddna.tif",
"D:/Perforce/GameSDK/Objects/natural/vegetation/veg_ivy/ivy_1_diff.tif",
"D:/Perforce/GameSDK/Objects/natural/vegetation/veg_ivy/ivy_2_ddna.tif",
"D:/Perforce/GameSDK/Objects/natural/vegetation/veg_ivy/ivy_2_diff.tif",
"D:/Perforce/GameSDK/Objects/structures/RangerTower/textures/Tower_Plaster_diff.tif",
"D:/Perforce/GameSDK/Objects/structures/Residential/The_Last_House/Textures/TLH/test Spec.tif",
#"D:/Perforce/GameSDK/Particles/projectiles/projectile01.tif",
#"D:/Perforce/GameSDK/Particles/textures/Corona.tif",
#"D:/Perforce/GameSDK/Particles/textures/glow05.tif",
#"D:/Perforce/GameSDK/Particles/textures/flame/fire_anim02_x72.tif",
"D:/Perforce/GameSDK/Textures/architecture/roof/rooftiles_black_dif.tif",
"D:/Perforce/GameSDK/Textures/concrete/concrete_rectanglepanel_ddna.tif",
"D:/Perforce/GameSDK/Textures/decals/Pine_Needles/PineNeedlesBig_ddna.tif",
"D:/Perforce/GameSDK/Textures/decals/Pine_Needles/PineNeedlesBig_diff.tif",
"D:/Perforce/GameSDK/Textures/decals/Pine_Needles/PineNeedlesBig_displ.tif",
"D:/Perforce/GameSDK/Textures/decals/RockyDirt/DirtPebbles_detail.tif",
"D:/Perforce/GameSDK/Textures/decals/RockyDirt/Pebbles_diff.tif",
"D:/Perforce/GameSDK/Textures/detail_bumpmaps/concrete/concrete_07_detailbump_ddn.tif",
"D:/Perforce/GameSDK/Textures/detail_bumpmaps/stone/stone_01_detailbump_ddn.tif",
"D:/Perforce/GameSDK/Textures/fabric/cloth_pack_01_dif.tif",
"D:/Perforce/GameSDK/Textures/fabric/cloth_pack_02_diff.tif",
"D:/Perforce/GameSDK/Textures/generic/Tiles/Tile_Floor_Ruined_ddna.tif",
"D:/Perforce/GameSDK/Textures/metal/metal_1_PBR_ddna.tif",
"D:/Perforce/GameSDK/Textures/terrain/Asphalt/Asphalt_ddna.tif",
"D:/Perforce/GameSDK/Textures/terrain/Asphalt/Asphalt_diff.tif",
"D:/Perforce/GameSDK/Textures/terrain/detail/grass_moss_PBR_ddna.tif",
"D:/Perforce/GameSDK/Textures/terrain/RiverBed/RiverBed_Ddna.tif",
"D:/Perforce/GameSDK/Textures/terrain/RiverBed/RiverBed_Detail.tif",
"D:/Perforce/GameSDK/Textures/terrain/Sand/SandPatch_Ddna.tif",
"D:/Perforce/GameSDK/Textures/terrain/Sand/SandPatch_Detail.tif",
"D:/Perforce/GameSDK/Textures/terrain/Sand/SandRocks1_ddna.tif",
"D:/Perforce/GameSDK/Textures/terrain/Sand/SandRocks1_detail.tif",
"D:/Perforce/GameSDK/Textures/terrain/Sand/SandRocks2_ddna.tif",
"D:/Perforce/GameSDK/Textures/terrain/Sand/SandRocks2_detail.tif",
"D:/Perforce/GameSDK/Textures/vegitation/Moss/Moss_soft_ddna.tif",
"D:/Perforce/GameSDK/Textures/Wood/house_textures/wood_paintedcracked.tif",
"D:/Perforce/GameSDK/Textures/Wood/house_textures/wood_paintedcracked_ddna.tif",
"D:/Perforce/GameSDK/Textures/Wood/house_textures/wood_paintedcracked_red.tif",
"D:/Perforce/GameSDK/Textures/Wood/house_textures/wood_painted_ddna.tif",
"D:/Perforce/GameSDK/Textures/Wood/house_textures/wood_painted_scraped.tif"
]

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
	      # return raw values from a tag
	      return input
	batch_list = list()
	
	for image in batch:
		im = tifffile.TiffFile(image)
		# extract the date
		iptc = strip_control_characters(im.pages[0].tags['photoshop'].value.tostring())
		fixed_iptc = iptc.replace('/ser=1', '/ser=0')
		executable = 'exiftool.exe'
		batch_list.append(executable + ' -SpecialInstructions="%s" "%s"' % (fixed_iptc, image))
	
	file = open('batch_list.bat', 'w')

	for batch in batch_list:
		file.writelines(batch + "\n")

	file.close()


if __name__ == '__main__':
	main()
