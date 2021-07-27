import json
import os
from re import M

events = {
    'accuracy': {
        'Description': "Indicator of whether task was performed correctly",
        'Levels': {1: 'Correct', 0: 'Incorrect'}
    },

}

bidsdir = '/home/poldrack/data/fmri-handbook-2e-data/bids'
with open(os.path.join(bidsdir, 'events.json'), 'w') as f:
    json.dump(events, f)


events_nback = {
    'nback': {
        'Description': 'Number of items back in memory for target match',
    },
    'stimtype': {
        'Description': 'Type of visual stimulus displayed',
    },
}

with open(os.path.join(bidsdir, 'task-nback_events.json'), 'w') as f:
    json.dump(events_nback, f)


events_dots = {
    'motion_coherence': {
        'Description': 'Relative coherence of motion left or right',
    },
    'SSD': {
        'Description': 'Stop-signal delay',
    },
    'stop_success': {
        'Description': 'Indicator for whether the response was successfully stopped',
    },
}

with open(os.path.join(bidsdir, 'task-dots_events.json'), 'w') as f:
    json.dump(events_dots, f)


events_language = {
    'stimulus_type': {
        'Description': 'Type of sentence show (word vs nonword)',
    }
}

with open(os.path.join(bidsdir, 'task-language_events.json'), 'w') as f:
    json.dump(events_language, f)

events_objects= {
    'is_target': {
        'Description': 'Indicator for whether stimulus was target (scrambled image)',
    }
}

with open(os.path.join(bidsdir, 'task-objects_events.json'), 'w') as f:
    json.dump(events_objects, f)

events_spatialwm = {
    'condition': {
        'Description': 'Hard vs. easy trial',
    }
}

with open(os.path.join(bidsdir, 'task-spatialwm_events.json'), 'w') as f:
    json.dump(events_spatialwm, f)

