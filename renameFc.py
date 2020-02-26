import arcpy
from arcpy import env

env.workspace=r'S:\LV_Valley_Imagery\2017\SwimmingPool2017\gdb\review_data.gdb'
env.overwriteOutput = True

fcs = arcpy.ListFeatureClasses()

for fc in fcs:
    if len(fc) == 20:
        print fc
        arcpy.Rename_management(fc, 'Review_' + fc[4:12])
