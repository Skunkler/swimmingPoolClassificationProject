import arcpy
from arcpy import env

step3_filtered2_ws = raw_input("Please enter pools_section_filtered2.gdb: ")
step4_ws = raw_input("Please enter step4 filter data: pools_cover_filter.gdb: ")
outBlendedWS = r'D:\SwimmingPool2017\gdb\Review_data.gdb'
projectAreaParcels = r'\\storage\snwa\spatialtech_imagery\LV_Valley_Imagery\2017\SwimmingPool2017\gdb\general_data.gdb\parcels_AOX_110LU'
outClippedBlendedWS = r'D:\SwimmingPool2017\gdb\ClippedBlended.gdb'
outClippedBlendedIDWS = r'D:\SwimmingPool2017\gdb\ClippedIDBlended_F.gdb'

#project tiles 
projectAreaTiles = r'\\storage\snwa\spatialtech_imagery\LV_Valley_Imagery\2017\SwimmingPool2017\gdb\general_data.gdb\ProjectStudyAreaTiles'





def further_process_blended():
    env.workspace = outBlendedWS
    env.overwriteOutput = True
    GISDBASCL = r'S:\LV_Valley_Imagery\2017\SwimmingPool2017\gdb\general_data.gdb\GISDBA_SCL_STREETS'
    
    fcs = arcpy.ListFeatureClasses()
    arcpy.MakeFeatureLayer_management(projectAreaTiles, 'TileClipLayer')
    for fc in fcs:
        print 'clipping ' + fc
        arcpy.MakeFeatureLayer_management(fc, 'lyr')
        arcpy.AddField_management('lyr', 'YARD', 'TEXT', '', '', '5')
        arcpy.AddField_management('lyr', 'TILENAME', 'Text', '', '', '8')
        arcpy.AddField_management('lyr', 'ERROR_TYPE', 'SHORT')
        arcpy.SelectLayerByAttribute_management('TileClipLayer', 'NEW_SELECTION', "BOOKSEC_PT = 'o" + fc[4:] + "'")

        arcpy.Clip_analysis(fc, 'TileClipLayer', outClippedBlendedWS + '\\' + fc + '_Clip')
        arcpy.SelectLayerByAttribute_management('TileClipLayer', 'CLEAR_SELECTION')
        
    env.workspace = outClippedBlendedWS
    env.overwriteOutput = True

    fcs = arcpy.ListFeatureClasses()
    arcpy.MakeFeatureLayer_management(projectAreaParcels, 'ProjAreaAOXLyr')
    arcpy.MakeFeatureLayer_management(GISDBASCL, 'GISDBA_SCL_STREETS')
    for fc in fcs:
        print "Performing Identity and Near Analysis on " + fc + "_Id"
        arcpy.Identity_analysis(fc, 'ProjAreaAOXLyr', outClippedBlendedIDWS + '\\' + fc + '_Id', 'ALL', '', 'NO_RELATIONSHIPS')
        arcpy.Near_analysis(outClippedBlendedIDWS + '\\' + fc+'_Id', 'GISDBA_SCL_STREETS', "300 Feet", "LOCATION", "NO_ANGLE", "PLANAR")


    env.workspace = outClippedBlendedIDWS
    env.overwriteOutput = True
    arcpy.MakeFeatureLayer_management(GISDBASCL, 'GISDBA_SCL_STREETS')
    fcs = arcpy.ListFeatureClasses()
    for fc in fcs:
        print "calculating frequency and stats on " + fc
        arcpy.MakeFeatureLayer_management(fc, 'lyr')
        arcpy.AddJoin_management('lyr', "NEAR_FID", 'GISDBA_SCL_STREETS', 'OBJECTID', 'KEEP_ALL')
        arcpy.Frequency_analysis('lyr', outClippedBlendedIDWS + '\\' + fc[:-8] + '_Frequen', '"{}.gridcode;{}.APN"'.format(fc,fc), '"{}.Shape_Area"'.format(fc))

        arcpy.Statistics_analysis(outClippedBlendedIDWS + '\\' + fc[:-8] + '_Frequen', outClippedBlendedIDWS + '\\' + fc[:-8] + '_TOTAREA', "FREQUENCY COUNT;"+"{i}_Shape_Area SUM".format(i=fc), "{x}_APN".format(x=fc))

        


                


def create_blended_review_fc():
    env.workspace = step3_filtered2_ws

    fcs2 = arcpy.ListFeatureClasses()

    for fc in fcs2:
        for i in range(0, len(step_4_fc_list)):
            
            if step_4_fc_list[i][6:] == fc[6:14]:
            #create empty feature class with necessary fields
                print "combining " + step_4_fc_list[i][6:] + " and " + fc[6:14]
                arcpy.CreateFeatureclass_management(outBlendedWS, 'Rev_' + fc[6:14], 'POLYGON', '', '', '',spatial_reference="PROJCS['NAD_1983_StatePlane_Nevada_East_FIPS_2701_Feet',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',656166.6666666665],PARAMETER['False_Northing',26246666.66666666],PARAMETER['Central_Meridian',-115.5833333333333],PARAMETER['Scale_Factor',0.9999],PARAMETER['Latitude_Of_Origin',34.75],UNIT['Foot_US',0.3048006096012192]];-17790500 -19184900 3048.00609601219;-100000 10000;-100000 10000;3.28083333333333E-03;0.001;0.001;IsHighPrecision" )
                arcpy.AddField_management(outBlendedWS + '\\' + 'Rev_' + fc[6:14], 'Id', 'LONG')
                arcpy.AddField_management(outBlendedWS + '\\' + 'Rev_' + fc[6:14], 'gridcode', 'LONG')
                arcpy.Append_management(fc, outBlendedWS + '\\' + 'Rev_' + fc[6:14], 'NO_TEST')
                arcpy.Append_management(step4_ws + '\\' + step_4_fc_list[i], outBlendedWS + '\\' + 'Rev_' + fc[6:14], 'NO_TEST')
                
            elif ('b1b3_o' + fc[6:14]) not in step_4_fc_list:
                print "just outputing " + fc[6:11]
                arcpy.CreateFeatureclass_management(outBlendedWS, 'Rev_' + fc[6:14], 'POLYGON')
                arcpy.AddField_management(outBlendedWS + '\\' + 'Rev_' + fc[6:14], 'Id', 'LONG')
                arcpy.AddField_management(outBlendedWS + '\\' + 'Rev_' + fc[6:14], 'gridcode', 'LONG')
                arcpy.Append_management(fc, outBlendedWS + '\\' + 'Rev_' + fc[6:14], 'NO_TEST')

    further_process_blended()



    










env.workspace = step4_ws


fcs = arcpy.ListFeatureClasses()
step_4_fc_list = []

print "Building step fc list to create blended fc"
for fc in fcs:
    step_4_fc_list.append(fc)

create_blended_review_fc()
























        
    
