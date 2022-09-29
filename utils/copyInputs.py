from parallelize import parallelize

def main():
    director = 'root://maite.iihe.ac.be:1094/'
    outdir = '/eos/home-a/anmalara/Public/DNNInputs/'
    files = []
    with open('ListFilesToCopy.txt', 'r') as fp:
        files = [x.replace('\n','') for x in fp.readlines()]
    commands = [' '.join(['xrdcp',director+file,outdir]) for file in files ]
    # print (commands)
    parallelize(commands, ncores=10, remove_temp_files=True)

if __name__ == '__main__':
    main()
