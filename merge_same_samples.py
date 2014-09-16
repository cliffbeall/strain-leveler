import subprocess



bamdir = '/Volumes/GriffenLeysLab/Cliff/illumina_strains/mosaik_others/proc_bams/'

files1 = ['140408_CCB0001_1_ATCACG_nh_Prev_mel_25845_sorted.bam', \
          '140408_CCB0001_1_ATCACG_nh_Ro_mu_43093_sorted.bam', \
          '140408_CCB0001_1_ATCACG_nh_Veill_parv_2008_sorted.bam', \
          '140408_CCB0002_1_CGATGT_nh_Prev_mel_25845_sorted.bam', \
          '140408_CCB0002_1_CGATGT_nh_Ro_mu_43093_sorted.bam', \
          '140408_CCB0002_1_CGATGT_nh_Veill_parv_2008_sorted.bam', \
          '140408_CCB0003_1_TTAGGC_nh_Prev_mel_25845_sorted.bam', \
          '140408_CCB0003_1_TTAGGC_nh_Ro_mu_43093_sorted.bam', \
          '140408_CCB0003_1_TTAGGC_nh_Veill_parv_2008_sorted.bam']
files2 = ['140408_CCB0021_1_GTTTCG_nh_Prev_mel_25845_sorted.bam', \
          '140408_CCB0021_1_GTTTCG_nh_Ro_mu_43093_sorted.bam', \
          '140408_CCB0021_1_GTTTCG_nh_Veill_parv_2008_sorted.bam', \
          '140408_CCB0016_1_CCGTCC_nh_Prev_mel_25845_sorted.bam', \
          '140408_CCB0016_1_CCGTCC_nh_Ro_mu_43093_sorted.bam', \
          '140408_CCB0016_1_CCGTCC_nh_Veill_parv_2008_sorted.bam', \
          '140408_CCB0014_1_AGTTCC_nh_Prev_mel_25845_sorted.bam', \
          '140408_CCB0014_1_AGTTCC_nh_Ro_mu_43093_sorted.bam', \
          '140408_CCB0014_1_AGTTCC_nh_Veill_parv_2008_sorted.bam']

merge1 = ['RGID=MERGE1', 'RGLB=CB0001/21', 'RGSM=AB.BS.10', \
          'RGPL=illumina', 'RGPI=170', 'RGPU=ATCACG/GTTTCG', \
          'VALIDATION_STRINGENCY=SILENT']
merge2 = ['RGID=MERGE2', 'RGLB=CB0002/16', 'RGSM=AB.BS.3', \
          'RGPL=illumina', 'RGPI=170', 'RGPU=CGATGT/CCGTCC', \
          'VALIDATION_STRINGENCY=SILENT']
merge3 = ['RGID=MERGE3', 'RGLB=CB0003/14', 'RGSM=AA.MS.10', \
          'RGPL=illumina', 'RGPI=170', 'RGPU=AGTTCCC/CCGTCC', \
          'VALIDATION_STRINGENCY=SILENT']
allmerge = ([merge1] * 3) + ([merge2] * 3) + ([merge3] * 3)
prefixlist = (['AB_BS_10_'] * 3) + (['AB_BS_3_'] * 3) + (['AA_MS_10_'] * 3)

rg_command = ['java', '-jar', '-Xmx4g', \
              '/Users/cliffbeall/picard-tools-1.112/picard-tools-1.112/AddOrReplaceReadGroups.jar', \
              '', '']


for i in range(len(files1)):
    rg_command[4] = 'INPUT=' + bamdir + files1[i]
    imfile1 = prefixlist[i] + '_'.join(files1[i].split('_')[5:8]) + 'part1.bam'
    rg_command[5] = 'OUTPUT=' + bamdir + imfile1
    subprocess.call(rg_command + allmerge[i])
    rg_command[4] = 'INPUT=' + bamdir + files2[i]
    imfile2 = prefixlist[i] + '_'.join(files1[i].split('_')[5:8]) + 'part2.bam'
    rg_command[5] = 'OUTPUT=' + bamdir + imfile2
    subprocess.call(rg_command + allmerge[i])
    command = '/Users/cliffbeall/samtools-1.0/samtools merge -c -p ' + \
               bamdir + imfile1[:-4] + '_combined.bam ' + \
               bamdir + imfile1 + ' ' + bamdir + imfile2
    subprocess.call(command, shell=True)
    
              
    
