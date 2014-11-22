# ###################################################
# This Script will hide and unhide the spawner cones
# Chris Sprance
# Entrada Interactive
# Miscreated 
# ##################################################

# function to get the list of current spawners
def getSpawners():
	import os
	# find out where were runing the editor from
	rundir = os.getcwd()
	# get a list of all the current spawners
	spawners = '\\GameSDK\\Objects\\spawners'
	spawnlist = os.listdir(rundir+spawners)
	spawnerlist = list()
	for x in spawnlist:
		if x.endswith('.cgf'):
			spawnerlist.append(x.replace('.cgf', ''))
	return spawnerlist

# function to get all the objects in the level into one list
def getAllObjects():
	# define our list of objects to search through
	objects = list()
	#get all the layers
	layers = general.get_all_layers()
	#for every layer get all the objects in it
	for x in layers:
		objects.extend(general.get_all_objects_of_layer(x))
	#send the compiled list back
	return objects	

# function to hide an object
def hideObject(obj):
	general.hide_objects(obj)

# function to unhide an object
def unhideObject(obj):
	general.unhide_object(obj)

	
# get our spawners
spawners = getSpawners()
# get our objects
objects = getAllObjects()

for obj in objects:
	for spawner in spawners:
		# print spawner
		# print obj
		if obj.find(spawner):
			print obj
		# here I need to compare the spawner to the obj and see if the names match
		# probably need to format the obj first and remove and number maybe using obj.find(spawner)
# the list full of the objects we want to hide
hidelist = list()

#iterate through our objects and check them against the spwaners list

			
# 
# 
# for each object in objects
# 	if it matches one of the valuesin spwaners[]
# 	add it to spawnerlist[]
# 
# 
# for x in spawnerlist:
# 	general.hide_object(x)
# 

