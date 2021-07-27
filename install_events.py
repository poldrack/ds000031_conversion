"""
install events.tsv files into BIDS dir
"""


import os
from utils import locate
import shutil

def parse_filename(fname):
    # return sub, ses, and task
    f_s = fname.split('_')
    sub = int(f_s[0].split('-')[1])
    ses = int(f_s[1].split('-')[1])
    task = f_s[2].split('-')[1]
    if len(f_s) > 3 and 'run' in f_s[3]:
        run = int(f_s[3].split('-')[1])
    else:
        run = 1
    return(sub, ses, task, run)


if __name__ == "__main__":
    bidsdir = '/home/poldrack/data/fmri-handbook-2e-data/bids'

    replacements = [i for i in locate('*events.tsv', 'behavior/data')]

    for f in replacements:
        fname = os.path.basename(f)
        sub, ses, task, run = parse_filename(fname)

        target = os.path.join(
            bidsdir, 'sub-%02d' % sub, 'ses-%03d' % ses, 'func',
            'sub-%02d_ses-%03d_task-%s_run-%d_events.tsv' % (
                sub, ses, task, run))
        match = ""
        if os.path.exists(target):
            match = 'FOUND MATCH'
        print(sub, ses, task, run, match)
        shutil.copy(f, target)

    replace = True
    # find breathhold scans and replace with common file
    bhfiles = [i for i in locate('*breathhold*events.tsv', bidsdir)]
    stub = 'behavior/breathhold_events.tsv'
    for f in bhfiles:
        # replace with the stub
        print('replacing', f, 'with', stub)
        if replace:
            shutil.copy(stub, f)
