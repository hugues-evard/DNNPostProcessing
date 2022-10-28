#! /usr/bin/env python
import os
from datetime import datetime
from collections import OrderedDict
from printing_utils import green
from ClusterSubmission.CondorBase import SubmitListToCondor

def GetArgs(args):
    empty = list(filter(lambda x: args[x]=='', args.keys()))
    if len(empty):
        raise ValueError('Some arguments are empty:'+ str(empty))
    return ' '.join(args.values())



def submit(n_epochs, cat, doTest, debug):
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

    times_cat = {
        'cat0':    {'cat': 'eventCategory_[0]',    'time':'00:05:00',},
        'cat1':    {'cat': 'eventCategory_[1]',    'time':'00:05:00',},
        'cat2':    {'cat': 'eventCategory_[2]',    'time':'00:05:00',},
        'catm0':   {'cat': 'eventCategory_-[0]',   'time':'00:30:00',},
        'catm1':   {'cat': 'eventCategory_-[1]',   'time':'00:30:00',},
        'catm2':   {'cat': 'eventCategory_-[2]',   'time':'00:30:00',},
        'cat012':  {'cat': 'eventCategory_[0-2]',  'time':'00:10:00',},
        'catm012': {'cat': 'eventCategory_-[0-2]', 'time':'00:30:00',},
        'all':     {'cat': 'all',                  'time':'02:00:00',},
    }

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
        ('train',      inputdir+'/'+times_cat[cat]['cat']+'/MC*M1[2][4-6]*UL1[6-7-8]*.root'),
        ('val',        inputdir+'/'+times_cat[cat]['cat']+'/MC*M1[2][0]*UL1[6-7-8]*.root'),
        ('test',       inputdir+'/'+times_cat[cat]['cat']+'/MC*M1[3][0]*UL1[6-7-8]*.root'),
        ('n_gpus',     '0' if not 'request_GPUs' in extraInfo else extraInfo['request_GPUs']),
        ('n_epochs',   n_epochs),
        ('extra_name', 'epoch_'+n_epochs+'_'+cat),
    ])
    if doTest:
        args['flag_test'], args['train'], args['val'], args['test'] = ('test', 'none','none','none')

    if args['flag_test']!= 'test' and any([ args[x]== 'none' for x in ['train','val','test']]):
        raise ValueError('Unexpected inputs.')

    for model,data in model_config_info:
        args['model'] = model
        args['data'] = data
        job_args.append(GetArgs(args))

    outdir     = os.getenv('HOME')+'/workspace/CondorOutputs/'
    executable = 'run_on_condor.sh'
    Time = str((datetime.strptime(times_cat[cat]['time'], '%H:%M:%S') - datetime(1900, 1, 1))*int(n_epochs))

    SubmitListToCondor(job_args, executable=executable, outdir=outdir, Time=Time, extraInfo=extraInfo, deleteInfo=deleteInfo, debug=debug)

def main():
    epochs = ['10']
    categories = ['cat0','cat1','cat2','catm0','catm1','catm2','cat012','catm012','all']
    categories = ['all']

    doTest = False
    # doTest = True
    debug=False
    debug=True
    for n_epochs in epochs:
        for cat in categories:
            print(green('--> Working on: n_epochs:'+n_epochs+' '+cat ))
            submit(n_epochs=n_epochs, cat=cat, doTest=doTest, debug=debug)

if __name__ == '__main__':
    main()
