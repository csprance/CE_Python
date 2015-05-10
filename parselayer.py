import xml.etree.ElementTree as ET

def parseXML(layerfile):
    """Parse the xml and return the xml tree back to us"""
    bake_settings = open(layerfile)
    tree = ET.parse(bake_settings).getroot()
    return tree

def main():
	pass

if __name__ == '__main__':
	main()
	tree = parseXML("D:\perforce\GameSDK\Levels\islands\layers\cave_mushroom_spaweners.lyr")
	x = tree.find('Layer').find('LayerObjects').findall('Object')
	print (x[0].attrib['Prefab'])


