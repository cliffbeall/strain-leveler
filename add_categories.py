with open('allele_frac_tsv.txt', 'r') as infile:
    lines = infile.readlines()

newlines = []
for line in lines:
    linelist = line.rstrip().split('\t')    
    if linelist[0] == 'Sample1':
        line = line.rstrip() + '\tCategory\n'
    else:        
        for i in range(2):
            if linelist[i][-2:] == 'en':
                linelist[i] = linelist[i][:-2]
        time0 = int(linelist[0].split('.')[2])
        time1 = int(linelist[1].split('.')[2])
        if linelist[0] == linelist[1]:
            linelist.append('same.sample')
        elif linelist[0][:2] == linelist[1][:2]: # same family
            if linelist[0][3:5] == linelist[1][3:5]:
                if linelist[0][3:5] == 'BS':
                    linelist.append('resamp.baby')
                else:
                    linelist.append('resamp.mom')
            else:
                if (time0 > 6 and time1 > 6) or (time0 < 6 and time1 < 6):
                    linelist.append('mom.relbaby.sametime')
                else:
                    linelist.append('mom.relbaby.difftime')
        elif linelist[0][3:5] == 'MS' and linelist[1][3:5] == 'MS':
            linelist.append('unrelated.moms')
        elif linelist[0][3:5] == 'BS' and linelist[1][3:5] == 'BS':
            if time0 < 6 and time1 < 6:
                linelist.append('unrelated.y.babies')
            elif time0 > 6 and time1 > 6:
                linelist.append('unrelated.o.babies')
            else:
                linelist.append('unrelated.d.babies')
        else:
            if (linelist[0][3:5] == 'BS' and time0 < 6) or \
               (linelist[1][3:5] == 'BS' and time1 < 6):
                linelist.append('unrel.mom.y.babies')
            else:
                linelist.append('unrel.mom.o.babies')
        line = '\t'.join(linelist) + '\n'
    newlines.append(line)
with open('allele_frac_wcats_tsv.txt', 'w') as outfile:
    outfile.writelines(newlines)

        
                                   
        
