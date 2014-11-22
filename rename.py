# get our selected objects and stick them into a list
selObj = general.get_names_of_selected_objects()

#for each object in the list go through and rename it 
counter = 0
names = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","0","1","2","3","4","5","6","7","8","9"]
for x in selObj:
	print x 
	print names[counter]
	general.rename_object(x,names[counter])
	counter = counter + 1
