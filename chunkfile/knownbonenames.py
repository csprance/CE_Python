#Embedded file name: chunkfile\knownbonenames.pyc
import binascii
import sys
init_known_bone_names = ('Bip01', 'Bip01 Camera', 'Bip01 CustomAim', 'Bip01 CustomAimStart', 'Bip01 AimTarget', 'Bip01 LookTarget', 'Bip01 Head', 'Bip01 Neck', 'Bip01 Clavicle', 'Bip01 Pelvis', 'Bip01 planeTargetLeft', 'Bip01 planeTargetRight', 'Bip01 planeWeightLeft', 'Bip01 planeWeightRight', 'Bip01 Spine', 'Bip01 Spine1', 'Bip01 Spine2', 'Bip01 Spine3', 'Bip01 L Calf', 'Bip01 L Clavicle', 'Bip01 L Finger0', 'Bip01 L Finger1', 'Bip01 L Finger2', 'Bip01 L Finger3', 'Bip01 L Finger4', 'Bip01 L Finger5', 'Bip01 L Finger00', 'Bip01 L Finger01', 'Bip01 L Finger02', 'Bip01 L Finger03', 'Bip01 L Finger04', 'Bip01 L Finger05', 'Bip01 L Finger10', 'Bip01 L Finger11', 'Bip01 L Finger12', 'Bip01 L Finger20', 'Bip01 L Finger21', 'Bip01 L Finger22', 'Bip01 L Finger30', 'Bip01 L Finger31', 'Bip01 L Finger32', 'Bip01 L Finger40', 'Bip01 L Finger41', 'Bip01 L Finger42', 'Bip01 L Finger50', 'Bip01 L Finger51', 'Bip01 L Finger52', 'Bip01 L Foot', 'Bip01 L Forearm', 'Bip01 L ForeTwist', 'Bip01 L ForeTwist0', 'Bip01 L ForeTwist1', 'Bip01 L ForeTwist2', 'Bip01 L Hand', 'Bip01 L Heel', 'Bip01 L Thigh', 'Bip01 L Toe', 'Bip01 L Toe0', 'Bip01 L Toe1', 'Bip01 L UpperArm', 'Bip01 L UpperTwist', 'Bip01 L UpperTwist0', 'Bip01 L UpperTwist1', 'Bip01 L UpperTwist2', 'L_ClavFront', 'L_Gluceus', 'L_Knee', 'L_Lat', 'L_Lat_0', 'L_Lat_1', 'L_Lat_2', 'L_Lat_3', 'L_Lat_4', 'L_Lat_5', 'L_Pectoralis', 'Lweapon_bone', 'Bip01 LHand2Aim_IKBlend', 'Bip01 LHand2Aim_IKTarget', 'Bip01 LHand2PistolPos_IKBlend', 'Bip01 LHand2PistolPos_IKTarget', 'Bip01 LHand2Pocket_IKBlend', 'Bip01 LHand2Pocket_IKTarget', 'Bip01 LHand2RiflePos_IKBlend', 'Bip01 LHand2RiflePos_IKTarget', 'Bip01 LHand2Weapon_IKBlend', 'Bip01 LHand2Weapon_IKTarget')
known_bone_names = {}
for init_name in init_known_bone_names:
    names = (init_name,)
    if ' L ' in init_name:
        names = (init_name, init_name.replace(' L ', ' R '))
    elif ' L' in init_name:
        names = (init_name, init_name.replace(' L', ' R', 1))
    elif init_name.startswith('L'):
        names = (init_name, init_name.replace('L', 'R', 1))
    for name in names:
        crc = binascii.crc32(name) & 4294967295L
        if crc in known_bone_names:
            print 'name: {0} crc: {1}  existName: {2}'.format(name, crc, known_bone_names[crc])
            sys.exit('bone names: crc32 collision')
        known_bone_names[crc] = name

def getBoneInfoByCrc32(crc):
    if crc in known_bone_names:
        return '{0:#x} ({1})'.format(crc, known_bone_names[crc])
    return '{0:#x}'.format(crc)
