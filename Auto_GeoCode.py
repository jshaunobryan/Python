# This script is intended to appply some of the troubleshooting techniques to geocode addresses
# with data entry errors in the zip code. Should only be ran after city names have been corrected.
# See Correct_Place_Spelling.py

# import arcpy library
import arcpy

arcpy.Delete_management("fcLayer")

# The featureclass containing the bad addresses
fc = raw_input("Enter service location: ")
arcpy.MakeFeatureLayer_management(fc, "fcLayer")
print "made layer"

# The featureclass or table containing the correct zip codes and city names 
pTable = raw_input("Enter table with correct place names and zips: ")

# Create values for query to be used in the rematch process
QF1 = "Status"
QF2 = "CorPlace"
QV1 = "U"

# Make a set of unique place names

pSet = set()
with arcpy.da.SearchCursor(fc,"CorPlace") as cursor:
    for row in cursor:
        pSet.add(row[0])

# convert set to a list so list properties can be applied
pList = []
for i in pSet:
	pList.append(i)

# loop through each place name to fix zip codes so that an address match can be made
try: 
    for x in pList:
        print x
        QV2 = x
        with arcpy.da.SearchCursor(pTable,['NAME','GEOID10']) as rows:
            # Build a list of unique zip codes for the current place
            zipSet = set()
            zipList = []
            for row in rows:
                if row[0] == x:
                    zipSet.add(row[1])
            for i in zipSet:
                zipList.append(i.encode("utf-8"))
            print zipList
            if len(zipList) > 0:
                for i in zipList: # For the current place loop through each of it's zip codes, and apply the rematch after changing the zip code
                    print i
                    WC = """{0} = '{1}' AND {2} = '{3}' """.format(QF1,QV1, QF2, QV2)
                    with arcpy.da.UpdateCursor("fcLayer", ['RS_Postal_Code'], WC) as cursor:
                        for cell in cursor:
                            cell[0] = i
                            cursor.updateRow(cell)
                    arcpy.SelectLayerByAttribute_management("fcLayer", "NEW_SELECTION", WC)
                    selCount = arcpy.GetCount_management("fcLayer")
                    print selCount
                    if selCount > 0:
                        arcpy.geocoding.RematchAddresses(fc, WC)
                    arcpy.SelectLayerByAttribute_management("fcLayer", "NEW_SELECTION",""""Status" = 'U'""")
                    unGeoCount = arcpy.GetCount_management("fcLayer")
                    print "Unmatched addresses = " + str(unGeoCount)
                    arcpy.SelectLayerByAttribute_management("fcLayer", "CLEAR_SELECTION")

except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))
arcpy.Delete_management("fcLayer")
    