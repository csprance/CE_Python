# given a selection of items go through and replace each one with a mesh selected from a file open dialog
import general


def replace_selected():
    new_objects = list()
    # get the mesh to replace the selected item with
    replacement_mesh = general.open_file_box()
    # get all selected object
    selected = general.get_names_of_selected_objects()
    # clear the selection so we can work on one item at a time
    general.clear_selection()
    for item in selected:
        # store the items xforms
        [scale_x, scale_y, scale_z] = general.get_scale(item)
        [pos_x, pos_y, pos_z] = general.get_position(item)
        [rot_x, rot_y, rot_z] = general.get_rotation(item)
        general.delete_object(item)
        new_objects.append(
            general.new_object("Brush", replacement_mesh, item, pos_x, pos_y, pos_z)
        )
        general.set_rotation(item, rot_x, rot_y, rot_z)
        general.set_scale(item, scale_x, scale_y, scale_z)
        print("Replaced: %s with %s" % (item, replacement_mesh))
    general.select_objects(new_objects)


if __name__ == "__main__":
    replace_selected()
