import xml.etree.ElementTree as ET

def parseXML(layerfile):
    """Parse the xml and return the xml tree back to us"""
    bake_settings = open(layerfile)
    tree = ET.parse(bake_settings).getroot()
    return tree

def get_atrribs(f, attribute):
	tree = parseXML(f)
	x = tree.find('Layer').find('LayerObjects').findall('Object')
	retval = list()
	for y in x:
		try:
			retval.append( (attribute, y.attrib[attribute]))
		except:
			retval.append((attribute,None))
	return retval

def main():
	x = get_atrribs("D:\perforce\GameSDK\Levels\islands\layers\marco_layers\center_hills.lyr", 'EntityType')
	x = get_atrribs("D:\perforce\GameSDK\Levels\islands\layers\marco_layers\center_hills.lyr", 'Prefab')
	print(x)

if __name__ == '__main__':
	main()



