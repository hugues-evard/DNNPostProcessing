#!/bin/bash

# Example of usage
#./train_VBF.sh
#./train_VBF.sh -m mlp_pf -d VBF_features
#./train_VBF.sh -m deepak8_pf -d VBF_features
#./train_VBF.sh -m particlenet_pf -d VBF_points_features
#./train_VBF.sh -e "--batch-size 512 --num-epochs 3"

set -x

echo "args: $@"

extra_opts=""

model="mlp_pf"
data="VBF_features"

while getopts m:d:e: flag
do
    case "${flag}" in
        m) model=${OPTARG};;
        d) data=${OPTARG};;
        e) extra_opts=${OPTARG};;
    esac
done


inputdir="/eos/home-a/anmalara/Public/DNNInputs"
outputdir="trainings/${model}/{auto}"
output_name="pred.root"

data_train="${inputdir}/MC__*_M130_*_UL18_[8-9].root"
data_val="${inputdir}/MC__*_M130_*_UL17_[8-9].root"
data_test="${inputdir}/MC__*_M130_*_UL16postVFP_[8-9].root"

model_config="models/${model}.py"
data_config="data/${data}.yaml"

train_opts="--num-epochs 20"
batch_opts="--batch-size 128 --start-lr 1e-3"

weaver \
    --data-train ${data_train} --data-val ${data_val} --data-test ${data_test} \
    --data-config ${data_config} --network-config ${model_config} \
    --model-prefix "${outputdir}/net" --log "${outputdir}/log.log" \
    --num-workers 2 --fetch-step 1 ${train_opts} ${batch_opts} --gpus "" \
    --optimizer ranger --predict-output ${output_name} \
    ${extra_opts}

#--samples-per-epoch 160000
#--samples-per-epoch-val 20000
#--tensorboard VBF_${suffix} \
#--in-memory --train-val-split 0.8889
