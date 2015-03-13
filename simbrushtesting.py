#! python
#SImulate Brush#

# 1. Select object
# 2. Run Script
# 	1. Get selected object. getselected()
# 	2. Create rigid body ex and copy model to rigidbodyex createrigid()
# 	3. snap rigid body ex to xform of selected object snapphys()
# 	4. and prompt user for weight setweight()
# 	5-6. hide selected object/simulate rigidbody ex simobj()
# 	7. after simulation is done copy original object to new xform of simulated rigid body setobj()
# 	8. delete rigid body. delrigids()
import sys, general, physics, thread, time

# get the list of all of our objects
class SimBrush(object):
	"""
	This class holds all the relevant info for the brush and it's temporary physics 
	object created with it
	"""
	def __init__(self,name, pos,rot,scale, model, physobj):
		super(SimBrush, self).__init__()
		self.pos = pos
		self.rot = rot
		self.scale = scale
		self.model = model
		self.physobj = physobj
		self.name = name



#returns a tuple3 containing all relevant info on object
# example: ('plastic_chair7', (78.49897003173828, 50.81959915161133, 29.135202407836914), (0.0, -0.0, -157.99998474121094), (1.0, 1.0, 1.0))
def getselected():
	# 	1. Get selected object.
	objname = general.get_names_of_selected_objects()
	objects = []
	for idx, x in enumerate(objname):
		objpos = general.get_position(x)
		objrot = general.get_rotation(x)
		objscale = general.get_scale(x)
		objgeo = general.get_entity_param(x,r'Geometry')
		physobj = createrigid(objgeo,idx)
		#append all the objects to the list
		objects.append(SimBrush(x , objpos, objrot, objscale, objgeo, physobj))
	return objects




def createrigid(modelgeo, simid):
	# 	2. Create rigid body ex and copy model to rigidbodyex
	# we create the name so we never have to worry about duplicate named objects
	simname = 'brush_sim_temp' + str(simid)
	#create the object at 0,0,0
	physobj = general.new_object('Entity', r'RigidBodyEx', simname, 0, 0, 0)
	# set the physobj to be the modelgeo param
	general.set_entity_property(physobj, r'Model', modelgeo)
	# return the name so we can use it later
	return physobj

def snapphys(obj):
	# 	3. snap physobj to xform of selected object
	general.set_position(obj.physobj,obj.pos[0],obj.pos[1],obj.pos[2])
	general.set_rotation(obj.physobj,obj.rot[0],obj.rot[1],obj.rot[2])
	general.set_scale(obj.physobj,obj.scale[0],obj.scale[1],obj.scale[2])

def setweight(obj):
	# 	4. prompt user for weight
	# How much does this object weight?
	if len(sys.argv) > 1:
		if sys.argv[1] == 'weight':
			simweight = general.edit_box('How much does this object weight?')
		else:
			simweight = 350
	else:
		simweight = 350
	#set the weight for every object
	for x in obj:
		general.set_entity_property(x.physobj, r'Mass', simweight)

def simobjs(obj):
	for x in obj:
		general.hide_object(x.name)
	physics.simulate_selection()
	print(general.get_edit_mode())
	return True


def setobj(obj, secs):
	# 	7. after simulation is done copy original object to new xform of simulated rigid body
	#general.unhide_object(obj.name)
	for x in xrange(1 , secs ):
		physics.get_state(obj.physobj)
		physpos = general.get_position(obj.physobj)
		physrot = general.get_rotation(obj.physobj)
		physscale = general.get_scale(obj.physobj)
		print(obj.pos)
		print(physpos)
		general.set_position(obj.name,physpos[0],physpos[1],physpos[2])
		general.set_rotation(obj.name,physrot[0],physrot[1],physrot[2])
		general.set_scale(obj.name,physscale[0],physscale[1],physscale[2])




# 	8. delete rigid body.
def delrigids(obj):
	general.delete_object(obj.physobj)

def restoreSelection(obj):
	general.unhide_object(obj.name)

def main():
	# get the list of selected objects and all the attributes convert them to objects and put them in a list
	# this also create the temp rigidbodies needed at 0,0,0
	selected = getselected()
	general.log('')
	# if the set weight option is called set it here if not use 45 as the weight
	setweight(selected)
	for x in selected:
		# snap our physobjects to there objects in space.
		snapphys(x)
	# clear the selection
	general.clear_selection()
	#this will contain the list of items to select
	names = []
	#generate or list of names to select
	for x in selected:
		names.append(x.physobj)
	#select our physobjs	
	general.select_objects(names)
	#simulate the selected objects
	simobjs(selected)



	# when phyics have finsihed set the objects
	for x in selected:
		thread.start_new_thread(setobj, (x,0))


if __name__ == "__main__": main()