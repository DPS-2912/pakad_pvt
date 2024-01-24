#!/bin/bash

eval "$(conda shell.bash hook)"
conda activate ~/alpha
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CONDA_PREFIX/lib/

python3 run_attack.py 5000 fiber_data
python3 run_attack.py 5000 satlink_data
