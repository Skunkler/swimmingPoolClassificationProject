import arcpy
from arcpy import env

env.workspace = r'S:\LV_Valley_Imagery\2017\SwimmingPool2017\QA_point_class.gdb'

fcs = arcpy.ListFeatureClasses()

for fc in fcs:
    if len(fc) >= 10:
        print fc
        arcpy.Delete_management(fc)
