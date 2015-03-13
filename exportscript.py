import general

selobj = general.get_names_of_selected_objects()

pos = general.get_position(selobj)

# set the posoition to 0,0,0 
general.set_position(selobj, 0,0,0)


