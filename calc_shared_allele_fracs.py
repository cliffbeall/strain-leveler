"""calc_shared_allele_fracs.py - A script to parse .vcf files and calculate the
shared allele fraction as in Schloissnig et al. Cliff Beall 9/9/14"""
import argparse
import random


def down_sample(varlist, level):
    refnum = int(varlist[2])
    altnums = [int(s) for s in varlist[4].split(',')]
    sample_source = [0] * refnum
    for i in range(1, len(altnums) + 1):
        sample_source += [i] * altnums[i - 1]
    return random.sample(sample_source, level)

parser = argparse.ArgumentParser()
parser.add_argument("infile", help=".vcf file to process")
parser.add_argument("-s", "--sampling", type=int, help="Downsampling level", default=10)

args = parser.parse_args()

filename = args.infile
samp_level = args.sampling
totals = [0,0,0,0] #[total sites, total alleles, snps, complex]
allele_dict = {}
random.seed(0)

with open(filename, 'r') as vcffile:
    for line in vcffile:
        if line[0] != '#':
            linelist = line.rstrip().split('\t')
            num_alleles = linelist[4].count(',') + 2
            totals[0] += 1
            totals[1] += num_alleles
            if len(linelist[3]) == 1:
                totals[2] += 1
            else:
                totals[3] += 1
            sublist = linelist[9:]
            for i in range(len(sublist)):
                if sublist[i] == '.':
                    continue
                else:
                    varlist_i = sublist[i].split(':')
                    if int(varlist_i[2]) + sum([int(s) for s in varlist_i[4].split(',')]) < samp_level:
                        continue
                    else:
                        samp_i = down_sample(varlist_i, samp_level)
                        for j in range(i, len(sublist)):
                            if sublist[j] == '.':
                                continue
                            else:
                                varlist_j = sublist[j].split(':')
                                if int(varlist_j[2]) + sum([int(s) for s in varlist_j[4].split(',')]) < samp_level:
                                    continue
                                else:
                                    samp_j = down_sample(varlist_j, samp_level)
                                    tot_alleles = len(set(samp_i) | set(samp_j))
                                    shared_alleles = len(set(samp_i) & set(samp_j))
                                    allele_dict[(samples[i], samples[j])][0] += tot_alleles
                                    allele_dict[(samples[i], samples[j])][1] += shared_alleles
                                    
                    
        elif line[:2] == '##':
            continue
        else:
            linelist = line.rstrip().split('\t')
            samples = linelist[linelist.index('FORMAT') + 1:]
            for i in range(len(samples)):
                for j in range(i, len(samples)):
                    allele_dict[(samples[i], samples[j])] = [0,0] # [total alleles, shared]
                    
print '#Input file: ' + filename
print '#Sampling depth: ' + str(samp_level)
print '#There were %s sites with %s alleles. %s were SNPs and %s were complex variants' % tuple(totals)
print 'Sample1\tSample2\tTot_alleles\tShared_alleles\tShared_fraction'
for k in allele_dict:
    if allele_dict[k][0] != 0:
        fraction = float(allele_dict[k][1]) / float(allele_dict[k][0])
        print '\t'.join([k[0], k[1], str(allele_dict[k][0]), str(allele_dict[k][1]), str(fraction)])
    else:
        print '\t'.join([k[0], k[1], str(allele_dict[k][0]), str(allele_dict[k][1]), "undefined"])

