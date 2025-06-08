#!/usr/bin/env python3
import subprocess
import os
import shutil

BLOCK_SIZES = ['4k', '8k', '16k', '32k', '64k', '128k', '256k', '512k', '1m']
READ_MIXES = [100, 80, 60, 40, 20, 0]
TEST_DIR = '/tmp/fio-comprehensive'
RESULTS_DIR = '/tmp/fio-results'

os.makedirs(TEST_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

print("Starting comprehensive fio test matrix...")
print(f"Block sizes: {BLOCK_SIZES}")
print(f"Read percentages: {READ_MIXES}")
print()

for bs in BLOCK_SIZES:
   for read_pct in READ_MIXES:
       if read_pct == 100:
           rw_type = 'read'
           test_name = f'bs{bs}_read100'
           cmd = ['fio', f'--name={test_name}', f'--directory={TEST_DIR}', 
                  f'--rw={rw_type}', f'--bs={bs}', '--size=100M', '--numjobs=4',
                  '--runtime=30s', '--time_based', '--group_reporting',
                  f'--output={RESULTS_DIR}/{test_name}.txt']
       elif read_pct == 0:
           rw_type = 'write'
           test_name = f'bs{bs}_write100'
           cmd = ['fio', f'--name={test_name}', f'--directory={TEST_DIR}', 
                  f'--rw={rw_type}', f'--bs={bs}', '--size=100M', '--numjobs=4',
                  '--runtime=30s', '--time_based', '--group_reporting',
                  f'--output={RESULTS_DIR}/{test_name}.txt']
       else:
           rw_type = 'randrw'
           test_name = f'bs{bs}_read{read_pct}write{100-read_pct}'
           cmd = ['fio', f'--name={test_name}', f'--directory={TEST_DIR}', 
                  f'--rw={rw_type}', f'--rwmixread={read_pct}', f'--bs={bs}',
                  '--size=100M', '--numjobs=4', '--runtime=30s', '--time_based',
                  '--group_reporting', f'--output={RESULTS_DIR}/{test_name}.txt']
       
       print(f"Running: {test_name}")
       subprocess.run(cmd)
       
       shutil.rmtree(TEST_DIR)
       os.makedirs(TEST_DIR, exist_ok=True)

print(f"All tests complete. Results in {RESULTS_DIR}")