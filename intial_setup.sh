DATADIR=$HOME/data_unsynced/selftracking_2021/dicom
SESNUM="013"
OUTDIR=$HOME/data_unsynced/selftracking_2021/bids

docker run --rm -it -v ${DATADIR}:/data:ro -v ${OUTDIR}:/output nipy/heudiconv:latest \
    -d /data/{subject}/{session}/SCANS/*/DICOM/*dcm -s sub-01 -ss ses-${SESNUM} \
    -f /src/heudiconv/heudiconv/heuristics/convertall.py -c none -o /output