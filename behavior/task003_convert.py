"""
convert object localizer files to BIDS events.tsv format
"""

from scipy.io import loadmat
import os
import numpy as np
import pandas as pd
import pickle
from pathlib import Path
import git
from collections import defaultdict
import re

if __name__ == "__main__":

    ### DEFINE ####################################################################
    # use repo base directory as base dir
    repo = git.Repo(os.path.dirname(__file__),
                search_parent_directories=True)
    repo_path = Path(repo.git.rev_parse("--show-toplevel"))

    # path to pkl files
    orig_path = repo_path / Path('behavior/data/orig/task_behavior/task003/origfiles')

    datafiles = [i for i in orig_path.glob('sess*/*.mat')]
    datafiles.sort()


    outdir = repo_path / Path('behavior/data/task003')
    if not outdir.exists():
        outdir.mkdir()


    for datafile in datafiles:
        sesnum = int(datafile.as_posix().split('/')[-2].lstrip('sess'))
        run = int(datafile.name.split('_')[-1].split('.')[0][-1])
        data = loadmat(datafile)
        subinfo = data['theSubject'][0][0]
        taskscript = subinfo[12][0].split('\n')
        trialinfo = [i.split('\t') for i in taskscript[8:] if not i[0] == '*']
        trialinfo_df = pd.DataFrame(trialinfo,
                                    columns=['block', 'onset', 'stimclass', 'is_target', 'stim'])
        trialinfo_df['is_target'] = [int(i.strip()) for i in trialinfo_df.is_target]
        trialinfo_df['stimclass'] = [int(i.strip()) for i in trialinfo_df.stimclass]
        trialinfo_df['trial_type'] = [i.lstrip().strip().split('-')[0] for i in trialinfo_df.stim]
        # remove numbers from face1/face2
        trialinfo_df['trial_type'] = [re.sub(r'[0-9]', '', i) for i in trialinfo_df['trial_type']]
        del trialinfo_df['stimclass']
        del trialinfo_df['stim']

            # save resulting dataframe as tsv file
        outfile = outdir / ('sub-01_ses-%03d_task-objects_events.tsv' % sesnum)
        if outfile.exists():
            print('warning: overwriting existing outfile', outfile.name)
        trialinfo_df.to_csv(outfile,
                        sep = '\t', index = False)
