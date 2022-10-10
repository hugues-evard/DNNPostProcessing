import os
from parallelize import parallelize

def main():
    director = 'root://maite.iihe.ac.be:1094/'
    outdir = '/eos/home-a/anmalara/Public/DNNInputs/'
    folders = [
        'all',
        'eventCategory_-3',
        'eventCategory_-2',
        'eventCategory_2',
        'eventCategory_-1',
        'eventCategory_1',
        'eventCategory_0',
        ]
    commands = []
    for folder in folders:
        os.system('mkdir -p '+outdir+folder)
        with open('ListFilesToCopy_'+folder+'.txt', 'r') as fp:
            commands += [' '.join(['xrdcp', '-f', director+x.replace('\n',''),outdir+folder+'/']) for x in fp.readlines()]
    parallelize(commands, ncores=10, remove_temp_files=True)

if __name__ == '__main__':
    main()
