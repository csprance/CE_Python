#! python
#SImulate Brush#

# 1. Select object
# 2. Run Script
# 	1. Get selected object.
# 	2. Create rigid body ex and copy model to rigidbodyex
# 	3. snap rigid body ex to xform of selected object
# 	4. and prompt user for weight
# 	5. hide selected object
# 	6. simulate rigidbody ex
# 	7. after simulation is done copy original object to new xform of simulated rigid body
# 	8. delete rigid body.
import sys

# 	1. Get selected object.
#grab some properties for our selected object
objname = general.get_names_of_selected_objects()
objpos = general.get_position(objname[0])
objrot = general.get_rotation(objname[0])
objscale = general.get_scale(objname[0])

# 	2. Create rigid body ex and copy model to rigidbodyex
#create the object at 0,0,0
physobj = general.new_object('Entity', r'RigidBodyEx', r'brush_sim_temp', 0, 0, 0)
# set the physobj to be the selected brush object
general.set_entity_property(physobj, r'Model', lodtools.getselected())

# 	3. snap physobj to xform of selected object
general.set_position(physobj,objpos[0],objpos[1],objpos[2])
general.set_rotation(physobj,objrot[0],objrot[1],objrot[2])
general.set_scale(physobj,objscale[0],objscale[1],objscale[2])

# 	4. prompt user for weight
# How much does this object weight?
if len(sys.argv) > 1:
	if sys.argv[1] == 'weight':
		simweight = general.edit_box('How much does this object weight?')
	else:
		simweight = 45
else:
	simweight = 45
#set the weight
general.set_entity_property(physobj, r'Mass', simweight)



#5 Hide object
general.log('hiding ' + objname[0])

def simobj():
	general.hide_object(objname[0])
	general.select_object(physobj)
	physics.simulate_selection()
	general.clear_selection()
	general.select_object(objname[0])


	
# 	6. simulate physobj
#select sim_brush
simobj()







# 	7. after simulation is done copy original object to new xform of simulated rigid body
def setobj():
	physics.get_state(physobj)
	physpos = general.get_position(physobj)
	physrot = general.get_rotation(physobj)
	physscale = general.get_scale(physobj)
	general.unhide_object(objname[0])
	general.set_position(objname[0],physpos[0],physpos[1],physpos[2])
	general.set_rotation(objname[0],physrot[0],physrot[1],physrot[2])
	general.set_scale(objname[0],physscale[0],physscale[1],physscale[2])



# 	8. delete rigid body.





