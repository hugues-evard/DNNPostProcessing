#!/bin/bash

set -x

MODEL=$1
DATA=$2
SAMPLES=$3
TRAIN="$4"
VAL="$5"
TEST="$6"
GPUS=$7
EPOCHS=$8
WORKDIR=$(pwd)

# Download miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda_install.sh
bash miniconda_install.sh -b -p ${WORKDIR}/miniconda
export PATH=$WORKDIR/miniconda/bin:$PATH
conda create -n weaver python=3.7
conda activate weaver
# # to be used in case one would want to
# conda create python=3.7 -p $WORKDIR/miniconda/envs/weaver
# conda activate $WORKDIR/miniconda/envs/weaver
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

ls /afs/cern.ch/work/a/anmalara/WorkingArea/DNN/DNNPostProcessing/train_VBF.sh

# CUDA environment setup
export PATH=$PATH:/usr/local/cuda-10.2/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-10.2/lib64
export LIBRARY_PATH=$LIBRARY_PATH:/usr/local/cuda-10.2/lib64

echo ./train_VBF.sh -m ${MODEL} -d ${DATA} -f ${SAMPLES} -t "${TRAIN}" -v "${VAL}" -x "${TEST}" -g ${GPUS} -e ${EPOCHS}
./train_VBF.sh -m ${MODEL} -d ${DATA} -f ${SAMPLES} -t "${TRAIN}" -v "${VAL}" -x "${TEST}" -g ${GPUS} -e ${EPOCHS}

[ -d "runs/" ] && tar -caf output.tar trainings/${MODEL}/ runs/ || tar -caf output.tar trainings/${MODEL}/
