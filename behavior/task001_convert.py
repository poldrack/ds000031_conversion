# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 11:22:49 2020

@author: mluec
- refactored and adapted by poldrack
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
    pkl_path = repo_path / Path('behavior/data/orig/task_behavior/task001/origfiles')

    pklfiles = [i for i in pkl_path.glob('*.pkl')]
    # sorting so that files are in temporal order for run numbering
    pklfiles.sort()

    outdir = repo_path / Path('behavior/data/task001')
    if not outdir.exists():
        outdir.mkdir()

    ###############################################################################

    ses_runnum = defaultdict(lambda: 0)

    # iterate over sessions
    for pklfile in pklfiles:
        ses = int(pklfile.name.replace('self-tracking', 'self_tracking').split('_')[2])

        # load original pkl file
        with open(pklfile, 'rb') as f:
            data = pickle.load(f)
        if len(data['trialdata']) < 180:
            print('skipping', pklfile.name)
            continue
        
        # turns out this isn't needed since there is only one good run for each session
        # but I'm leaving it in to be safe
        ses_runnum[ses] += 1

        # create empty lists to be filled below
        onset_list = []
        duration_list = []
        trial_type_list = []
        response_time_list = []
        accuracy_list = []
        stimtype_list = []
        nback_list = []
        
        # fill lists trialwise
        for i in np.arange(len(data['trialdata'])):
        
            # extract trial infos 
            stim_type = data['trialdata'][i]['stim_type']
            block = data['trialdata'][i]['block']
            nback = data['trialdata'][i]['nback']
            onset = data['trialdata'][i]['actual_onset_time']
            duration = data['trialdata'][i]['duration']
            try:
                response = data['trialdata'][i]['response']
            except KeyError:
                response = 'n/a'
            try:
                match = data['trialdata'][i]['match']
            except KeyError:
                match = 'n/a'
            try:
                RT = data['trialdata'][i]['rt']
            except KeyError:
                RT = 'n/a'
            
            # create naming for stimulus type
            if stim_type == "faces":
                event = 'faces_' + str(nback) + 'back'
            if stim_type == "scenes":
                event = 'scenes_' + str(nback) + 'back'
            if stim_type == "chinese_characters":
                event = 'characters_' + str(nback) + 'back'

            
                
            # identify correct responses
            if nback == 1:
                if (match == 1 and response == str(4)) or (match != 1 and response == str(1)):
                    accuracy = 1
                else:
                    accuracy = 0
            elif nback == 2:
                if (match == 2 and response == str(4)) or (match != 2 and response == str(1)):
                    accuracy = 1
                else:
                    accuracy = 0
                
            # add values to respective lists
            onset_list.append(onset)
            duration_list.append(duration)
            trial_type_list.append(event)
            response_time_list.append(RT)
            accuracy_list.append(accuracy)
            stimtype_list.append(stim_type)
            nback_list.append(nback)

        # combine lists into dictionary
        # ...including correct responses
        d = {'onset': onset_list,
            'duration': duration_list,
            'trial_type': trial_type_list,
            'response_time': response_time_list,
            'accuracy': accuracy_list,
            'stimtype': stimtype_list,
            'nback': nback_list}
        # ...without correct responses
    #    d = {'onset': onset_list,
    #         'duration': duration_list,
    #         'trial_type': trial_type_list,
    #         'response_time': response_time_list}
    
        # turn dictionary into dataframe
        events_tsv = pd.DataFrame(d)       
        
        # save resulting dataframe as tsv file
        outfile = outdir / ('sub-01_ses-%03d_task-nback_run-%03d_events.tsv' % (ses, ses_runnum[ses]))
        if outfile.exists():
            print('warning: overwriting existing outfile', outfile.name)
        events_tsv.to_csv(outfile,
                        sep = '\t', index = False)
            
        
        
        

