'''
    Adjustments to allow the tests to be run against the local module
'''
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(1, 'mozdef_client')

sys.dont_write_bytecode = True
