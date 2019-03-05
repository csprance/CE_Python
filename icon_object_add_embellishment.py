import general
from icon_object_capture import get_icon_object_in_scene
import icon_object_save


def add_embellishment():
    obj = get_icon_object_in_scene()
    embellishment = dict()
    general.message_box("Select 48x48 Embellishment Image")
    embellishment["embellishment_48"] = general.open_file_box()
    general.message_box("Select 200x200 Embellishment Image")
    embellishment["embellishment_200"] = general.open_file_box()
    general.message_box("Select 2048x2048 Embellishment Image")
    embellishment["embellishment_2048"] = general.open_file_box()
    if general.message_box_yes_no("Should embellishment be under main image?"):
        embellishment["embellishment_under"] = True
    icon_object_save.save(obj["name"], embellishment=embellishment)


if __name__ == "__main__":
    reload(icon_object_save)
    add_embellishment()
