'''
Ask the user for the values and paste them into the box comma seperated

'''
import sys

properties = ['amount','DiffuseDarkening','FakeReflectionsAmount','PuddlesAmount','puddlesMaskAmount','puddlesRippleAmount','RainDropsAmount','RainDropsLighting','RainDropsSpeed','SplashesAmount']

#grab the selected rain entity
selObj = general.get_names_of_selected_objects()
selObj = selObj[0]

#grab the values
values = general.edit_box('Paste Values')
# split them into a list
valList = [x.strip() for x in values.split(',')]

#set all the values
counter = 0
for x in properties:
	general.set_entity_property(selObj, x, valList[counter])
	#increment
	counter += 1	