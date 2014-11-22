'''
Spits out your rain Values for you

this will take the currently select rain item and generate the rain values for you.
horrible code but it does the job
'''
import sys

#spits out the code for the rain values for faster tweaking
properties = ['amount','DiffuseDarkening','FakeReflectionsAmount','PuddlesAmount','puddlesMaskAmount','puddlesRippleAmount','RainDropsAmount','RainDropsLighting','RainDropsSpeed','SplashesAmount']


#holding pattern for loop
retVal = "self:SetRainValues("
for x in properties:
	selObj = general.get_names_of_selected_objects()
	temp = general.get_entity_property(selObj[0] , x)
	retVal = retVal + str(temp) + ','
# print out the holding pattern
print "holding pattern"
print retVal + ");"


# ramp u pattern for loop
print "ramp up pattern"
retVal = "self:SetRainValues("
counter = 0
for x in properties:
	counter = counter + 1
	selObj = general.get_names_of_selected_objects()
	temp = general.get_entity_property(selObj[0] , x)
	#0.5*rp, 0.0*rp, 0.11*rp, 1.0, 0.7, 1.0, 0.1*rp, 2.0, 1.0, 1.0*rp
	if (counter == 1) or (counter == 2) or (counter == 3) or (counter == 7) or (counter == 10):
		retVal = retVal + str(temp) + "*rp,"
	else:
		retVal = retVal + str(temp) + ','
print retVal + ");"



# ramp down pattern for loop
print "ramp down pattern"
retVal = "self:SetRainValues("
counter = 0
for x in properties:
	counter = counter + 1
	selObj = general.get_names_of_selected_objects()
	temp = general.get_entity_property(selObj[0] , x)
	#0.5 - 0.5*rp, 0.0, 0.11 - 0.11*rp, 1.0, 0.7, 1.0, 0.1 - 0.1*rp, 2.0, 1.0, 1.0 - 1.0*rp
	if (counter == 1) or (counter == 3) or (counter == 7) or (counter == 10):
		retVal = retVal + str(temp) + " - " + str(temp) + "*rp,"
	else:
		retVal = retVal + str(temp) + ','
print retVal + ");"			
