# This script uses an ArcGIS Pro project to loop through mp objects and overwrite ArcGIS Online services sharing the same name
# in their service definition files

# import modules
import arcpy
import os, sys, json, urllib.request
from arcgis.gis import GIS
from arcgis.features import FeatureLayerCollection as FLC

# set environmental variables
arcpy.env.overwriteOutput = True

# variable for ArcPro project with all of the feature service maps
prj = r"C:\Data\Replication.aprx"
print ("defining variables")

# make a list of maps representing the feature services to be overwritten
prj = arcpy.mp.ArcGISProject(prj)
mp = prj.listMaps()
print("set up mp object")

# staging area for draft service definition files
relPath = 'C:\\Temp'
print( "relative path = " + relPath)

# credentials to acces AGOL
portal = "https://www.arcgis.com" # Can also reference a local portal
user = "MyOrg"
password = "MyPassWord"

# get token for url in case there are secured services to overwrite
print("Connecting to {}".format(portal))
gis = GIS(portal, user, password)
token = gis._con.token

# Also need to connect to AGOL using arcpy.SignInToPortal for some reason as the GIS method fails to connect to the portal at .exportToSDDraft
# This will create an Oauth token that lasts for 24 hours.
arcpy.SignInToPortal(portal, user, password)
print ("sign in successful")

# query used to extract feature service metadata
url1a = r"https://someservices.arcgis.com/###########/ArcGIS/rest/services/"
url1b = r"/FeatureServer/info/itemInfo?f=pjson&token=" + "{}".format(token)

# editing info
url2a = r"https://someservices.arcgis.com/###########/ArcGIS/rest/services/"
url2b = r"/FeatureServer/0?f=pjson&token=" + "{}".format(token)

# list through project maps to update/overwrite existing feature services
for m in mp:
    sd_fs_name = m.name
    # construct json urls to reteive service definition parms
    url1 = '{}{}{}'.format(url1a, sd_fs_name.replace(' ','_'), url1b)
    url2 = '{}{}{}'.format(url2a, sd_fs_name.replace(' ','_'), url2b)

    with urllib.request.urlopen(url1) as http_response1:
        data = json.loads(http_response1.read().decode())
        # data is the dict whose keys hold the parm values

    with urllib.request.urlopen(url2) as http_response2:
        editInfo = json.loads(http_response2.read().decode())
        # editInfo is the dict that exposes the editing capabilities

    # get editInfo['capabilities'] before overwriting service definition or you will lose these parms
    capabilities = editInfo['capabilities']

    sddraft = os.path.join(relPath, m.name + ".sddraft")
    print (sddraft)
    sd = os.path.join(relPath, "tempPub1.sd")
    # temporary sd file, placeholder

    print("Creating SD file")

    # get parms/metadata for SD draft
    sharing_draft = m.getWebLayerSharingDraft("HOSTING_SERVER", "FEATURE", sd_fs_name)
    sharing_draft.summary = data['snippet']
    sharing_draft.tags = data['tags']
    sharing_draft.description = data['description']
    sharing_draft.credits = data['accessInformation']
    sharing_draft.useLimitations = data['licenseInfo']

    sharing_draft.exportToSDDraft(sddraft)
    arcpy.StageService_server(sddraft, sd)

    # Find the SD, update it, publish /w overwrite and set sharing and metadata
    print("Search for original SD on portal…")
    print(f"Query: {sd_fs_name}")
    sdItem = gis.content.search(query=sd_fs_name, item_type="Service Definition")
    i=0
    while sdItem[i].title != sd_fs_name:
        i += 1
    print('Item Found')
    print(f'item[i].title = {sdItem[i].title}, sd_fs_name = {sd_fs_name}')
    item = sdItem[i] 
    item.update(data=sd)

    print("Overwriting existing feature service…")
    fs = item.publish(overwrite=True)
    print ("Feature service overwritten.")

    if data['access'] == 'public':
        shrEveryone = True
    else:
        shrEveryone = False

    fs.share(everyone=shrEveryone)


    # now we need to restore editing capabilities prior to the feature layer getting overwritten
    search_result= gis.content.search(m.name, "Feature Layer")
    test_item= search_result[0]
    test_flc = FLC.fromitem(test_item)
    update_dict = {"capabilities": capabilities}
    test_flc.manager.update_definition(update_dict)

    # clear out json objects
    data.clear()
    editInfo.clear()
    http_response1.close()
    http_response2.close()

    print (sdItem[i].title +' service successfully updated')
