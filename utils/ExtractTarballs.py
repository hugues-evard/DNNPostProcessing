#!/usr/bin/env python
import os, argparse
from parallelize import parallelize

def ExtractFolders(list_folders, outpath=''):
    commands = ['tar -xvf %s' %(name) for name in list_folders if os.path.exists(name)]
    cwd = outpath!=''
    if cwd:
        commands = [ [outpath,c] for c in commands]
    parallelize(commands, ncores=8, cwd=cwd, remove_temp_files=False)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folders', nargs='*', default=[])
    parser.add_argument('-o', '--outpath', type=str, default='')
    args = parser.parse_args()
    ExtractFolders(list_folders=args.folders, outpath=args.outpath)

if __name__ == '__main__':
    main()
