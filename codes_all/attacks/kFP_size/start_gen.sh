#!/bin/bash

eval "$(conda shell.bash hook)"
conda activate ~/alpha
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CONDA_PREFIX/lib/

python3 gen_data.py firefox_fiber_direction.pkl
python3 gen_data.py firefox_satlink_direction.pkl
python3 gen_data.py tor_fiber_direction.pkl
python3 gen_data.py tor_satlink_direction.pkl

