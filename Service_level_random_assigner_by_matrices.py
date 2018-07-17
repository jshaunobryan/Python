# This script allows you to randomly assign phenomena to a population represented by an ArcMap featureclass 
# specified by values in a two matrices stored in excel spreadsheets

import xlrd
import random
import arcpy

## Setup
# Define random selection function

def SelectRandomByCount (layer, count):
    layerCount = int (arcpy.GetCount_management (layer).getOutput (0))
    if layerCount < count:
        print "input count is greater than layer count"
        print "number of selection: " + str(arcpy.GetCount_management (layer))
        return
    oids = [oid for oid, in arcpy.da.SearchCursor (layer, "OID@")]
    oidFldName = arcpy.Describe (layer).OIDFieldName
    path = arcpy.Describe (layer).path
    delimOidFld = arcpy.AddFieldDelimiters (path, oidFldName)
    randOids = random.sample (oids, count)
    oidsStr = ", ".join (map (str, randOids))
    sql = "{0} IN ({1})".format (delimOidFld, oidsStr)
    arcpy.SelectLayerByAttribute_management (layer, "", sql)
    print "number of selection: " + str(arcpy.GetCount_management (layer))

# Define 'make a matrix function'

def makeMatrix(wbi):
    wb = xlrd.open_workbook(wbi)
    sh = wb.sheet_by_index(0)

    # Get column range value
    column_range_value = 0
    for i in sh.row(0):
        column_range_value += 1
    column_range_value = column_range_value - 1
    print column_range_value

    # Get row range value
    row_range_value = 0
    for i in sh.col(0):
        row_range_value += 1
    row_range_value = row_range_value -1
    print row_range_value

    for i in range(0,column_range_value,1):
        for j in range(0,row_range_value,1):
            if sh.cell(j+1,i+1).value != '':
                #print sh.cell(j+1,i+1).value
                key = str(sh.cell(0,i+1).value)+"_"+str(sh.cell(j+1,0).value)
                #print key
                serParams[key] = sh.cell(j+1, i+1).value

# Define random assigner

def assignRandom(fc, WC):
    lyr = arcpy.MakeFeatureLayer_management(fc,"lyr")
    arcpy.GetCount_management(lyr)

    for k, v in serParams.items():
        print k, v
        # break dict items into input values
        v1 = k.split("_")[0]
        v2 = k.split("_")[1]
        v3 = int(v)
        
        # make a where clause that will select features that have not been populated yet
        
        arcpy.SelectLayerByAttribute_management(lyr, "NEW_SELECTION", WC)

        # pass in values to SelectRandomByCount
        SelectRandomByCount(lyr, v3)

        # update fields
        with arcpy.da.UpdateCursor(lyr, [upF1, upF2]) as cursor:
            for row in cursor:
                row[0] = v1
                row[1] = v2
                cursor.updateRow(row)
        arcpy.SelectLayerByAttribute_management(lyr, "CLEAR_SELECTION")
    arcpy.Delete_management(lyr)

# Designate default workspace

ws = raw_input("Enter path workspace: ")

arcpy.env.workspace = ws

# Create program variables

fc = raw_input("Enter path to featureclass: ")

serT = raw_input("Enter service type: ")
serF = raw_input("Provide field name describing service type: ")
compF = raw_input("Enter field name representing compaction: ")
upF1 = raw_input("Enter service frequency field: ")
upF2 = raw_input("Enter bin size field: ")
wb1 = raw_input("Enter path to matrix worksheet: ")
wb2 = raw_input("Enter path to matrix worksheet: ")
blank = "Null"
wc1 = """ {} IS {} AND {} IS {}""".format(upF1, blank, compF, blank)
print wc1
wc2 = """ {} IS {} AND {} IS NOT {}""".format(upF1, blank, compF, blank)
params = [[wb1,wc1],[wb2,wc2]]

# Call functions
for p in params:
    serParams = {}
    makeMatrix(p[0])
    assignRandom(fc, p[1])
    print p[1]

print "Done!"



    
    

        
        
        
        
    