#!/bin/bash

set -x

MODEL=$1
DATA=$2
SAMPLES=$3
TRAIN="$4"
VAL="$5"
TEST="$6"
GPUS=$7
WORKDIR=$(pwd)

# Download miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda_install.sh
bash miniconda_install.sh -b -p ${WORKDIR}/miniconda
export PATH=$WORKDIR/miniconda/bin:$PATH
# install weaver and clone particle_transformer
pip install numpy pandas scikit-learn scipy matplotlib tqdm PyYAML
pip install uproot3 awkward0 lz4 xxhash
pip install tables
pip install onnxruntime-gpu
pip install tensorboard
pip install torch
pip install pyarrow
pip install weaver-core
# git clone https://github.com/LEAF-HQ/DNNPostProcessing.git
git clone https://github.com/anmalara/DNNPostProcessing.git

cd DNNPostProcessing

# CUDA environment setup
export PATH=$PATH:/usr/local/cuda-10.2/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-10.2/lib64
export LIBRARY_PATH=$LIBRARY_PATH:/usr/local/cuda-10.2/lib64

./train_VBF.sh -m ${MODEL} -d ${DATA} -f ${SAMPLES} -t ${TRAIN} -v ${VAL} -x ${TEST} -g ${GPUS}

subdir=$(cd trainings/${MODEL}/;echo *)

cp train_VBF.sh trainings/${MODEL}/${subdir}

[ -d "runs/" ] && tar -caf output.tar trainings/${MODEL}/ runs/ || tar -caf output.tar trainings/${MODEL}/
