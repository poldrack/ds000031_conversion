# -*- coding: utf-8 -*-
"""
creation of events.tsv for RDM/stop signal task

"""

import os
import numpy as np
import pandas as pd
import pickle
from pathlib import Path
import git
from collections import defaultdict

if __name__ == "__main__":

    ### DEFINE ####################################################################
    # use repo base directory as base dir
    repo = git.Repo(os.path.dirname(__file__),
                search_parent_directories=True)
    repo_path = Path(repo.git.rev_parse("--show-toplevel"))

    # path to pkl files
    orig_path = repo_path / Path('behavior/data/orig/task_behavior/task002/origfiles')

    datafiles = [i for i in orig_path.glob('stopSigRDM_ses_*.txt')]
    datafiles.sort()


    outdir = repo_path / Path('behavior/data/task002')
    if not outdir.exists():
        outdir.mkdir()

    # created by hand - mapping to session numbers from original 
    ses_dict = {
        1: 83,
        2: 84,
        3: 85,
        4: 86,
        5: 88,
        6: 89,
        7: 91,
        8: 92,
        9: None
        }

    ###############################################################################

    # iterate over sessions
    for datafile in datafiles:
        logfile = datafile.as_posix().replace('_ses_', '_log_ses_')
        ses = int(datafile.name.split('_')[-1].split('.')[0])
        sesnum = ses_dict[ses]
        if sesnum is None:
            continue
        print('processing session', ses, sesnum)
        
        # load data files
        logdata = pd.read_csv(logfile, skiprows=1, sep='\t')
        data = pd.read_csv(datafile, skiprows=1, sep='\t')
        assert data.shape[0] == logdata.shape[0]

        trial_type_list = ['stop' if i == 1 else 'go' for i in data.TrialType]

        logdata['Onset'] = logdata.StimOn - logdata.BlockAncher

        logdata['Duration'] = logdata.StimOff - logdata.StimOn

        response_time_list = ['n/a' if i == 0 else i for i in data.RT.tolist()]

        # create empty lists to be filled below
        accuracy_list = []
        stimtype_list = []
        nback_list = []

        for i in data.index:
            if data.TrialType[i] == 0:
                data.loc[i, 'SSD'] = 'n/a'
                data.loc[i, 'CorrStop'] = 'n/a'
            if data.RT[i] == 0:
                data.loc[i, 'IsCorrect'] = 'n/a'

        # combine lists into dictionary
        d = {'onset': logdata.Onset.tolist(),
            'duration': logdata.Duration.tolist(),
            'trial_type': trial_type_list,
            'response_time': response_time_list,
            'accuracy': data.IsCorrect.tolist(),
            'motion_coherence': data.Coherence.tolist(),
            'SSD': data.SSD.tolist(),
            'stop_success': data.CorrStop.tolist()}

    
        # turn dictionary into dataframe
        events_tsv = pd.DataFrame(d)       
        
        # save resulting dataframe as tsv file
        outfile = outdir / ('sub-01_ses-%03d_task-dots_events.tsv' % sesnum)

        if outfile.exists():
            print('warning: overwriting existing outfile', outfile.name)
        events_tsv.to_csv(outfile,
                        sep = '\t', index = False)
            
        
        
        

