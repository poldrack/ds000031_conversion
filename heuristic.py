import os


def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes


def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where

    allowed template fields - follow python string module:

    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """

    # paths in BIDS format
    t1w = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_T1w')
    t2w = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_T2w')
    pdt2 = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_PDT2')

    rest = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_run-{item:01d}_bold')
    sbref_rest = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_run-{item:01d}_sbref')

    nback = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-nback_run-{item:01d}_bold')
    sbref_nback = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-nback_run-{item:01d}_sbref')

    dots = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-dots_run-{item:01d}_bold')
    sbref_dots = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-dots_run-{item:01d}_sbref')

    breath = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-breathhold_run-{item:01d}_bold')
    sbref_breath = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-breathhold_run-{item:01d}_sbref')

    superloc = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-language_run-{item:01d}_bold')
    sbref_superloc = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-language_run-{item:01d}_sbref')

    hardeasy = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-spatialwm_run-{item:01d}_bold')
    sbref_hardeasy = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-spatialwm_run-{item:01d}_sbref')

    hardeasy = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-spatialwm_run-{item:01d}_bold')
    sbref_hardeasy = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-spatialwm_run-{item:01d}_sbref')

    dwi_rl = create_key('sub-{subject}/{session}/dwi/sub-{subject}_{session}_dir-RL_run-{item:01d}_dwi')
    sbref_dwi_rl = create_key('sub-{subject}/{session}/dwi/sub-{subject}_{session}_dir-RL_run-{item:01d}_sbref')
    dwi_lr = create_key('sub-{subject}/{session}/dwi/sub-{subject}_{session}_dir-LR_run-{item:01d}_dwi')
    sbref_dwi_lr = create_key('sub-{subject}/{session}/dwi/sub-{subject}_{session}_dir-RL-_run-{item:01d}_sbref')

    se_fmap_ap = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_dir-AP_run-{item:01d}_epi')
    se_fmap_pa = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_dir-PA_run-{item:01d}_epi')
    
    gre_fmap_mag = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_magnitude')
    gre_fmap_phasediff = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_phasediff')
    

    # data = create_key('run{item:03d}')
    info = {t1w: [], t2w: [], rest: [], sbref_rest: [], 
            dwi_lr: [], dwi_rl: [], sbref_dwi_lr: [], sbref_dwi_rl: [],
            se_fmap_ap: [], se_fmap_pa: [],
            gre_fmap_mag: [], gre_fmap_phasediff: [],
            pdt2: [],
            sbref_nback: [], nback: [],
            sbref_dots: [], dots: [],
            sbref_breath: [], breath: [], 
            sbref_superloc: [], superloc: [],
            sbref_hardeasy: [], hardeasy: []
            }
    last_run = len(seqinfo)

    for s in seqinfo:
        """
        The namedtuple `s` contains the following fields:

        * total_files_till_now
        * example_dcm_file
        * series_id
        * dcm_dir_name
        * unspecified2
        * unspecified3
        * dim1
        * dim2
        * dim3
        * dim4
        * TR
        * TE
        * protocol_name
        * is_motion_corrected
        * is_derived
        * patient_id
        * study_description
        * referring_physician_name
        * series_description
        * image_type
        """
        if 'Resting State fMRI' in s.series_description:
            if 'SBRef' in s.series_description:
                info[sbref_rest].append(s.series_id)
            else:
                info[rest].append(s.series_id)
        elif "N Back fMRI" in s.series_description:
            if 'SBRef' in s.series_description:
                info[sbref_nback].append(s.series_id)
            else:
                info[nback].append(s.series_id)
        elif "dots_motion" in s.series_description:
            if 'SBRef' in s.series_description:
                info[sbref_dots].append(s.series_id)
            else:
                info[dots].append(s.series_id)
        elif "Breath_Hold" in s.series_description:
            if 'SBRef' in s.series_description:
                info[sbref_breath].append(s.series_id)
            else:
                info[breath].append(s.series_id)
        elif "superloc" in s.series_description:
            if 'SBRef' in s.series_description:
                info[sbref_superloc].append(s.series_id)
            else:
                info[superloc].append(s.series_id)
        elif "hard_easy" in s.series_description:
            if 'SBRef' in s.series_description:
                info[sbref_hardeasy].append(s.series_id)
            else:
                info[hardeasy].append(s.series_id)

        elif ("MDDW" in s.series_description) and ('TRACE' not in s.series_description):
            direction = 'lr' if 'L-R' in s.series_description else 'rl'
            if "SBRef" in s.series_description:
                if direction == 'lr':
                    info[sbref_dwi_lr].append(s.series_id)
                else:
                    info[sbref_dwi_rl].append(s.series_id)
            else:
                if direction == 'lr':
                    info[dwi_lr].append(s.series_id)
                else:
                    info[dwi_rl].append(s.series_id)

        elif "MB-SE_FieldMap_A-P" in s.series_description:
            info[se_fmap_ap].append(s.series_id)
        elif "MB-SE_FieldMap_P-A" in s.series_description:
            info[se_fmap_pa].append(s.series_id)

        elif "gre_field_mapping" in s.series_description:
            if s.dim3 > 68:
                info[gre_fmap_mag].append(s.series_id)
            else:
                info[gre_fmap_phasediff].append(s.series_id)

        elif "PD-T2" in s.series_description:
            info[pdt2] = [s.series_id] # assign if a single scan meets criteria
        elif 'T1w' in s.series_description:
            info[t1w] = [s.series_id] # assign if a single scan meets criteria
        elif 'T2w' in s.series_description:
            info[t2w] = [s.series_id] # assign if a single scan meets criteria

        else:
            print('unmatched:', s.series_description)
        # info[data].append(s.series_id)
    return info
