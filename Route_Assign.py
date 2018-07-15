# import modules

import pandas as pd
import numpy as np
import os

# get max route counts per blockface

rts_f1 = rts.loc[rts['z1tims'] < 2]
mxRt = rts_f1.groupby(['ref_id_side', 'route']).size().reset_index(name='count')
mxRt = mxRt.sort_values(by=(['ref_id_side', 'count']))
mxRt = mxRt.drop_duplicates('ref_id_side', keep='last')

mxRt.head(5)
mxRt.to_csv(r"C:\Data\maxGarb.csv", index=False)
type(mxRt)
len(mxRt)

def get_mode(group):
    return group.mode()[0]

rts_f1 = rts.loc[rts['z1tims'] < 2]
merged = rts_f1.merge(rts_f1.groupby(['ref_id_side'])['route'].apply(get_mode).reset_index(), how='left', indicator=True)
merged[merged['_merge'] != 'both'].groupby(['ref_id_side', 'route']).size().to_csv(r"C:\Data\noMaxGarb.csv")

fix = merged[merged['_merge'] != 'both'].groupby(['ref_id_side', 'route']).size()
len(fix)


final = rts_f1.merge(mxRt)
final.to_csv(r"C:\Data\FixGarb.csv")
len(final)