import general
import uuid


def makeUnique(obj):
	#init our list
	retlist  = list()
	for x in obj:
		unid = str(uuid.uuid4())[:10]
		general.rename_object(x,unid)
		retlist.append(unid)
	return retlist

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

test = getAllObjects()

print test