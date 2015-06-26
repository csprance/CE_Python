import xml.etree.ElementTree as et
import sys


try:
	if len(sys.argv[1]) > 0:
		f = sys.argv[1]
except:
			f = 'D:\perforce\GameSDK\Scripts\Crafting\Recipes.xml'
tree = et.parse(f)

root = tree.getroot()


recipes = tree.findall('recipe')
file  = open('formatted_recipes.txt', 'w+')
for recipe in recipes:
	recipe_name = recipe.attrib['name']
	for con_time in recipe:
		construction_time = con_time.attrib['time']
		item_name = con_time.findall('item')[0].attrib['name']
		mats = con_time.findall('material')
		materials = set()
		file.write( 'Item Name: ' + item_name + '\n')
		file.write( 'Time to Construct: ' + construction_time + '\n')
		file.write( 'Name of Recipe: ' + recipe_name + '\n')
		for mat in mats:
			file.write( 'Mats Needed: ' + mat.attrib['name'] + '\n')
		file.write( "---------------------"  + '\n')

