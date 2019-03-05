import general
from user_values import UserValues


def copy_xforms():
    store = UserValues()
    selected = general.get_names_of_selected_objects()[0]
    if selected is None:
        general.message_box_ok("Please Select an object")
    rot = general.get_rotation(selected)
    pos = general.get_position(selected)
    scale = general.get_scale(selected)
    store.set("xforms", {"rot": rot, "pos": pos, "scale": scale})


if __name__ == "__main__":
    copy_xforms()
