import subprocess
import os

os.chdir('/Volumes/GriffenLeysLab/Cliff/illumina_strains/mosaik_others/')

files = {}

with open('samples_filenames.txt', 'r') as infile:
    for line in infile:
        linelist = line.rstrip().split('\t')
        files[linelist[3]] = linelist[:3]
samples = files.keys()

with open('cov_per_sample_tsv.txt', 'w') as outfile:
    outfile.write('Sample\tCov_Veill_parv_2008\tCov_Prev_mel_25845\tCov_Ro_mu_43093\n')
    for sample in samples:
        outfile.write(sample)
        for name in files[sample]:
            command = "~/samtools-0.1.16/samtools depth %s | awk 'BEGIN { COV = 0; LEN = 0 } { COV += $3; LEN++ } END { print COV / LEN }'" % ('./proc_bams/' + name)
            o = subprocess.check_output(command, shell=True)
            outfile.write('\t' + o.rstrip())
        outfile.write('\n')
        
    
