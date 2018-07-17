# Takes features from a RouteSmart service location and assigns it to a truck territory using a spatial join
# Produces report to be used in Tower Go Live. Runs daily.

# import modules

import arcpy, os, time

print" Running Python Script"

# Set up workspace and mxd
workSpace = r"C:\RS_Data\Workspace\BATCH_CO_161_imports\gisdb\layers.gdb"
arcpy.env.workspace = workSpace
arcpy.env.overwriteOutput = True

# make list of attribute fields to reference in sequence join table

inFields = ["UniqueID","Address_ID","Account_ID","X","Y","Ref_ID","Side","Score","Route","Sequence","Service_Day","Demand_2","Demand_3","Week"]


# do a spatial join and then a table join, joining route values and sequences for each type of waste
try:

	comms = ["GarbRes","RecRes","YwRes"]

	layerFCS = []

	for waste in comms:

	# Perform a spatial join so the new routes can be assigned to the map features

		target = r"C:\RS_Data\Workspace\BATCH_CO_161_imports\gisdb\layers.gdb\Service_Location"

		path = r"C:\RS_Data\Workspace\BATCH_CO_161_imports\gisdb\layers.gdb"

		join = os.path.join(path,("{0}{1}".format("Sea_",waste)))

		outFC = "{0}{1}".format("XX_SPJ_", waste)
		print outFC

		arcpy.SpatialJoin_analysis(target, join, outFC)

		layer = "{0}{1}".format("XX_",waste)

		arcpy.MakeFeatureLayer_management(outFC,layer)

		layerFCS.append(layer)
		print layer

	# Select all records in map layer

	for layer in layerFCS:
		valueDI = {}
		arcpy.SelectLayerByAttribute_management(layer,"NEW_SELECTION")

		# Remove relevant commodity codes so they do not get deleted

		if layer == "XX_GarbRes":

			QF1 = '\"Product_Code\"'
			RV1 = '(\'R10T\', \'R10TBP\', \'R10TWP\', \'R20T\', \'R20TBP\', \'R20TWP\', \'R32T\', \'R32TBP\', \'R32TWP\', \'R45T\', \'R45TBY\', \'R45TBP\', \'R45TWP\', \'R64T\', \'R64TBP\', \'R64TWP\', \'R96T\', \'R96TBP\', \'R96TWP\', \'R10TBY\', \'R20TBY\', \'R32TBY\', \'R64TBY\',\'NOSVCGAR\', \'R96TBY\')'
			WC1 = QF1 + ' IN ' + RV1

		elif layer == "XX_RecRes":

			QF1 = '\"Product_Code\"'
			RV1 = '( \'R10R\', \'R10RBP\', \'R20R\', \'R20RBP\', \'R32R\', \'R32RBP\', \'R64R\', \'R64RBP\', \'R96R\', \'R96RBP\', \'R10RBY\', \'R20RBY\', \'R32RBY\', \'R64RBY\', \'R96RBY\', \'R10REC\', \'R20REC\', \'R32REC\', \'R64REC\', \'R96REC\',\'NOSVCREC\')'
			WC1 = QF1 + ' IN ' + RV1

		elif layer == "XX_YwRes":

			QF1 = '\"Product_Code\"'
			RV1 = '(\'R10YW\', \'R13YW\', \'R20YW\', \'R32YW\', \'R64YW\', \'R96YW\', \'R13YWBY\', \'R20YWBY\', \'R32YWBY\', \'R64YWBY\', \'R96YWBY\',  \'R13YWBP\', \'R20YWBP\', \'R32YWBP\', \'R64YWBP\', \'R96YWBP\', \'R13YWWP\', \'R20YWWP\', \'R32YWWP\', \'R64YWWP\', \'R96YWWP\',\'NOSVCYW\')'
			WC1 = QF1 + ' IN ' + RV1

		arcpy.SelectLayerByAttribute_management(layer,"REMOVE_FROM_SELECTION", WC1)

		print "Select 2"

		# Add unmatched records back to selection

		QF2 = "Status"
		RV2 = "M"
		WC2 = """ {} <> '{}'""".format(QF2, RV2)

		arcpy.SelectLayerByAttribute_management(layer,"ADD_TO_SELECTION",WC2)

		print "select 3"

		# Add records with incorrect service day back to selection

		QF3 = "ServDay"
		QF4 = "Service_Day"
		WC3 = """ {} <> {} """.format(QF3, QF4)

		arcpy.SelectLayerByAttribute_management(layer,"ADD_TO_SELECTION",WC3)

		if layer == "XX_RecRes":

			QF5 = "Week"
			QF6 = "FREQUENCY"
			RV3 = '( \'A\', \'B\')'
			WC4 = """{0} = {1} AND {0} IN {2} """.format(QF5,QF6, RV3)  

			arcpy.SelectLayerByAttribute_management(layer,"ADD_TO_SELECTION",WC4)

		arcpy.DeleteFeatures_management(layer)

		# Bring over route values rom spatial join

		with arcpy.da.UpdateCursor(layer,["Route_Name","Route"]) as cursor:
			for row in cursor:
				row[1] = row[0]
				cursor.updateRow(row)

		# Bring over sequence values from Tower ODBC table
		SeqTable = 'S:\\Shared\\RouteSmart\\CO_161_Cleanscapes\\From_Tower\\COS zero sequence and xx route.xlsx'

		arcpy.ExcelToTable_conversion(SeqTable,"Join_Table")

		if layer == "XX_GarbRes":

		    QF7 = "SVCCODE"
		    QV3 = "%T%"
		    WC5 = """ {} LIKE '{}' """.format(QF7, QV3)

		elif layer == "XX_RecRes":

			QF7 = "SVCCODE"
			QV3 = "R%R%"
			WC5 = """ {} LIKE '{}' """.format(QF7, QV3)

		elif layer == "XX_YwRes":

			QF7 = "SVCCODE"
			QV3 = "%YW%"
			WC5 = """ {} LIKE '{}' """.format(QF7, QV3)

		arcpy.MakeTableView_management("Join_Table", "OldSeq", WC5)

		with arcpy.da.UpdateCursor("OldSeq", "CUSTID") as cursor:
			for row in cursor:
				row[0] = str(row[0]) + "001"
				cursor.updateRow(row)
		print "UPDATED ROWS"

		joinFc = "OldSeq"
		joinIdFld = "CUSTID"
		joinValFld = "OLDSEQUENCE"

		valueDi = {x[0]: x[1] for x in arcpy.da.SearchCursor(joinFc, [joinIdFld, joinValFld])}

		with arcpy.da.UpdateCursor(layer, ["Sequence", "Address_ID"]) as cursor:
			for update, key in cursor:
				if not key in valueDi:
					continue
				row = (valueDi[key], key)
				cursor.updateRow(row)
		del cursor

		outPath = 'S:\\Shared\\RouteSmart\\CO_161_Cleanscapes\\To_Tower'
		day = time.strftime("%m%d%Y")
		name = os.path.basename(layer)
		
		dataFields = [i.name for i in arcpy.ListFields(layer)]

		file = os.path.join(outPath, ("{0}{1}{2}".format(day,name,".txt")))
		print file
		f = open(file, "w")

		writeFields = []

		for field in inFields:
		    if field in dataFields:
		        writeFields.append(field)

		for row in arcpy.SearchCursor(layer):
		    # No longer need to reference name property (field.name)

		    fieldVals = [row.getValue(field) for field in writeFields]
		    # Replace nulls with empty strings
		    fieldVals = ['' if i is None else i for i in fieldVals]
		    fieldVals = [str(field) for field in fieldVals]
		    out_string = ','.join(fieldVals)
		    # Write the string--not the list--to the table
		    f.writelines(out_string +"\n")
		del row
		f.close()

	arcpy.Delete_management(layer)
	arcpy.Delete_management("OldSeq")

	print "done"

except arcpy.ExecuteError:
	print(arcpy.GetMessages(2))
