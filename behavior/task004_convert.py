"""
convert language task files to BIDS events.tsv format
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
    orig_path = repo_path / Path('behavior/data/orig/task_behavior/task004/origfiles')

    datafiles = [i for i in orig_path.glob('*.csv')]
    datafiles.sort()


    outdir = repo_path / Path('behavior/data/task004')
    if not outdir.exists():
        outdir.mkdir()


    fixation_duration = 18
    sent_duration = 6
    probe_delay = 4.
    for datafile in datafiles:
        sesnum = int(datafile.name.split('_')[1])
        data = pd.read_csv(datafile)
        t = 0.3 # start with a .3 sec offset
        onsets = []
        probe_onsets = []
        for trial in data.index:
            if data.loc[trial, 'condition'] == 'fixation':
                t += fixation_duration
            elif data.loc[trial, 'condition'] in ['Sent', 'Nonw']:
                onsets.append(t)
                probe_onsets.append(t + probe_delay)
                t += sent_duration

        trialdata = data.query('condition != "fixation"')
        trialdata['onset'] = onsets
        trialdata['probe_onsets'] = probe_onsets
        trialdata.rename({'condition': 'stimulus_type', 'rt': 'response_time'}, axis=1, inplace=True)

        trial_event_df = trialdata[['onset', 'stimulus_type', 'accuracy']]
        trial_event_df['response_time'] = 'n/a'
        trial_event_df['trial_type'] = 'sentence'
        trial_event_df['duration'] = 4
        probe_event_df = trialdata[['probe_onsets',  'stimulus_type', 'accuracy', 'response_time']].rename(
            {'probe_onsets': 'onset'}, axis=1)
        probe_event_df['trial_type'] = 'probe'
        probe_event_df['duration'] = 1
        
        all_events_df = pd.concat((trial_event_df, probe_event_df))
        all_events_df = all_events_df.sort_values('onset')
        # save resulting dataframe as tsv file
        outfile = outdir / ('sub-01_ses-%03d_task-language_run-1_events.tsv' % sesnum)
        if outfile.exists():
            print('warning: overwriting existing outfile', outfile.name)
        all_events_df.to_csv(outfile,
                        sep = '\t', index = False)
