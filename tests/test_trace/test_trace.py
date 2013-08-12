#!/usr/bin/env python

import os
from subprocess import Popen, STDOUT, PIPE
import filecmp

pwd = os.path.dirname(__file__)

def setup(): 
    os.putenv('PWD', pwd)
    os.chdir(pwd)

def test_run():
    proc = Popen([pwd + '/../../src/openmc'], stderr=STDOUT, stdout=PIPE)
    returncode = proc.wait()
    stdout = proc.communicate()[0]
    print(stdout)
    assert returncode == 0
    assert stdout.find('Simulating Particle 453') != -1

def test_created_statepoint():
    assert os.path.exists(pwd + '/statepoint.10.binary')

def test_results():
    os.system('python results.py')
    compare = filecmp.cmp('results_test.dat', 'results_true.dat')
    if not compare:
      os.system('cp results_test.dat results_error.dat')
    assert compare

def teardown():
    output = [pwd + '/statepoint.10.binary', pwd + '/results_test.dat']
    for f in output:
        if os.path.exists(f):
            os.remove(f)
