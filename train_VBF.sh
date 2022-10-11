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
samples=""
gpus=""
epochs="10"

while getopts e:g:m:d:e:f:t:v:x: flag
do
    case "${flag}" in
        e) epochs=${OPTARG};;
        g) gpus=${OPTARG};;
        m) model=${OPTARG};;
        d) data=${OPTARG};;
        e) extra_opts=${OPTARG};;
        f) samples=${OPTARG};;
        t) data_train=${OPTARG};;
        v) data_val=${OPTARG};;
        x) data_test=${OPTARG};;
    esac
done

inputdir="/eos/home-a/anmalara/Public/DNNInputs"
outputdir="trainings/${model}/{auto}"
output_name="pred.root"

if [[ $samples == "full" ]]; then
    data_train="${inputdir}/MC*UL1[6-7-8]*_[2-9][0-9].root"
    data_val="${inputdir}/MC*UL1[6-7-8]*_[0-9].root"
    data_test="${inputdir}/MC*UL1[6-7-8]*_[1][0-9].root"
elif [[ $samples == "half" ]]; then
    data_train="${inputdir}/MC*UL18*_[1-3][0-9].root"
    data_val="${inputdir}/MC*UL17*_[0-5].root"
    data_test="${inputdir}/MC*UL16*_[1][0-5].root"
elif [[ $samples == "short" ]]; then
    data_train="${inputdir}/MC*UL18*_[0-9].root"
    data_val="${inputdir}/MC*UL17*_[0-1].root"
    data_test="${inputdir}/MC*UL16*_[1][0-1].root"
fi


model_config="models/${model}.py"
data_config="data/${data}.yaml"

train_opts="--num-epochs "${epochs}
batch_opts="--batch-size 128 --start-lr 1e-3"

weaver \
    --data-train "${data_train}" --data-val "${data_val}" --data-test "${data_test}" \
    --data-config ${data_config} --network-config ${model_config} \
    --model-prefix "${outputdir}/net" --log "${outputdir}/log.log" \
    --num-workers 2 --fetch-by-files --fetch-step 10 ${train_opts} ${batch_opts} --gpus "" \
    --optimizer ranger --predict-output ${output_name} \
    ${extra_opts}

#--samples-per-epoch 160000
#--samples-per-epoch-val 20000
#--tensorboard VBF_${suffix} \
#--in-memory --train-val-split 0.8889
