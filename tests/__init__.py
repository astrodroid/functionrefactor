#!/usr/bin/env python3

import os


_sourceroot = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if 'COV_CORE_CONFIG' in os.environ:
    os.environ['COVERAGE_FILE'] = os.path.join(_sourceroot, '.coverage')
    os.environ['COV_CORE_CONFIG'] = os.path.join(_sourceroot,
                                                 os.environ['COV_CORE_CONFIG'])
