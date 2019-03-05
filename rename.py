import general


if __name__ == "__main__":
    # get our selected objects and stick them into a list
    selObj = general.get_names_of_selected_objects()
    for item in selObj:
        print(item)
        general.rename_object(item, ("%s_%s" % (item, 1)).replace("_41_1", ""))
