from pathlib import Path
import os
dicomdir = Path('/home/poldrack/data/fmri-handbook-2e-data/dicom/sub-01')

sessions = [os.path.basename(i) for i in dicomdir.glob('*')]
DATAHOME='/home/poldrack/data/fmri-handbook-2e-data'
DATADIR=os.path.join(DATAHOME, 'dicom')
OUTDIR = os.path.join(DATAHOME, 'bids')
CODE = os.path.join('/home/poldrack/Dropbox/code/ds000031_conversion')

for s in sessions:
   cmd = 'heudiconv -d %s/sub-{subject}/{session}/SCANS/*/DICOM/*dcm -s 01 -ss %s -f %s/heuristic.py -b -o %s' % (DATADIR, s, CODE, OUTDIR)
   print(cmd)
