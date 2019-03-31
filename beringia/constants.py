# -*- coding: utf-8 -*-
"""constants.py

.. _Docstring example here:
   https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html
"""
STATE_CONSTANTS = {
    0: {'stateIncreaseProb': 0.20, 'stateDecreaseProb': 0, 'fireStartProb': 0.000, 'fireSpreadProb': 0.000},
    1: {'stateIncreaseProb': 0.10, 'stateDecreaseProb': 0.00, 'fireStartProb': 0.0005, 'fireSpreadProb': 0.100},
    2: {'stateIncreaseProb': 0.15, 'stateDecreaseProb': 0.00, 'fireStartProb': 0.0005, 'fireSpreadProb': 0.200},
    3: {'stateIncreaseProb': 0.10, 'stateDecreaseProb': 0.00, 'fireStartProb': 0.0005, 'fireSpreadProb': 0.300},
    4: {'stateIncreaseProb': 0.10, 'stateDecreaseProb': 0.00, 'fireStartProb': 0.0005, 'fireSpreadProb': 0.450},
    5: {'stateIncreaseProb': 0.00, 'stateDecreaseProb': 0.00, 'fireStartProb': 0.0005, 'fireSpreadProb': 0.700},
    -1: {'stateIncreaseProb': 1.00, 'stateDecreaseProb': 0.00, 'fireStartProb': 0.000, 'fireSpreadProb': 0.000}
}


PLANT_COLOR_KEY = {
    0: '\033[1;30;48;5;246m0\033[0;39m',
    1: '\033[1;30;48;5;190m1\033[0;39m',
    2: '\033[1;30;48;5;118m2\033[0;39m',
    3: '\033[1;30;48;5;46m3\033[0;39m',
    4: '\033[1;30;48;5;34m4\033[0;39m',
    5: '\033[1;30;48;5;2m5\033[0;39m',
    -1: 'f'
}

COLOR_KEY = {
    0: ''
}

FEATURES_SWITCH = {
    'geology': True
}
