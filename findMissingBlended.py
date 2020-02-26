import arcpy
from arcpy import env

env.workspace = r'D:\SwimmingPool2017\gdb\Review_data.gdb'
poolFiltered2 = r'D:\SwimmingPool2017\gdb\pools_section_filtered2.gdb'
pool_cover_filter = r'D:\SwimmingPool2017\gdb\pools_cover_filter.gdb'



fcs = arcpy.ListFeatureClasses()
Rev_polys = []

for fc in fcs:
    print fc[7:16]
    Rev_polys.append(fc[7:16])
    

env.workspace = poolFiltered2

print "looping through poolfiltered 2"

fcs = arcpy.ListFeatureClasses()


"""for fc in fcs:
    if fc[6:14] in Rev_polys:
        print "deleting " + fc
        arcpy.Delete_management(fc)"""


env.workspace = pool_cover_filter

fcs = arcpy.ListFeatureClasses()

for fc in fcs:
    if fc[6:] in Rev_polys:
        print "deleting " + fc
        arcpy.Delete_management(fc)
