import os
import subprocess
import time

print time.strftime("Start: %a %H:%M", time.localtime())

mb = '/Users/cliffbeall/MOSAIK/bin/MosaikBuild'
ma = '/Users/cliffbeall/MOSAIK/bin/MosaikAligner'
anndir = '/Users/cliffbeall/MOSAIK/MOSAIK-2.2.3-source/networkFile/'

querydir = '/Users/cliffbeall/illumina_strains/sequences/mosaik_queries/'
refdir = '/Volumes/GriffenLeysLab/Cliff/illumina_strains/bact_genomes/'

queries = os.listdir(querydir)

genomefiles = []
with open("/Volumes/GriffenLeysLab/Cliff/illumina_strains/genome_fastas.txt", "r") as gffile:
	for line in gffile:
		genomefiles.append(line.rstrip())

shortnames = {}
for genome in genomefiles:
	sublist = genome.split('_')
	namelist = [sublist[0][:4], sublist[1][:4]] + sublist[2:-2] 
	shortnames[genome] = '_'.join(namelist)

with open('/Volumes/GriffenLeysLab/Cliff/illumina_strains/mosaik_output_1005.txt', 'w') as stdoutfile:
    for genome in genomefiles:
    	barglist = [mb, '-fr', refdir + genome, '-oa', refdir + genome[:-3] + '.mkb']
    	subprocess.call(barglist, stdout=stdoutfile, stderr=subprocess.STDOUT)
        outdir = '/Volumes/GriffenLeysLab/Cliff/illumina_strains/mosaik_run3/' + shortnames[genome]
        os.mkdir(outdir)
        for query in queries:
            arglist = [ma, '-in', querydir + query, '-quiet', \
                       '-out', outdir + '/' + query[:-4] + shortnames[genome], \
                       '-ia', refdir + genome[:-3] + '.mkb', '-annpe', anndir + '2.1.78.pe.ann', \
                       '-annse', anndir + '2.1.78.se.ann']
            subprocess.call(arglist, stdout=stdoutfile, stderr=subprocess.STDOUT)

print time.strftime("End: %a %H:%M", time.localtime())
        
