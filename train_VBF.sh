#!/bin/bash

MODEL=$1
DATA_CARD=$2

set -x

#export DATADIR_VBF='/eos/user/h/hevard/datasets/test'
export DATADIR_VBF='/eos/user/a/anmalara/Public/DNNInputs/'

echo "args: $@"

# set the dataset dir via `DATADIR_QuarkGluon`
DATADIR=${DATADIR_VBF}
[[ -z $DATADIR ]] && DATADIR='./datasets/QuarkGluon'

# set a comment via `COMMENT`
suffix=${COMMENT}

# PN, PFN, PCNN, ParT
#modelopts="networks/particlenet_pf.py"
lr="1e-3"
extraopts=""

weaver \
    --data-train "${DATADIR}/MC__*_M130_*_UL18_1.root" \
    --data-test "${DATADIR}/MC__*_M130_*_UL18_2.root" \
    --data-config $DATA_CARD --network-config $MODEL \
    --model-prefix training/VBF/{auto}${suffix}/net \
    --num-workers 1 --fetch-step 1 --in-memory --train-val-split 0.8889 \
    --batch-size 512 --samples-per-epoch 160000 --samples-per-epoch-val 20000 --num-epochs 20 \
    --start-lr $lr --optimizer ranger --log logs/VBF_{auto}${suffix}.log --predict-output pred.root \
    --tensorboard VBF_${suffix} \
    ${extraopts} "${@:3}"
#    --batch-size 512 --samples-per-epoch 16000 --samples-per-epoch-val 2000 --num-epochs 2 --gpus 0 \
#    --data-train "${DATADIR}/MC__*_M130_*_UL18_1.root" \
#    --data-test "${DATADIR}/MC__*_M130_*_UL18_2.root" \
#    --data-train "${DATADIR}/MC__*_M130_*_UL18_[1-2][0-9].root" \
#    --data-test "${DATADIR}/MC__*_M130_*_UL18_3[0-9].root" \
#    --data-config data/VBF_points_features.yaml --network-config $modelopts \
