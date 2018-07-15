import collections
import xlrd

#open workbook to get values
wb1 = xlrd.open_workbook(r"S:\Shared\RouteSmart\Misc Projects\RouteReady\Rate Code Cleanup\RS10_CO73_All_08102016.xlsx")
sh1 = wb1.sheet_by_index(0)

#Open a rate code workbook
wb2 = xlrd.open_workbook(r"S:\Shared\RouteSmart\Misc Projects\RouteReady\Rate Code Cleanup\SanMateo_Rates_Routes.xlsx")
sh2 = wb2.sheet_by_index(0)

#make a lists

roLst = []
raLst = []

# polpulate lists

cell_range_value = 0
for value in sh1.col(9):
    cell_range_value += 1
print cell_range_value

for i in range(1,cell_range_value,1):
    roVal = str(sh1.cell(i,9).value)
    raVal = str(sh1.cell(i,19).value)
    cell_value_id = sh1.cell(i,1).value
    roLst.append(roVal)
    raLst.append(raVal)

#make multivalue dict1
RoRaDct = collections.defaultdict(set)

for key, item in zip(roLst,raLst):
    RoRaDct[key].add(item)

print RoRaDct

#make multivalue dict2

fType = []
rtLst2 = []

cell_range_value = 0
for value in sh2.col(0):
    cell_range_value += 1

for i in range(1,cell_range_value,1):
    fVal = str(sh2.cell(i,1).value)
    rtVal = str(sh2.cell(i,0).value)
    cell_value_id = sh2.cell(i,1).value
    fType.append(fVal)
    rtLst2.append(rtVal)

TpRtDct = collections.defaultdict(set)

#check values

for key, item in zip(fType,rtLst2):
    TpRtDct[key].add(item)

print TpRtDct

Types = set(TpRtDct)

RateByType = collections.defaultdict(list)

for key in TpRtDct:
    for k in TpRtDct[key]:
        RateByType[key].extend(RoRaDct[k])

for key, item in RateByType.items():
    print key, item





