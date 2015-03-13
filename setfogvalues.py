'''
Ask the user for the values and paste them into the box comma seperated

'''

import sys


setFogValues( 0 , 0 , 0 , .5 , 500, .3 , .5 , 6000 , .3 , 1 , 20 , 0 , 1000 , 0.7 )

def setFogValues(hdrpowfac, gimult, suncolmult, fogcol2mult, volfogheight, volfogdensity, volfogfindensityclamp, volfogrampstart, volfogrampend, volfogrampinf):
	#grab the values
	values = general.edit_box('Paste Fog Values :hdrpowfac, gimult, suncolmult, fogcol2mult, volfogheight, volfogdensity, volfogfindensityclamp, volfogrampstart, volfogrampend, volfogrampinf')
	# split them into a list
	valList = [x.strip() for x in values.split(',')]

	#set all the values
	counter = 0
	for x in properties:
		#set it here
		#general.set_entity_property(selObj, x, valList[counter])

		
		#increment
		counter += 1	

def getFogValues(hdrpowfac, gimult, suncolmult, fogcol2mult, volfogheight, volfogdensity, volfogfindensityclamp, volfogrampstart, volfogrampend, volfogrampinf):

	strOut = 'WM.SetFloatModifier(eWM_HDR_DYNAMIC_POWER_FACTOR, 0, rdpmult)'+
	'WM.SetFloatModifier(eWM_GI_MULTIPLIER, 0, rdpmult);'+
	'# sun values (sun becomes hidden by fog, we dont want shadows)'+
	'WM.SetFloatModifier(eWM_SUN_COLOR_MULTIPLIER, 0, rdpmult);'+

	'# bottom values'+
	'#WM.SetFloatModifier(eWM_FOG_COLOR_MULTIPLIER, .5, rdp);'+
	'#WM.SetFloatModifier(eWM_VOLFOG_HEIGHT, 500, rdp);'+
	'#WM.SetFloatModifier(eWM_VOLFOG_DENSITY, .3, rdp);'+

	'# top values'+
	'WM.SetFloatModifier(eWM_FOG_COLOR2_MULTIPLIER, .5, rdp);'+
	'WM.SetFloatModifier(eWM_VOLFOG_HEIGHT2, 6000, rdp);'+
	'WM.SetFloatModifier(eWM_VOLFOG_DENSITY2, .3, rdp);'+

	'# global values'+
	'WM.SetFloatModifier(eWM_VOLFOG_FINAL_DENSITY_CLAMP, 1, rdp);'+
	'WM.SetFloatModifier(eWM_VOLFOG_GLOBAL_DENSITY, 20, rdp);'+

	'# ramp values (helps make the fog dense)'+
	'WM.SetFloatModifier(eWM_VOLFOG_RAMP_START, 0, rdp);'+
	'WM.SetFloatModifier(eWM_VOLFOG_RAMP_END, 1000, rdp);'+
	'WM.SetFloaModifier(eWM_VOLFOG_RAMP_INFLUENCE, 0.7, rdp);'