
import os
from pathlib import Path


basedir = '/home/poldrack/data/fmri-handbook-2e-data/bids/sub-01'

for i in range(1, 108):
    bidsdir = Path(basedir) / ('ses-%03d' % i)
    if not bidsdir.exists():
        print('ses-%03d' % i, 'no bidsdir')