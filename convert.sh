DATADIR=$HOME/data_unsynced/selftracking_2021/dicom
SESNUM="015"
OUTDIR=$HOME/data_unsynced/selftracking_2021/bids
CODE=/Users/poldrack/Dropbox/code/ds000031_conversion

rm -rf $OUTDIR/.heudiconv
rm -rf $OUTDIR/*

#docker run --rm -it -v ${DATADIR}:/data:ro -v ${OUTDIR}:/output -v ${CODE}:/code nipy/heudiconv:latest \
heudiconv -d ${DATADIR}/sub-{subject}/{session}/SCANS/*/DICOM/*dcm -s 01 -ss ${SESNUM} \
    -f $CODE/heuristic.py -b -o ${OUTDIR}