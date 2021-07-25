from pathlib import Path
import os
dicomdir = Path('/scratch/01329/poldrack/selftracking_2021/dicom/sub-01')

sessions = [os.path.basename(i) for i in dicomdir.glob('*')]
DATAHOME='/scratch/01329/poldrack/selftracking_2021'
DATADIR=os.path.join(DATAHOME, 'dicom')
OUTDIR = os.path.join(DATAHOME, 'bids')
CODE = os.path.join(DATAHOME, 'ds000031_conversion')

for s in sessions:
   cmd = 'heudiconv -d %s/sub-{subject}/{session}/SCANS/*/DICOM/*dcm -s 01 -ss %s -c none -f %s/heuristic.py -o %s' % (DATADIR, s, CODE, OUTDIR)
   print(cmd)
