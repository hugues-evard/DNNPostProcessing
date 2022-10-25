#! /usr/bin/env python
import os
from collections import OrderedDict
from ClusterSubmission.CondorBase import SubmitListToCondor

def GetArgs(args):
    empty = list(filter(lambda x: args[x]=='', args.keys()))
    if len(empty):
        raise ValueError('Some arguments are empty:'+ str(empty))
    return ' '.join(args.values())


def main():
    extraInfo = {
        'should_transfer_files': 'YES',
        'transfer_output_files': 'DNNPostProcessing/output.tar',
        'transfer_output_remaps': '"output.tar = $(outdir)/output.$(ClusterId).$(ProcId).tar"',
        'request_GPUs': '1',
        'request_CPUs': '4',
        'getenv': 'False',
        'MY.SendCredential': 'True',
        'request_memory': '4',
        'request_disk': '4',
        'on_exit_remove':'(ExitBySignal == False) && (ExitCode == 0)',
        'max_retries': '3',
        'requirements': 'Machine =!= LastRemoteHost',
    }
    deleteInfo = [
        #'request_disk', 'request_memory'
        ]

    model_config_info = []
    modes = ['', '_charged', '_neutral', '_UE', '_VBF']
    # modes = ['']
    for mode in modes:
        model_config_info.append(('mlp_pf',         'VBF_features'+mode))
        model_config_info.append(('deepak8_pf',     'VBF_features'+mode))
        model_config_info.append(('particlenet_pf', 'VBF_points_features'+mode))

    job_args   = []
    inputdir ='/eos/home-a/anmalara/Public/DNNInputs/'
    args = OrderedDict([
        # ('filepath',   'DNNPostProcessing'),
        ('filepath',   os.getcwd()),
        ('model',      ''),
        ('data',       ''),
        ('flag_test',  'none'),
        # ('flag_test',  'test'),
        ('train',      'none'),
        ('val',        'none'),
        ('test',       'none'),
        ('train',      inputdir+'/eventCategory_[0-2]/MC*M1[2][4-6]*UL1[6-7-8]*.root'),
        ('val',        inputdir+'/eventCategory_[0-2]/MC*M1[2][0]*UL1[6-7-8]*.root'),
        ('test',       inputdir+'/eventCategory_[0-2]/MC*M1[3][0]*UL1[6-7-8]*.root'),
        ('n_gpus',     '0' if not 'request_GPUs' in extraInfo else extraInfo['request_GPUs']),
        ('n_epochs',   '10'),
        ('extra_name', ''),
        ('extra_name', 'epoch_10_cat012'),
    ])

    if args['flag_test']!= 'test' and any([ args[x]== 'none' for x in ['train','val','test']]):
        raise ValueError('Unexpected inputs.')

    for model,data in model_config_info:
        args['model'] = model
        args['data'] = data
        job_args.append(GetArgs(args))

    outdir    = os.getenv('HOME')+'/workspace/CondorOutputs/'
    time = 'espresso'     # 20min
    time = 'microcentury' # 1h
    # time = 'longlunch'    # 2h
    # time = 'workday'      # 8h
    # time = 'tomorrow'     # 24h

    debug=False
    # debug=True
    SubmitListToCondor(job_args, executable='run_on_condor.sh', outdir=outdir, Time=time, extraInfo=extraInfo, deleteInfo=deleteInfo, debug=debug)

if __name__ == '__main__':
    main()
