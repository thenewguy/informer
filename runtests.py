# coding: utf-8

"""run tests for Informer"""

import pytest
import sys
import os
import subprocess

PYTEST_ARGS = {
    'default': ['tests'],
    'fast': ['tests', '-q'],
}

sys.path.append(os.path.dirname(__file__))

if __name__ == '__main__':
    pytest.main(PYTEST_ARGS['default'])
