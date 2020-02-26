import arcpy
from arcpy import env


ws = r'D:\SwimmingPool2017\Process_dataForFinal\QA_point_class.gdb'
env.workspace = ws
env.overwriteOutput = True
parcelData = r'D:\SwimmingPool2017\Process_dataForFinal\general_data.gdb\parcels_AOX_110LU'
outputData = r'D:\SwimmingPool2017\Process_dataForFinal\FinalQA_Points.gdb'

arcpy.MakeFeatureLayer_management(parcelData, 'ParcelDataLyr')

fcs = arcpy.ListFeatureClasses()

for fc in fcs:
    if len(fc) == 9:
        print fc
        arcpy.MakeFeatureLayer_management(fc,'lyr')

        

        arcpy.Identity_analysis('lyr', 'ParcelDataLyr', outputData + '\\' + fc)

        arcpy.MakeFeatureLayer_management(outputData+ '\\' + fc, 'fc_id_lyr')
        
        arcpy.SelectLayerByAttribute_management('fc_id_lyr', 'NEW_SELECTION', "APN IS NULL")
        arcpy.CalculateField_management('fc_id_lyr', 'APN', "!APN_1!", "PYTHON_9.3")
        arcpy.SelectLayerByAttribute_management('fc_id_lyr', 'CLEAR_SELECTION')
        
        arcpy.DeleteField_management('fc_id_lyr', "FID_parcels_AOX_110LU;APN_1;PARCELTYPE;TAX_DIST;CALC_ACRES;ASSR_ACRES;TXT_ANGLE;LABEL_CLASS;TAXDIST;ETALFLAG;"\
                                     "OWNER;OWNER2;ADDRESS1;ADDRESS2;ADDRESS3;ADDRESS4;ADDRESS5;NAMETAG;ZIPCODE;STRNO;STRFRAC;STRDIR;STRNAME;STRTYPE;STRUNIT;"\
                                     "LANDUSE;CAPACITY;ASSDYR;CONSTYR;DOCDATE;DOCNO;DOCMULTI;DOCVEST;SALEPRICE;SALETYPE;SALEDATE;LANDCD1;LANDACRE1;LANDVAL1;LANDCD2;LANDACRE2;LANDVAL2;IMPVAL;TOTVAL;EXMPTCD;EXMPTVAL;LYLANDVAL;LYIMPVAL;"\
                                     "LYTOTAL;LYEXMPTCD;LYEXMPTVAL;NBRHOOD;ADTYPE;ADFILE;ADPAGE;ADPART;ADBLKCD;ADBLK;ADLOTCD;ADLOT;SECTION;TOWNSHIP;RANGE;MARKAREA;SUBNAME;LANDADJ;STATEADJ;CALCACRES;COMMONNAME;LOTSQFT;ZONE;STATIC;SE_ANNO_CAD_DATA;PARCELADDRESS")

