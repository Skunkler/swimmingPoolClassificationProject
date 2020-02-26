import arcpy
from arcpy import env
from arcpy.sa import *

env.workspace = r'D:\SwimmingPools2017\unsupervisedClassification'

studyArea = r"S:\LV_Valley_Imagery\2017\Veg_analysis\Veg_Sections_3in6in.shp"

rasters = arcpy.ListRasters()


areaOfInterestTable = r"S:\LV_Valley_Imagery\2017\SwimmingPool2017\Tileswith110_2017.csv"
outputStatsTable = r'S:\LV_Valley_Imagery\2017\SwimmingPool2017\unsupervisedStatsStudy.gdb\StatsTable_'

arcpy.CheckOutExtension("Spatial")

def get_swimming_pool_list():
    swimmingPoolBkSecSet = set()
    readFile = open(areaOfInterestTable, 'r')
    lines = readFile.readlines()

    for line in lines:
        if line.split(',')[0].isdigit():
            swimmingPoolBkSecSet.add(line.split(',')[14])
    return swimmingPoolBkSecSet
        
def get_specific_zone():

    stdyLyr = arcpy.MakeFeatureLayer_management(studyArea, 'studyAreaLyr')
    for raster in rasters:
        with arcpy.da.SearchCursor(stdyLyr, 'BOOKSEC_PT') as cursor:
            for row in cursor:
                if row[0] == raster[:-4]:
                    print row[0]
                    arcpy.SelectLayerByAttribute_management(stdyLyr, 'NEW_SELECTION', "BOOKSEC_PT = '" + raster[:-4] + "'")
                    outZSat = ZonalStatisticsAsTable(stdyLyr, 'BOOKSEC_PT', raster, outputStatsTable + raster[:-4])
                    arcpy.SelectLayerByAttribute_management(stdyLyr, 'CLEAR_SELECTION')
    


    

def get_study_area_tile(stdyLyr, raster):
    with arcpy.da.SearchCursor(stdyLyr, 'BOOKSEC_PT') as cursor:
        for row in cursor:
            if row[0] == raster[:-4]:
                print row[0]
                arcpy.SelectLayerByAttribute_management(stdyLyr, 'NEW_SELECTION', "BOOKSEC_PT = '" + raster[:-4] + "'")
                outZSat = ZonalStatisticsAsTable(stdyLyr, 'BOOKSEC_PT', raster, outputStatsTable)
        print "Process complete"
            

get_specific_zone()
