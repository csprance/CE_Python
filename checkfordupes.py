# checks selected objects for duplicated objects
# a duplicated object is any mesh that shares the same position, rotation, scale and model name.
# it adds all the selected objects to a list and then checks each item in the list against the other items in the list
# if it finds a match it will add that match to a new list of duplicates
# once it's finsihed running through the list it will unselect everything and select the duplicated objects so you can move/delete them


# get our selected objects and stick them into a list
selObj = general.get_names_of_selected_objects()
# declare our object array
objList = []
# iterate through each selected object and add it's data to be checked into objList[]

for x in selObj:
	pos = general.get_position(x)
	rot = general.get_rotation(x)
	scl = general.get_scale(x)
	name = x
	geo = general.get_entity_param(x, "Geometry")
	params = [pos, rot, scl, geo]
	# append the params to the objList
	objList.append(params)

#objList now cotains a list of lists with all the paramters
# add it to a select
setList = set(objList)

# setList now cotains only unique values
# iterate through it and check if a value is in the set. If it's not, add the name of the mesh to a list to select
listToSelect = list()

for x not in setList:
	print x 
