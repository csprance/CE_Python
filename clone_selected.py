# duplicates a selected object a set amount of time in any direction
import general


def main():
    selected = general.get_names_of_selected_objects()
    print(selected)
    input_axis = {"X": 0, "Y": 1, "Z": 2}
    axis = input_axis[str(general.edit_box("Axis: X, Y, Z")).upper()]
    num_copies = int(general.edit_box("Number of Clones"))
    distance = int(general.edit_box("Distance between clones"))
    for mesh_idx, mesh in enumerate(selected):
        start_pos = general.get_position(mesh)
        start_rot = general.get_rotation(mesh)
        start_scale = general.get_scale(mesh)
        for idx in xrange(num_copies):
            new_mesh = general.create_object(
                "Brush",
                general.get_entity_geometry_file(selected[mesh_idx]),
                mesh,
                0,
                0,
                0,
            )
            new_pos = [x for x in start_pos]
            new_pos[axis] += distance * (idx + 1)
            new_mesh.position = (new_pos[0], new_pos[1], new_pos[2])
            new_mesh.rotation = (start_rot[0], start_rot[1], start_rot[2])
            new_mesh.scale = (start_scale[0], start_scale[1], start_scale[2])
            new_mesh.update()


if __name__ == "__main__":
    main()
