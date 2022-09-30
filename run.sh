#!/bin/bash

MODEL=$1
DATA_CARD=$2
WORKDIR=`pwd`

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
#git clone https://github.com/jet-universe/particle_transformer
git clone https://github.com/hugues-evard/DNNPostProcessing

cd DNNPostProcessing

# CUDA environment setup
export PATH=$PATH:/usr/local/cuda-10.2/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-10.2/lib64
export LIBRARY_PATH=$LIBRARY_PATH:/usr/local/cuda-10.2/lib64

#
#mkdir output

# proper env.sh
#echo '#!/bin/bash

#export DATADIR_JetClass=
#export DATADIR_TopLandscape=
#export DATADIR_QuarkGluon=/eos/user/h/hevard/datasets/QuarkGluon' > env.sh

#./train_QuarkGluon.sh ParT kin \
#    --gpus 0 --batch-size 512 --num-epochs 2
./train_VBF.sh $MODEL $DATA_CARD

#python train.py --predict \
# --data-test ${PATH_TO_SAMPLES}'/prep/top_test_*.root' \
# --num-workers 3 \
# --data-config top_tagging/data/${DATA_CONFIG} \
# --network-config top_tagging/networks/${MODEL_CONFIG} \
# --model-prefix /eos/user/h/hevard/top_tagging/output/particlenet/${PREFIX}_best_epoch_state.pt \
# --gpus 0 --batch-size 512 \
# --predict-output output/${PREFIX}_predict.root

[ -d "runs/" ] && tar -caf output.tar training/VBF/ runs/ || tar -caf output.tar training/VBF/
