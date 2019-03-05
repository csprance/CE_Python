import os

screens_list = ['MilitaryJacketGreen_48.jpg',
                'MilitaryJacketGreenCamo1_48.jpg',
                'MilitaryJacketGreenCamo2_48.jpg',
                'MilitaryJacketGreenCamo3_48.jpg',
                'MilitaryJacketGreenCamo4_48.jpg',
                'MilitaryJacketTan_48.jpg',
                'MilitaryJacketTanCamo_1_48.jpg',
                'MilitaryJacketTanCamo_2_48.jpg',
                'MilitaryJacketTanCamo_3_48.jpg',
                'MilitaryJacketTanCamo_4_48.jpg',
                'MilitaryJacketUrbanCamo_1_48.jpg',
                'MilitaryJacketUrbanCamo_2_48.jpg',
                'MilitaryJacketUrbanCamo_3_48.jpg',
                'MilitaryJacketUrbanCamo_4_48.jpg',
                ]

for idx, i in enumerate(os.listdir("D:\perforce\dev\USER\screenshots")):
    if i.endswith(".jpg"):
        print "D:\perforce\dev\USER\screenshots\\" + i
        print screens_list[idx]
        os.rename("D:\perforce\dev\USER\screenshots\\" + i, screens_list[idx])
