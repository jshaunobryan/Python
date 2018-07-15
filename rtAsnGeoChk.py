
# this is a dict of street links with the 
dict1 = {"LinkID4": [{101:65, 107: 2}],"linkID1":[{101:20, 102:5}], "linkID2":[{101:4}],"linkID3":[{101:15, 102:14, 103:1}]}

# create a container to store the route numbers with the less stop counts for link IDs that have 
# have more than one route:counts pairing
chkDct = {}


# iterate through links. for each list item (a list of dicts) if there is more than one dict in the list,
# delete the dict with the maximum count. If the list only has one dict, delete the entire item.

# begin iteration on main dict
for links, list1 in dict1.items():
	# iterate through each value item in the main dict (a list of dicts) 
	for dicts in list1: 			
	# dItems are the dicts in rtCts
		#print dicts, ": - dicts length: ",  str(len(dicts))
		if len(dicts) > 1:
			del dicts[max(dicts, key=dicts.get)]
			chkDct[links] = dicts
			             

print "chkDct: ", chkDct

def get_mode(group):
    return group.mode()[0]

merged = rts.merge(rts.groupby(['ref_id'])['route'].apply(get_mode).reset_index(), how='left', indicator=True)
merged[merged['_merge'] != 'both'].groupby(['ref_id', 'route']).size()