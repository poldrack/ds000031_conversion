# run fmriprep on myconnectome

docker run -ti --rm \
    -v /data/fmri-handbook-2e-data/bids:/data:ro \
    -v /data/fmri-handbook-2e-data/derivatives:/out \
    -v /data/fmri-handbook-2e-data/ds000031-workdir:/work \
    -v $HOME/license.txt:/opt/freesurfer/license.txt \
    nipreps/fmriprep \
    /data /out/fmriprep-20.2.0 \
    participant -u $(id -u) \
    --skip_bids_validation -w /work --participant-label sub-01 -t rest
