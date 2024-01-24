#!/bin/bash

eval "$(conda shell.bash hook)"
conda activate ~/alpha
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CONDA_PREFIX/lib/

python3 gen_npy.py 5000 fiber_data_tiktok.pkl
python3 gen_npy.py 5000 satlink_data_tiktok.pkl

