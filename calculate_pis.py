import argparse
from Bio import SeqIO

parser = argparse.ArgumentParser()
parser.add_argument("infile", help=".vcf file to process")

args = parser.parse_args()
filename = args.infile

pi_sum = 0.0
pi_between = {}
pi_by_samp = {}


with open(filename, 'r') as vcffile:
    for line in vcffile:
        if line[0] != '#':
            linelist = line.rstrip().split('\t')
            num_alleles = linelist[4].count(',') + 2
            infolist = linelist[7].split(';')
            if infolist[5][:3] != 'AO=' or infolist[28][:3] != 'RO=':
                print 'Unexpected format of INFO field at position ' + linelist[1]
                break
            allele_counts = [float(infolist[28][3:])] + [float(x) for x in infolist[5][3:].split(',')]
            s_ac = sum(allele_counts)
            for k in range(len(allele_counts)):
                count1 = allele_counts[k]
                remaining = allele_counts[:k] + allele_counts[k+1:]
                for count2 in remaining:
                    pi_sum += (count1 / s_ac) * (count2 / (s_ac - 1))
            sublist = linelist[9:]
            for i in range(len(sublist)):
                if sublist[i] == '.':
                    continue
                varlist_i = sublist[i].split(':')
                allele_counts_i = [float(varlist_i[2])] + [float(x) for x in varlist_i[4].split(',')]
                s_aci = sum(allele_counts_i)
                if s_aci == 0.0:
                    continue
                for k in range(len(allele_counts_i)):
                    countik = allele_counts_i[k]
                    remaining = allele_counts_i[:k] + allele_counts_i[k+1:]
                    for count2 in remaining:
                        if s_aci > 1:
                            pi_by_samp[samples[i]] += (countik/s_aci)*((count2)/(s_aci - 1))
                if i == len(sublist) - 1:
                    break
                for j in range(i + 1, len(sublist)):
                    if sublist[j] == '.':
                        continue
                    varlist_j = sublist[j].split(':')
                    allele_counts_j = [float(varlist_j[2])] + [float(x) for x in varlist_j[4].split(',')]
                    s_acj = sum(allele_counts_j)
                    if s_acj == 0.0:
                        continue
                    for k in range(len(allele_counts_i)):
                        j_sublist = allele_counts_j[:k] + allele_counts_j[k+1:]
                        for countj in j_sublist:
                            pi_between[(samples[i], samples[j])] += (allele_counts_i[k] / s_aci) * (countj / s_acj)
            
        elif line[:2] == '##':
            if len(line) > 12 and line[2:12] == 'reference=':
                reffile = line.rstrip()[12:]
            continue
        else:
            linelist = line.rstrip().split('\t')
            samples = linelist[linelist.index('FORMAT') + 1:]
            for i in range(len(samples)):
                pi_by_samp[samples[i]] = 0.0
                if i == len(samples) - 1:
                    break
                for j in range(i + 1, len(samples)):
                    pi_between[(samples[i], samples[j])] = 0.0 

with open(reffile, 'r') as handle:
    reflen = sum([len(rec) for rec in SeqIO.parse(handle, 'fasta')])
##reflen = 42

print "# Analyzed vcf file: " + filename
print "# Reference genome: " + reffile
print "# Reference genome length: " + str(reflen)
print "# Pi within samples:"
print "Sample\tPi"
print "All\t" + str(pi_sum / reflen)
for samp in sorted(pi_by_samp):
    print samp + "\t" + str(pi_by_samp[samp] / reflen)
print "# Pi between samples:"
print "Sample1\tSample2\tPi"
for (samp1, samp2) in pi_between:
    print "\t".join(sorted([samp1, samp2]) + [str(pi_between[(samp1, samp2)] / reflen)])
