# This script reads the CaseRates field values and determines the natural breaks for the ranges 
# and then replaces the symbology values in an associated webmap JSON file to update webmap

# need to call pyhton from the environment where ArcGIS Pro allows third party library installs 
# to access all the necessary modules in the script
import sys

sys.path.append(r'C:\arcgispro-py3-clone2')

# import remaining modules

try:
    from arcgis import GIS
    import arcpy, json, jenkspy

    print ("imported modules")

    # set up environmental geodatabase using prod-replication query
    arcpy.env.workspace = r'C:\Data\env_db.sde'

    # create layer variable for search cursor
    lyr = r'C:\Data\env_db.sde\Alco_CaseRatesByZip'

    # create list to store case rate values

    cRates = []

    with arcpy.da.SearchCursor(lyr, "CaseRates") as rows:
        for row in rows:
            if row[0] != None:
                if row[0] >= 10:
                    cRates.append(row[0])

    # use jenkspy to calculate natural breaks for new values

    breaks = jenkspy.jenks_breaks(cRates, 5)

    # round breaks to nearest tenth

    rBreaks = []

    for i in breaks:
        rBreaks.append(round(i,1))

    # create value brackets to put in JSON where b = bin value
    b1 = str(rBreaks[0]) + " " +"to "+ str(rBreaks[1])
    b2 = "> " + str(rBreaks[1]) + " " +"to "+ str(rBreaks[2])
    b3 = "> " + str(rBreaks[2]) + " " +"to "+ str(rBreaks[3])
    b4 = "> " + str(rBreaks[3]) + " " +"to "+ str(rBreaks[4])
    b5 = "> " + str(rBreaks[4]) + " " +"to "+ str(rBreaks[5])

    bins = [b1, b2, b3, b4, b5]

    print ("jenks calculated")
    # open json file:

    jFile = r"C:\Data\CaseRates_BU.json"

    obj  = json.load(open(jFile))

    infoBreaks = obj['operationalLayers'][1]['layerDefinition']['drawingInfo']['renderer']['classBreakInfos']

    count = 0

    for b in infoBreaks:
        infoBreaks[count]['classMaxValue'] = breaks[count+1]
        infoBreaks[count]['label'] = bins[count]
        count +=1

    obj['operationalLayers'][1]['layerDefinition']['drawingInfo']['renderer']['minValue'] = rBreaks[0]

    # make update json file

    uJSON = r"C:\Data\Data\CaseRates_Update.json"

    with open(uJSON, "w") as f:
        json.dump(obj, f)

    f.close()

    print ("Json ready")

    # update webmap layer symbology with updated JSON file
    def search_item(conn,layer_name):
        search_results = conn.content.search(layer_name, item_type='Web Map')
        proper_index = [i for i, s in enumerate(search_results) if 
                        '"'+layer_name+'"' in str(s)]
        found_item = search_results[proper_index[0]]
        get_item = conn.content.get(found_item.id)
        return get_item

    def update_wm_layerdef(item):
        item_data = item.get_data()

        # Open JSON file containing symbology update
        with open(uJSON) as json_data:
            data = json.load(json_data)

        # Set the item_properties to include the desired update
        item_properties = {"text": json.dumps(data)}

        # 'Commit' the updates to the Item
        item.update(item_properties=item_properties)

        new_item_data = item.get_data()

    def main():
        conn = GIS("https://arcgis.com","MyOrg","MyPassWord") 
        
        # Search for item, get item data
        item = search_item(conn, 'COVID-19 Case Rates By Zip Code')
        update_wm_layerdef(item)

        print ("successful")

    if __name__ == '__main__':
        sys.exit(main())

except:
    print(sys.exc_info())