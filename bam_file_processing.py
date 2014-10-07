import os
import subprocess
import time

##time.sleep(86400)

mosdir = '/Volumes/GriffenLeysLab/Cliff/illumina_strains/mosaik_others/'

subfolders = ['Prev_mel_25845', 'Ro_mu_25296', \
              'Ro_mu_43093', 'Veill_parv_ACS', \
              'Veill_parv_2008']

##os.mkdir(mosdir + 'proc_bams')
for folder in subfolders:
##    mergelist = []
##    files = os.listdir(mosdir + folder)
##    for f in files:
##        if f[-4:] == '.bam':
##            file1 = mosdir + folder + '/' + f
##            file2 = mosdir + 'proc_bams/' + f[:-4] + '.bam'
##            command1 = "~/samtools-0.1.16/samtools view -b -F 4 %s > %s" % (file1, file2)
##            subprocess.call(command1, shell=True)
##            prefix3 = mosdir + 'proc_bams/' + f[:-4] + '_sorted'
##            command2 = "~/samtools-0.1.16/samtools sort %s %s" % (file2, prefix3)
##            subprocess.call(command2, shell=True)
##            mergelist.append(prefix3 + '.bam')
    mergedbam = "%sproc_bams/%s_merged.bam" % (mosdir, folder)
##    command3 = "~/samtools-0.1.16/samtools merge " + mergedbam + " " + ' '.join(mergelist)
##    subprocess.call(command3, shell=True)
##    command4 = "~/samtools-0.1.16/samtools index " + mergedbam
##    subprocess.call(command4, shell=True)
    command5 = "~/samtools-0.1.16/samtools view %s | cut -f1 | sort -u > %sproc_bams/%s_reads.txt" % (mergedbam, mosdir, folder)
    subprocess.call(command5, shell=True)

with open('/Volumes/GriffenLeysLab/Cliff/illumina_strains/new_read_comparisons.txt', 'w') as outputfile:
    outputfile.write('Genome1\tGenome2\tCommon\t1only\t2only\n')
    for i in range(4):
        for j in range(i+1,5):
            filename1 = "%sproc_bams/%s_reads.txt" % (mosdir, subfolders[i])
            filename2 = "%sproc_bams/%s_reads.txt" % (mosdir, subfolders[j])
            command2 = "comm -12 %s %s | wc -l" % (filename1, filename2)
            command3 = "comm -23 %s %s | wc -l" % (filename1, filename2)
            command4 = "comm -13 %s %s | wc -l" % (filename1, filename2)
            output2 = subprocess.check_output(command2, shell=True)
            output3 = subprocess.check_output(command3, shell=True)
            output4 = subprocess.check_output(command4, shell=True)
            outstr = '\t'.join([subfolders[i], subfolders[j], output2.strip(), \
                                output3.strip(), output4.strip()])
            outputfile.write(outstr + '\n')
                     
