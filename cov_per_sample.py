"""cov_per_sample.py - uses samtools depth and awk to calculate average coverage per sample
It assumes alignments that have been processed with the bam_file_processing script
stored in a proc_bams folder within parent_folder. It gets a list of species abbreviations
to calculate for from a file designated by the species_file argument
"""
import argparse
import subprocess
import os

parser = argparse.ArgumentParser()
parser.add_argument("parent_folder", help="parent folder with subfolders containing alignments")
parser.add_argument("species_file", help="species abbreviations to calculate")
args = parser.parse_args()

os.chdir(args.parent_folder)

prefixes = {}

with open('/Volumes/GriffenLeysLab/Cliff/illumina_strains/fileprefix_samples.txt', 'r') as infile:
    for line in infile:
        linelist = line.rstrip().split('\t')
        prefixes[linelist[1]] = linelist[0]
samples = prefixes.keys()

species = []
with open(args.species_file, 'r') as infile2:
    for line in infile2:
        species.append(line.rstrip())

with open('cov_per_sample_tsv.txt', 'w') as outfile:
    outfile.write('Sample\t' + '\t'.join(species) + '\n')
    for sample in samples:
        outfile.write(sample)
        for spec in species:
            path = args.parent_folder + 'proc_bams/' + prefixes[sample] + spec +  '_sorted.bam'
            command = "~/samtools-0.1.16/samtools depth %s | awk 'BEGIN { COV = 0; LEN = 0 } { COV += $3; LEN++ } END { print COV / LEN }'" % (path)
            o = subprocess.check_output(command, shell=True)
            outfile.write('\t' + o.rstrip())
        outfile.write('\n')
