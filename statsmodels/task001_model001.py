"""
build basic model for n-back task
"""

import os
import json
from pathlib import Path

if __name__ == "__main__":
    outdir = Path('models')
    if not outdir.exists():
        outdir.mkdir()
    
    spec = {
        "Name": "N-Back",
        "Description": "Model for N-back task",
        "BIDSModelVersion": "1.0.0",
        "Input": {
            "task": "nback"},
        "Nodes": [{
            "Level": "run",
            "Name": "run",
            "GroupBy": ["run", "subject"],
            "Transformations": {
                "Transformer": "pybids-transforms-v1",
                "Instructions": [
                    {
                        "Name": "Scale",
                        "Input": ["response_time"],
                        "Demean": true,
                        "Rescale": false,
                        "Output": ["demeaned_RT"]
                    },
                    {
                        "Name": "Factor",
                        "Input": ["trial_type"]
                    },
                    {
                        "Name": "Convolve",
                        "Model": "spm",
                        "Input": ["trialtype.*", "demeaned_RT"]
                    }
                ]
            }
            "Model": {
                "X": [
                "trial_type.*", 'demeaned_RT'
                "framewise_displacement",
                "trans_x", "trans_y", "trans_z", "rot_x", "rot_y", "rot_z",
                "a_comp_cor_00", "a_comp_cor_01", "a_comp_cor_02",
                "a_comp_cor_03", "a_comp_cor_04", "a_comp_cor_05"]
            },
            "DummyContrasts": {
                "Conditions": ["trial_type.*", 'demeaned_RT'],
                "Test": "t"
            }
        }]
    {
      "Level": "subject",
      "Name": "subject",
      "GroupBy": ["subject", "contrast"],
      "Model": {"X": [1], "Type": "Meta"},
      "DummyContrasts": {
        "Test": "t"
      }
    }