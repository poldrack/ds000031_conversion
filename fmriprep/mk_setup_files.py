"""
create json files for each set of resting runs 
"""

import json
from bids import BIDSLayout

d = {"bold": {"task": ["rest"]}} 

layout = BIDSLayout('/data/fmri-handbook-2e-data/bids')

rest_sessions = layout.get(task='rest',extension='nii.gz')

sesslist = []

for i in rest_sessions:
    sess = i.path.split('/')[5]
    sesslist.append(sess)

sesslist = [i.replace('ses-', '') for i in list(set(sesslist))]
listlen = 20
sesslist_splits = [sesslist[x:x+listlen] for x in range(0, len(sesslist), listlen)]

for i in range(len(sesslist_splits)):
    d_split = d.copy()
    d_split['bold']['session'] = sesslist_splits[i]
    with open('rest_set%d.json' % i, 'w') as f:
        json.dump(d_split, f)