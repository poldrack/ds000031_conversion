"""
convert spatial wm  task files to BIDS events.tsv format
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
    orig_path = repo_path / Path('behavior/data/orig/task_behavior/task005/origfiles')

    datafiles = [i for i in orig_path.glob('*.csv')]
    datafiles.sort()


    outdir = repo_path / Path('behavior/data/task005')
    if not outdir.exists():
        outdir.mkdir()


    for datafile in datafiles:
        sesnum = int(datafile.name.split('_')[1])
        data = pd.read_csv(datafile)

        trial_df = data[['TrialOnset', 'Condition']].rename(
            {'TrialOnset': 'onset', 'Condition': 'condition'}, axis=1
        )
        trial_df['trial_type'] = 'spatial'
        trial_df['duration'] = 4.5
        trial_df['response_time'] = 'n/a'

        probe_df = data[['ChoiceOnset', 'Condition', 'RT']].rename(
            {'ChoiceOnset': 'onset', 'Condition': 'condition', 'RT': 'response_time'}, axis=1
        )
        probe_df['trial_type'] = 'probe'
        probe_df['duration'] = 1
        
        all_events_df = pd.concat((trial_df, probe_df))
        all_events_df = all_events_df.sort_values('onset')
        # save resulting dataframe as tsv file
        outfile = outdir / ('sub-01_ses-%03d_task-language_run-1_events.tsv' % sesnum)
        if outfile.exists():
            print('warning: overwriting existing outfile', outfile.name)
        all_events_df.to_csv(outfile,
                        sep = '\t', index = False)
