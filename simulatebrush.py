#! python
# SImulate Brush#

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
import better_cry
from user_values import UserValues

if __name__ == "__main__":
    PHY_OBJ_NAME = "brush_sim_temp"
    level = better_cry.Level()
    store = UserValues()
    # check if we have a stored brush
    stored_brush = store.get("simmed_brush")

    if stored_brush is None:
        # 	1. Get selected object.
        brush = level.selected[0]
        # store the users selection for setting the physics state later on
        store.set("simmed_brush", brush.name)
        # 	2. Create rigid body ex and copy model to rigidbodyex
        phys_obj = level.new_object("Entity", r"RigidBodyEx", PHY_OBJ_NAME, 0, 0, 0)
        # mark it with a special material so you know it's being simulated
        phys_obj.material = "Materials/Special/green_screen.mtl"
        # set the physobj to be the selected brush object
        phys_obj.geometry_file = brush.geometry_file
        # 	3. snap physobj to xform of selected object
        phys_obj.position = (brush.position[0], brush.position[1], brush.position[2])
        phys_obj.rotation = (brush.rotation[0], brush.rotation[1], brush.rotation[2])
        phys_obj.scale = (brush.scale[0], brush.scale[1], brush.scale[2])
        # 5 Hide user selection object
        brush.hide()
        # 	6. simulate physobj
        phys_obj.simulate()

    if stored_brush is not None:
        brush = level.get_object_by_name(str(stored_brush))
        # unhide the original object
        brush.unhide()
        # get the state of the physics objects
        phys_obj = level.get_object_by_name(PHY_OBJ_NAME)
        phys_obj.get_physics_state()
        # set the transforms of the original object to have the transforms of the simulated object
        brush.position = phys_obj.position
        brush.rotation = phys_obj.rotation
        brush.scale = phys_obj.scale
        # delete the physics object
        level.clear_selection()
        phys_obj.delete()
        # reselect the users original selection
        brush.select()
        # delete the simmed brush key so we can simulate another model
        store.delete("simmed_brush")
