"""
get lengths for each bold scan
"""

import os
import pandas as pd
from utils import locate


basedir =  '/home/poldrack/data/fmri-handbook-2e-data/bids/.heudiconv'

dicomfiles = [i for i in locate('dicominfo*', basedir)]

data = None
for f in dicomfiles:
    df = pd.read_csv(f, sep='\t')
    if data is None:
        data = df
    else:
        data = pd.concat((data, df))

data.to_csv('data/all_scan_info.csv')