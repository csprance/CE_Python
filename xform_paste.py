import general
from user_values import UserValues


def paste_xforms():
    store = UserValues()
    selected = general.get_names_of_selected_objects()[0]
    if selected is None:
        general.message_box_ok("Please Select an object")
    xforms = store.get("xforms")
    general.set_position(selected, xforms['pos'][0], xforms['pos'][1], xforms['pos'][2])
    general.set_rotation(selected, xforms['rot'][0], xforms['rot'][1], xforms['rot'][2])
    general.set_scale(selected, xforms['scale'][0], xforms['scale'][1], xforms['scale'][2])


if __name__ == "__main__":
    paste_xforms()
