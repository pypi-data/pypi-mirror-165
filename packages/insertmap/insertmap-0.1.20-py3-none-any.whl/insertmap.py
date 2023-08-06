#!/usr/bin/env python
__version__='0.1.20'
last_update='2022-08-30'
author='Damien Marsic, damien.marsic@aliyun.com'
license='GNU General Public v3 (GPLv3)'

import dmbiolib as dbl
import argparse,sys,math
from glob import glob
from collections import defaultdict
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def main():
    parser=argparse.ArgumentParser(description="Analysis of insertion sites in viral or microbial genomes using either LAM-PCR or whole genome sequencing. For full documentation, visit: https://insertmap.readthedocs.io")
    parser.add_argument('-v','--version',nargs=0,action=override(version),help="Display version")
    subparser=parser.add_subparsers(dest='command',required=True)
    parser_a=subparser.add_parser('lampcr',help="Detect insertion sites using LAM-PCR derived amplicon libraries")
    parser_a.add_argument('-c','--configuration_file',default='insertmap_lampcr.conf',type=str,help="Configuration file for the insertmap lampcr program (default: insertmap_lampcr.conf), will be created if absent")
    parser_a.add_argument('-n','--new',default=False,action='store_true',help="Create new configuration file and rename existing one")
    parser_b=subparser.add_parser('wgs',help="Detect insertion sites using WGS libraries")
    parser_b.add_argument('-c','--configuration_file',default='insertmap_wgs.conf',type=str,help="Configuration file for the insertmap lampcr program (default: insertmap_wgs.conf), will be created if absent")
    parser_b.add_argument('-n','--new',default=False,action='store_true',help="Create new configuration file and rename existing one")
    parser_c=subparser.add_parser('analyze',help="Analyze data")
    parser_c.add_argument('-c','--configuration_file',default='insertmap_analyze.conf',type=str,help="Configuration file for the lampcr analyze program (default: insertmap_analyze.conf), will be created if absent")
    parser_c.add_argument('-n','--new',default=False,action='store_true',help="Create new configuration file and rename existing one")
    parser_c.add_argument('-f','--file_format',type=str,default='Single multipage pdf',help="Save each figure in separate file with choice of format instead of the default single multipage pdf file. Choices: svg, png, jpg, pdf, ps, eps, pgf, raw, rgba, tif")
    args=parser.parse_args()
    if args.command in 'lampcr,wgs':
        rmap(args)
    if args.command=='analyze':
        analyze(args)

def rmap(args):
    fname=args.configuration_file
    if args.new:
        dbl.rename(fname)
    if args.new or not dbl.check_file(fname,False):
        mapconf(fname,args)
        return
    rname='insertmap_'+args.command+'-report.txt'
    dbl.rename(rname)
    r=open(rname,'w')
    print('\n  Checking configuration... ',end='')
    f=open(fname,'r')
    read=''
    rfiles=[]
    ins={}
    linker={}
    host=''
    insseq={}
    probe=10
    fail=''
    for line in f:
        ln=line.strip()
        if ln[:1]=='#':
            read=''
        if ln[:12]=='# READ FILES':
            read='rfiles'
        if ln[:13]=='# INSERT SITE':
            read='insert'
        if ln[:13]=='# LINKER SITE':
            read='linker'
        if ln[:13]=='# HOST GENOME':
            read='host'
        if ln[:7]=='# PROBE':
            read='probe'
        if ln[:11]=='# INSERTION':
            read='insseq'
        if ln[:3]=='===' or ln[:2]=='# ' or ln[:13]=='Instructions:' or not ln:
            continue
        if read=='rfiles':
            x=ln.split()
            fail+=dbl.check_read_file(x[-1])
            if len(x)>3:
                fail+='\n  Too many items per line under READ FILES! Each line must contain a prefix followed by 1 or 2 (if paired-ends) read files, separated by space or tab!'
            if len(x)==3:
                fail+=dbl.check_read_file(x[1])
            if len(x)==1 or (len(x)==2 and glob(x[0])):
                if '-' in x[0]:
                    z=x[0][:x[0].find('-')]
                elif '_' in x[0]:
                    z=x[0][:x[0].find('_')]
                else:
                    z=x[0][:x[0].find('.')]
                x.insert(0,z)
            if x[0] in [k[0] for k in rfiles]:
                fail+='\n  Duplicate prefix '+x[0]+' found under READ FILES! Each line must contain a different prefix!'
            else:
                rfiles.append(x)
        for n in (('insert',ins),('linker',linker)):
            if read==n[0]:
                x=ln.split()
                if len(x)!=2:
                    fail+='\n  Each line under '+n[0].upper()+' SITE COMMON SEQUENCE must contain a name and a nucleotide sequence, separated by a space or tab!'
                else:
                    t,req=dbl.check_seq(x[1],'atgcryswkmbdhvn','atgc')
                    if not t or not req:
                        fail+='\n  Invalid characters were found under '+n[0].upper()+' SITE COMMON SEQUENCE!'
                    elif x[0] in ins or x[0] in linker:
                        fail+='\n  Duplicate '+n[0]+' name '+x[0]+' found! All insert and linker sequences must have different names!'
                    else:
                        c=x[1].lower()
                        a=len(c)
                        b=0
                        for i in range(len(c)):
                            if c[i] not in 'atgc':
                                a=i
                                break
                        for i in reversed(range(len(c))):
                            if c[i] not in 'atgc':
                                b=i+1
                                break
                        z=c.count('n')
                        y=[c[b:],b,z]  # constant region of sequence (after non-atgc region if present), index, number of N
                        if y in ins.values() or y in linker.values():
                            fail+='\n  Duplicate sequence found: '+x[0]+' !'
                        else:
                            n[1][x[0]]=y
        if read=='host':
            x,y=dbl.getfasta(ln,'atgcryswkmbdhvn','atgc',False)
            if y:
                fail+=y
            else:
                host=list(x.values())[0]
                hname=list(x.keys())[0]
        if read=='probe':
            if not ln.isdigit() or int(ln)<10 or int(ln)>50:
                fail+='\n  Probe length must be an integer between 10 and 50'
            else:
                probe=int(ln)
        if read=='insseq':
            x,y=dbl.getfasta(ln,'atgcryswkmbdhvn','atgc',True)
            if y:
                fail+=y
            else:
                insseq.update(x)
    f.close()
    insprobe={}
    if insseq:
        insrc={}
        for n in insseq:
            insrc[n]=dbl.revcomp(insseq[n])
        q,y=shortest_probe(list(insseq.values())+list(insrc.values()),probe,host,'insert')
        fail+=y
        if not y:
            for n in insseq:
                insprobe[n+'-L']=(insrc[n][-q:],insseq[n][:q])  # left 3', left 5'
                insprobe[n+'-R']=(insseq[n][-q:],insrc[n][:q])  # right 3', right 5'
    if ins:
        q1,y1=shortest_probe([k[0] for k in list(ins.values())],probe,host,'insert')
        if linker:
            q2,y2=shortest_probe([k[0] for k in list(linker.values())],probe,host,'linker')
        else:
            q2,y2=q1,''
        fail+=(y1+y2)
        if not y1 and not y2:
            for n in ins:
                insprobe[n]=(ins[n][0][-q1:],ins[n][1]+len(ins[n][0])-q1)  # probe sequence, index
            for n in linker:
                insprobe[n]=(linker[n][0][-q2:],linker[n][1]+len(linker[n][0])-q2)
    if not rfiles:
        fail+='\n  Read files are missing!'
    if args.command=='lampcr':
        if not ins:
            fail+='\n  Insert site common sequence is missing!'
        if rfiles and len(rfiles[0])==3 and not linker:
            fail+='\n  Linker site common sequence is missing!'
        if rfiles and len(rfiles[0])==2 and linker:
            fail+='\n  R2 read file is missing!'
    elif not insseq:
        fail+='\n  Insert sequence is missing!'
    if not host:
        fail+='\n  Host genome sequence is missing!'
    if fail:
        print('\n'+fail+'\n')
        sys.exit()
    fail=''
    r.write('\n  Host genome: '+hname)
    if ins:
        r.write('\n\n  Insert site common sequence(s):\n  '+'\n  '.join([k+'\t'+ins[k][0] for k in ins]))
    if linker:
        r.write('\n\n  Linker site common sequence(s):\n  '+'\n  '.join([k+'\t'+linker[k][0] for k in linker]))
    if insseq:
        r.write('\n\n  Insertion sequence(s): '+', '.join([k for k in insseq]))
    r.write('\n\n  Probe size: '+str(probe)+'\n\n')
    print('OK\n\n  Checking read files...    ',end='')
    for j in range(len(rfiles)):
        R1=rfiles[j][1]
        nr1,fail=dbl.readcount(R1,fail)
        rfiles[j].append(nr1)
        R2=''
        if len(rfiles[j])==4:
            R2=rfiles[j][2]
            nr2,fail=dbl.readcount(R2,fail)
            rfiles[j].append(nr2)
            if args.command=='lampcr' and nr1>1 and nr2>1 and nr1!=nr2:
                fail+='\n  Paired files '+R1+' and '+R2+' have different numbers of reads! You must use raw read files!'
        if args.command=='lampcr' and R2:
            f1,y1=dbl.initreadfile(R1)
            f2,y2=dbl.initreadfile(R2)
            c1=0
            c2=0
            z=[False,False,False,False]   # insert in R1, linker in R1, insert in R2, linker in R2
            for i in range(100):
                l1,f1,c1,n1=dbl.getread(f1,y1,c1)
                l2,f2,c2,n2=dbl.getread(f2,y2,c2)
                if not l1 or not l2:
                    break
                x=dbl.check_sync(n1,n2)
                fail+=x
                if x:
                    break
                x,_=probe_get(l1,insprobe)
                if x in ins:
                    z[0]=True
                elif x:
                    z[1]=True
                x,_=probe_get(l2,insprobe)
                if x in ins:
                    z[2]=True
                elif x:
                    z[3]=True
            f1.close()
            f2.close()
            if z==[True,False,False,True]:
                x=['R1','R2']
            elif z==[False,True,True,False]:
                x=['R2','R1']
            else:
                x=['mixed','mixed']
            rfiles[j].extend(x)
    if fail:
        dbl.pr2(r,'Problems found!\n'+fail+'\n')
    else:
        print('OK\n')
    if (args.command=='lampcr' and R2) or not R2:
        x='  Read file prefix         Number of read'
        if R2:
            x+=' pairs      Insert reads      Linker reads'
        else:
            x+='s'
        dbl.pr2(r,x)
        for n in rfiles:
            x='  '+n[0].ljust(25)
            if R2:
                x+=f'{n[3]:,}'.rjust(20)+n[-2].center(24)+n[-1].center(12)
            if not R2:
                x+=f'{n[2]:,}'.rjust(15)
            if not R2 or (R2 and n[3]==n[4]):
                dbl.pr2(r,x)
    else:
        dbl.pr2(r,'  Read file prefix         Read file                     Number of reads')
        for n in rfiles:
            dbl.pr2(r,'  '+n[0].ljust(25)+n[1].ljust(30)+f'{n[3]:,}'.rjust(15)+'\n  '+n[0].ljust(25)+n[2].ljust(30)+f'{n[4]:,}'.rjust(15))
    dbl.pr2(r,'')
    if fail:
        r.close()
        sys.exit()
    UMI={}
    t=' nt UMI detected in '
    z=set()
    for n in ins:
        if not R2:
            if ins[n][2]>5:
                UMI[n]=True
                dbl.pr2(r,'  '+str(ins[n][2])+t+n+'\n')
            else:
                UMI[n]=False
        for m in linker:
            if linker[m][2]>5:
                UMI[(n,m)]=(False,True)
                x=m
                y=linker[m][2]
            elif ins[n][2]>5:
                UMI[(n,m)]=(True,False)
                x=n
                y=ins[n][2]
            elif ins[n][2]+linker[m][2]>5:
                UMI[(n,m)]=(True,True)
                x=n+'-'+m
                y=ins[n][2]+linker[m][2]
            else:
                UMI[(n,m)]=(False,False)
                x=''
            if x:
                z.add((x,y))
    for n in z:
        dbl.pr2(r,'  '+str(n[1])+t+n[0]+'\n')
    for rfile in rfiles:
        pre=rfile[0]
        R1=rfile[1]
        f1,y1=dbl.initreadfile(R1)
        c1=0
        R2=''
        if len(rfile)>4:
            R2=rfile[2]
            f2,y2=dbl.initreadfile(R2)
            c2=0
        imap={}
        cnt={}
        idc=[0,0]  # reads with insert detected, reads with linker detected
        for n in [k for k in insprobe if k[:-2] in insseq]:
            imap[n]=defaultdict(int)
            cnt[n]=[0,0]  # insert identified, insertion site identified
        for n in ins:
            for m in linker:
                if True in UMI[(n,m)]:
                    imap[(n,m)]=defaultdict(lambda: defaultdict(int))
                else:
                    imap[(n,m)]=defaultdict(int)
                cnt[(n,m)]=[0,0,0,0]  # insert-linker pair identified, insertion site identified, shear site identified, PCR replicates discarded
            if not R2:
                if UMI[n]==True:
                    imap[n]=defaultdict(lambda: defaultdict(int))
                else:
                    imap[n]=defaultdict(int)
                cnt[n]=[0,0,0]  # insert identified, insertion site identified, PCR replicates discarded
        X=[(R1,f1,y1,c1)]
        if R2:
            X.append((R2,f2,y2,c2))
        C=0
        for j in (0,1):
            if j and (not R2 or args.command=='lampcr'):
                break
            f,y,c=X[j][1],X[j][2],X[j][3]
            nr=rfile[2+j]
            if R2:
                nr=rfile[3+j]
            x=pre
            if insseq:
                x=X[j][0]
            dbl.pr2(r,'\n  -------------------------------------------------------------\n\n')
            t='Processing reads from '+x+'...'
            show=dbl.progress_start(nr,t)
            while True:
                if args.command=='wgs':
                    l,f,c,_=dbl.getread(f,y,c)
                    if not l:
                        break
                    dbl.progress_check(c,show,t)
                    for n in [k for k in insprobe if k[:-2] in insseq]:
                        for m in insprobe[n]:
                            a=l.find(m)
                            if a==-1:
                                continue
                            cnt[n][0]+=1
                            if m in insprobe[n][:2]:
                                dir=1
                                A=l[a+len(m):]
                            else:
                                dir=0
                                A=l[:a]
                            x=seq_locate(A,dir,host,probe)
                            if not x:
                                continue
                            if len(x)==1:
                                x=str(x[0])
                            else:
                                x=str(x).replace(',',' ')
                            cnt[n][1]+=1
                            imap[n][x]+=1
                elif args.command=='lampcr':
                    l1,f1,c1,n1=dbl.getread(f1,y1,c1)
                    if R2:
                        l2,f2,c2,n2=dbl.getread(f2,y2,c2)
                    if not l1 or (R2 and not l2):
                        break
                    if R2:
                        x=dbl.check_sync(n1,n2)
                        if x:
                            dbl.pr2(r,x)
                            r.close()
                            sys.exit()
                    dbl.progress_check(c1,show,t)
                    if R2 and rfile[-1]=='R1':
                        l1,l2=l2,l1
                    if not R2 or rfile[-1]=='mixed':
                        n,a=probe_get(l1,insprobe)   # n: name of ins or linker, a: index of seq to be searched in host
                        if R2 and n in linker:
                            m,b,l2,l1=n,a,l1,l2
                            n,a=probe_get(l1,{i:insprobe[i] for i in ins})
                        elif R2 and n in ins:
                            m,b=probe_get(l2,{i:insprobe[i] for i in linker})
                    else:
                        n,a=probe_get(l1,{i:insprobe[i] for i in ins})
                        m,b=probe_get(l2,{i:insprobe[i] for i in linker})
                    if n:
                        idc[0]+=1
                    if R2 and m:
                        idc[1]+=1
                    if not n or (R2 and not m):
                        continue
                    if R2:
                        cnt[(n,m)][0]+=1
                        x=seq_locate(l1[a:],1,host,probe)
                        if not x:
                            continue
                        cnt[(n,m)][1]+=1
                        y=seq_locate(l2[b:],1,host,probe)
                        if y:
                            cnt[(n,m)][2]+=1
                        if len(x)>1 or len(y)>1:
                            temp=[]
                            for u in x:
                                for v in y:
                                    if abs(u-v)<1000:
                                        temp.append((u,v))
                            if len(temp)==1:
                                x=tuple([temp[0][0]])
                                y=tuple([temp[0][1]])
                        if len(x)==1:
                            x=str(x[0])
                        else:
                            x=str(x).replace(',',' ')
                        if len(y)==1:
                            y=str(y[0])
                        elif not y:
                            y=''
                        else:
                            y=str(y).replace(',',' ')
                        if True in UMI[(n,m)]:
                            u=''
                            if UMI[(n,m)][0]==True:
                                u+=l1[:ins[n][1]]
                            if UMI[(n,m)][1]==True:
                                u+=l2[:linker[m][1]]
                            imap[(n,m)][(x,y)][u]+=1
                            if imap[(n,m)][(x,y)][u]>1:
                                cnt[(n,m)][-1]+=1
                        else:
                            imap[(n,m)][(x,y)]+=1
                    else:
                        cnt[n][0]+=1
                        x=seq_locate(l1[a:],1,host,probe)
                        if not x:
                            continue
                        if len(x)==1:
                            x=str(x[0])
                        else:
                            x=str(x).replace(',',' ')
                        cnt[n][1]+=1
                        if UMI[n]==True:
                            imap[n][x][l1[:ins[n][1]]]+=1
                            if imap[n][x][l1[:ins[n][1]]]>1:
                                cnt[n][-1]+=1
                        else:
                            imap[n][x]+=1
            dbl.progress_end()
            if args.command=='wgs':
                C+=c
        f1.close()
        if R2:
            f2.close()
        dbl.pr2(r,'\n  Read file prefix: '+pre)
        x='s'
        if R2:
            x=' pairs'
        if args.command=='lampcr':
            C=c1
        dbl.pr2(r,('  Read'+x+' processed:').ljust(48)+f'{C:,}'.rjust(15))
        for n in [k for k in insprobe if k[:-2] in insseq]:
            dbl.pr2(r,'\n  Insert: '+n)
            dbl.pr2(r,'  Number of insert ends found:'.ljust(48)+f'{cnt[n][0]:,}'.rjust(15))
            dbl.pr2(r,'  Number of insertion site identifications:'.ljust(48)+f'{cnt[n][1]:,}'.rjust(15))
            dbl.pr2(r,'  Number of different insertion sites:'.ljust(48)+f'{len(imap[n]):,}'.rjust(15))
            x=pre+'--'+n+'_imap.csv'
            dbl.dict2csv(x,sorted(imap[n],key=sortmix),imap[n],None,'Insertion map',r)
        if args.command=='lampcr':
            dbl.pr2(r,('  Reads with insert identified:').ljust(48)+f'{idc[0]:,}'.rjust(15))
            if R2:
                dbl.pr2(r,('  Reads with linker identified:').ljust(48)+f'{idc[1]:,}'.rjust(15))
            for c in imap:
                x=''
                y=c
                if R2:
                    x='-linker pair'
                    y='-'.join(c)
                dbl.pr2(r,'\n  Insert'+x+': '+y)
                dbl.pr2(r,('  Number of insert'+x+' identifications:').ljust(48)+f'{cnt[c][0]:,}'.rjust(15))
                dbl.pr2(r,'  Number of insertion site identifications:'.ljust(48)+f'{cnt[c][1]:,}'.rjust(15))
                x=len(imap[c])
                if R2:
                    x=len({k[0] for k in imap[c]})
                dbl.pr2(r,'  Number of different insertion sites:'.ljust(48)+f'{x:,}'.rjust(15))
                if R2:
                    dbl.pr2(r,'  Number of shear site identifications:'.ljust(48)+f'{cnt[c][2]:,}'.rjust(15))
                    dbl.pr2(r,'  Number of different shear sites:'.ljust(48)+f'{len({k[1] for k in imap[c] if k[1]}):,}'.rjust(15))
                y=pre+'--'+y
                if UMI[c]==True or (R2 and True in UMI[c]):
                    dbl.pr2(r,'  Number of insert-linker-UMI replicates found:'.ljust(48)+f'{cnt[c][-1]:,}'.rjust(15))
                    for n in ('_raw','_corrected'):
                        z=defaultdict(int)
                        for i in imap[c]:
                            if R2:
                                q=i[0]
                            else:
                                q=i
                            if n=='-raw':
                                z[q]+=sum(imap[c][i].values())
                            else:
                                z[q]+=len(imap[c][i])
                        x=y+n+'_imap.csv'        
                        dbl.dict2csv(x,sorted(z,key=sortmix),z,None,n[1].upper()+n[2:]+' insertion map',r)
                else:
                    if R2:
                        z=defaultdict(int)
                        for i in imap[c]:
                            z[i[0]]+=imap[c][i]
                    else:
                        z=imap[c]
                    x=y+'_imap.csv'
                    dbl.dict2csv(x,sorted(z,key=sortmix),z,None,'Insertion map',r)
                if R2 and True in UMI[c]:
                    for n in ('_raw','_corrected'):
                        z=defaultdict(int)
                        for i in imap[c]:
                            if not '(' in i[0] and i[1] and not '(' in i[1]:
                                a,b=int(i[0]),int(i[1])
                                q=abs(b-a)
                                if q>len(host)/2:
                                    q=abs(min(a,b)+len(host)-max(a,b))
                                if n=='-raw':
                                    z[q]+=sum(imap[c][i].values())
                                else:
                                    z[q]+=len(imap[c][i])
                        x=y+n+'_sd.csv'
                        dbl.dict2csv(x,sorted(z),z,None,n[1].upper()+n[2:]+' Fragment size distribution',r)
                elif R2 and not True in UMI[c]:
                    x=y+'_sd.csv'
                    z=defaultdict(int)
                    for i in imap[c]:
                        if not '(' in i[0] and i[1] and not '(' in i[1]:
                            a,b=int(i[0]),int(i[1])
                            q=abs(b-a)
                            if q>len(host)/2:
                                q=abs(min(a,b)+len(host)-max(a,b))
                            z[q]+=imap[c][i]
                    dbl.dict2csv(x,sorted(z),z,None,'Fragment size distribution',r)
                    



# Improve detection of insertion sites by allowing 1 nt mismatches (1, 2 or 3 to be optionally selected)
# same for identification of inserts (create alternate set located just before the current ones with no overlap)

    r.close()
    print('\n  Report was saved into file: '+rname+'\n')

def analyze(args):
    cf=args.configuration_file
    if args.new:
        dbl.rename(cf)
    if args.new or not dbl.check_file(cf,False):
        anaconf(cf,args)
        return
    format=dbl.check_plot_format(args.file_format)
    print('\n  Checking configuration... ',end='')
    f=open(cf,'r')
    read=''
    report=[]
    gb=''
    sd={}
    ins={}
    thr=0
    fail=''
    title=''
    for line in f:
        ln=line.strip()
        if ln[:1]=='#':
            read=''
        if ln[:13]=='# REPORT FILE':
            read='report'
        if ln[:11]=='# ANNOTATED':
            read='gb'
        if ln[:10]=='# FRAGMENT':
            read='sd'
        if ln[:11]=='# INSERTION':
            read='ins'
        if ln[:11]=='# THRESHOLD':
            read='thr'
        if not ln and read in ('sd','ins'):
            title=''
        if ln[:3]=='===' or ln[:2]=='# ' or ln[:13]=='Instructions:' or not ln:
            continue
        if read=='report':
            if dbl.check_file(ln,False):
                report.append(ln)
            else:
                fail+='\n  Report file '+ln+' not found!'
        if read=='gb':
            if gb:
                fail+='\n  Only one file should be listed under ANNOTATED GENOME FILE!'
            elif dbl.check_file(ln,False):
                gb=ln
            else:
                fail+='\n  Genome file '+ln+' not found!'
        if read in ('sd','ins'):
            if title:
                x=ln.split()
                if dbl.check_file(x[-1],False):
                    if (read=='sd' and len(sd[title])==31) or (read=='ins' and len(ins[title])==31):
                        fail+='\n  Maximum number of files per plot exceeded! '+title
                        continue
                    if len(x)>2 and read=='sd':
                        fail+='\n  More than 2 items per line! '+str(x)
                        continue
                    if len(x)>3 and read=='ins':
                        fail+='\n  More than 3 items per line! '+str(x)
                        continue
                    if len(x)==1 or (len(x)==2 and read=='ins' and x[0][-4:]=='.csv' and x[1][-4:]=='.csv'):
                        x.insert(0,x[-1][:x[-1].find('--')])
                    if read=='sd':
                        sd[title].append(x)
                    else:
                        ins[title].append(x)
                else:
                    fail+='\n  File '+ln+' not found!'
            elif read=='sd' and ln not in sd:
                sd[ln]=[]
                title=ln
            elif read=='ins' and ln not in ins:
                ins[ln]=[]
                title=ln
            else:
                fail+='\n  Duplicate title found! '+ln
        if read=='thr':
            if ln.replace('.','').replace('%','').isdigit():
                if thr:
                    fail+='\n  Only one number should be entered under THRESHOLD!'
                    continue
                x=float(ln.replace('%',''))
                if x<0 or x>100:
                    fail+='\n  Threshold must be a number between 0 and 100! (recommended: 0.1))'
                    continue
                thr=x
    if not ins:
        fail+='\n  No insertion site distribution found!'
    if fail:
        print('Problems found!\n'+fail+'\n')
        sys.exit()
    else:
        print('OK')
    if format:
        mppdf=''
        print()
    else:
        dbl.rename('insertmap_'+str(thr)+'_figs.pdf')
        fname='insertmap_'+str(thr)+'_figs.pdf'
        mppdf=PdfPages(fname)
    if sd:
        sdmode={}
        c='viridis_r'
        for title in sd:
            sdist=defaultdict(lambda:[0]*len(sd[title]))
            labels=[]
            s=[]
            sdmode[title]=[]
            for i in range(len(sd[title])):
                labels.append(sd[title][i][0])
                x=dbl.csv2list(sd[title][i][1])
                if len(x[0])>2:
                    print('\n  Wrong file format! Each line should contain exactly 2 items!\n')
                    sys.exit()
                s.append(sum([int(k[1]) for k in x]))
                j=0
                while len(x)>400:
                    j+=1
                    x=[k for k in x if int(k[1])>j]
                for n in x:
                    sdist[int(n[0])][i]=int(n[1])/s[i]*100
                y=[k for k in sdist if sdist[k][i]]
                if y:
                    sdmode[title].append(max(sdist,key=lambda k:sdist[k][i]))
                else:
                    sdmode[title].append(0)
            colors,fig=dbl.plot_start(c,len(sd[title]),title+' Fragment size distribution')
            for i in range(len(s)):
                plt.scatter([k for k in sdist],[sdist[k][i] for k in sdist],alpha=0.7,s=20,color=colors.colors[i],label=labels[i])
            plt.xlabel('Fragment size (bp)')
            plt.ylabel('% of reads')
            plt.xscale('log')
            plt.ylim(bottom=0)
            plt.margins(x=0.015)
            plt.legend()
            dbl.plot_end(fig,title+'_size-distribution',format,mppdf)
        locs=list(range(len(sdmode)))
        colors,fig=dbl.plot_start(c,len(labels),'Most common fragment size')
        z=0.94/len(labels)
        w=z*0.9
        for i in range(len(labels)):
            plt.bar([n+z*i for n in locs],[sdmode[n][i] for n in sdmode],width=w,label=labels[i],color=colors.colors[i])
        plt.xticks([n+z*i/2 for n in locs],sdmode.keys())
        plt.ylabel('Most common fragment size (bp)')
        plt.legend()
        dbl.plot_end(fig,'insertmap_most-common-fragment-size',format,mppdf)
    compl={}
    glenr=defaultdict(lambda:{k:(0,0) for k in ins})
    for title in ins:
        compl[title]=[]
        imap=defaultdict(lambda:[0]*len(ins[title]))
        labels=[]
        s=[]
        for i in range(len(ins[title])):
            labels.append(ins[title][i][0])
            x=dbl.csv2list(ins[title][i][1])
            y=[]
            if len(ins[title][i])==3:
                y=dbl.csv2list(ins[title][i][2])
            for z in (x,y):
                for n in z:
                    if len(n)>2:
                        print('\n  Wrong file format! Each line should contain exactly 2 items!\n')
                        sys.exit()
                    a,b=n[0],n[1]
                    if a[0]=='(':
                        a=a.replace(' ',',')
                    if z==x:
                        imap[a][i]=int(b)
                    else:
                        imap[a][i]=(imap[a][i],int(b))
                if z==x:
                    s.append(sum([imap[k][i] for k in imap]))
                elif y and z==y:
                    for n in imap:
                        if isinstance(imap[n][i],int):
                            imap[n][i]=(imap[n][i],0)
                    s[i]=(s[i],sum([imap[k][i][1] for k in imap]))
        if len(ins[title][0])==3:
            for n in [k for k in imap]:
                for m in imap[n]:
                    if isinstance(m,tuple) and m[0] and m[1]:
                        break
                else:
                    del imap[n]
        compl[title].append(len(imap))
        cpl={}
        for i in range(len(s)):
            if len(ins[title][0])==2:
                cpl[labels[i]]=[len([imap[n][i]/s[i]*100 for n in imap if imap[n][i]])]
                for j in dbl.exprange(0.0001,101,1.3):
                    x=[imap[n][i]/s[i]*100 for n in imap]
                    cpl[labels[i]].append(len([k for k in x if k>=j]))
            else:
                cpl[labels[i]]=[len([min(imap[n][i][0]/s[i][0]*100,imap[n][i][1]/s[i][1]*100) for n in imap if isinstance(imap[n][i],tuple) and imap[n][i][0] and imap[n][i][1]])]
                for j in dbl.exprange(0.0001,101,1.3):
                    x=[min(imap[n][i][0]/s[i][0]*100,imap[n][i][1]/s[i][1]*100) for n in imap if isinstance(imap[n][i],tuple)]
                    cpl[labels[i]].append(len([k for k in x if k>=j]))
            compl[title].append(cpl[labels[i]][0])
        for n in imap:
            for i in range(len(s)):
                if isinstance(imap[n][i],int):
                    if len(ins[title][0])==2:
                        imap[n][i]=max(imap[n][i]/s[i]*100,1/s[i]*100)
                    else:
                        imap[n][i]=max(imap[n][i]/s[i][0]*100,1/s[i][0]*100)
                else:
                    imap[n][i]=min(max(1/s[i][0]*100,imap[n][i][0]/s[i][0]*100),max(1/s[i][1]*100,imap[n][i][1]/s[i][1]*100))
        enr={}
        if len(ins[title])>1:
            for n in imap:
                if max(imap[n])<thr:
                    continue
                x=[]
                for i in range(1,len(s)):
                    x.append(math.log10(imap[n][i]/imap[n][i-1]))
                if max(x)>0:
                    enr[n]=x
            for n in enr:
                x=imap[n][-1]
                y=sum(enr[n])
                if x>=thr and y>0:
                    glenr[n][title]=(x,y)
        for n in [k for k in imap]:
            if max(imap[n])<thr:
                del imap[n]
        c='viridis_r'
        colors,fig=dbl.plot_start(c,len(ins[title]),title.replace('_',' ')+' Insertion site complexity')
        for i in range(len(s)):
            plt.plot([0]+list(dbl.exprange(0.0001,101,1.3)),cpl[labels[i]],color=colors.colors[i],label=labels[i])
        plt.xscale('log')
        plt.yscale('log')
        plt.ylabel('Number of insertion sites')
        plt.xlabel('Minimum insertion site frequency (%)')
        plt.xticks(size=7.5)
        plt.legend()
        dbl.plot_end(fig,title+'_'+str(thr)+'_complexity',format,mppdf)
        x2=sorted([k for k in imap if k[0]=='('],key=lambda x: int(x[1:x.find(',')]))
        x1=sorted([int(k) for k in imap if not '(' in k])
        for x in (x1,x2):
            if not x:
                continue
            colors,fig=dbl.plot_start(c,len(ins[title]),title.replace('_',' ')+' Insertion site frequencies')
            for i in range(len(s)):
                plt.scatter(x,[imap[str(k)][i] for k in x],alpha=0.7,s=50,color=colors.colors[i],label=labels[i])
            plt.xlabel('Genome position')
            plt.ylabel('% of reads')
            plt.xticks(rotation=90,size=7.5)
            plt.ylim(bottom=0)
            plt.margins(x=0.015)
            plt.legend()
            y=title+'_frequency'
            if x==x2:
                y+='_ambiguous'
            dbl.plot_end(fig,y,format,mppdf)
        if enr:
            colors,fig=dbl.plot_start(c,None,title.replace('_',' ')+' Insertion site enrichment')
            x=list(enr.values())
            y=list(zip(*x))
            plt.imshow(y,aspect='auto',cmap='RdBu',origin='lower')
            lim=max(max([n for m in y for n in m]),abs(min([n for m in y for n in m])))
            plt.clim(-lim, lim)
            plt.colorbar(shrink=0.7,pad=0.015,label='Log(Enrichment factor)')
            plt.xlabel('Genome position')
            plt.ylabel('Evolution')
            plt.xticks(range(len(enr)),enr.keys(),rotation=90,size=7.5)
            plt.yticks([k-0.5 for k in range(len(labels))],labels)
            dbl.plot_end(fig,title+'_complexity',format,mppdf)
    locs=list(range(len(compl)))
    labels=['Global']+[k[0] for k in ins[list(ins.keys())[0]]]
    colors,fig=dbl.plot_start(c,len(labels),'Global insertion site complexity')
    z=0.94/len(labels)
    w=z*0.9
    for i in range(len(labels)):
        plt.bar([n+z*i for n in locs],[compl[n][i] for n in compl],width=w,label=labels[i],color=(['red']+list(colors.colors))[i])
    plt.xticks([n+z*i/2 for n in locs],compl.keys())
    plt.ylabel('Number of insertion sites')
    plt.legend()
    dbl.plot_end(fig,'insertmap_complexity',format,mppdf)
    colors,fig=dbl.plot_start(c,None,'Global insertion site enrichment')
    sf=1000/max([max([glenr[x][y][0] for y in glenr[x]]) for x in glenr])
    for title in ins:
        X=sorted(glenr,key=sortmix)
        plt.scatter(x=X,y=[glenr[k][title][1] for k in X],s=[glenr[k][title][0]*sf for k in X],alpha=0.6,label=title)
    plt.xlabel('Genome position')
    plt.ylabel('Enrichment score')
    plt.xticks(rotation=90,size=7.5)
    plt.ylim(bottom=0)
    plt.margins(x=0.015)
    plt.legend()
    dbl.plot_end(fig,'insertmap_enrichment',format,mppdf)
    if not format:
        mppdf.close()
        print('  All figures were saved into single multipage file: '+fname+'\n')
    f.close()
 

###  save new csv files (enrichment...)

###  wgs -> add evolution of frequency of IS detection with passage number (or nb inserts per genome ?) -> in analysis !!!
###      -> do right and left separately in addition to combined !

### do plot from report

#  table: add final freq * enrichment score for candidates in candidate table, add most common fragment size and % in stat table 

# optional x axis limit for SD

    ####################

def anaconf(fname,args):
    report=glob('*report.txt')
    if not report:
        print('\n  Warning! Report file not found!\n')
    imap=glob('*imap.csv')
    if not imap:
        print('\n Insert map files not found!\n')
        sys.exit()
    gb=glob('*.gb*')+glob('*.gen*')
    if not gb:
        print('\n  Warning! No Genbank file found! An annotated genome sequence in Genbank format is recommended for detailed analysis.')
    sd=glob('*sd.csv')
    f=open(fname,'w')
    f.write('=== INSERTMAP ANALYZE  CONFIGURATION FILE ===\n\n')
    f.write('# REPORT FILE(S):\n')
    f.write('\n'.join(report))
    f.write('\n\n')
    f.write('# ANNOTATED GENOME FILE:\n')
    if len(gb)==1:
        f.write(gb[0])
    f.write('\n\n')
    if sd:
        sd=dbl.sortfiles(sd,'--')
        f.write('# FRAGMENT SIZE DISTRIBUTION\nInstructions: Each group (surrounded by empty lines) is a separate plot. The first line in each group is the plot title, subsequent lines (maximum 20!) are file names of size distributions, preceded by optional label (if not present, the part before "--" will be used as label). Multiple files within groups will be combined and displayed with different colors.\n\n')
        x=[k for k in sd if '_corrected_' in k]
        y=[k for k in sd if '_corrected_' not in k and '_raw_' not in k]
        for n in (x,y):
            for m in set([k[k.rfind('--')+2:k.rfind('_sd.csv')] for k in n]):
                f.write(m.replace('_corrected','')+'\n'+'\n'.join([k[:k.find('--')]+' '+k for k in n if m in k])+'\n\n')
    f.write('# INSERTION SITE DISTRIBUTION AND ENRICHMENT\nInstructions: Each group (surrounded by empty lines) is a separate plot. The first line in each group is the plot title, subsequent lines (maximum 20!) are file names of insertion site distributions in chronological order, preceded by optional label (if not present, the part before "--" will be used as label).\n\n')
    x=sorted(set([k[k.find('--')+2:].replace('_raw','').replace('_corrected','').replace('_imap.csv','') for k in imap]))
    pairs=[]
    if len(x)>1:
        if len(x)==2:
            pairs.append(list(x))
        else:
            y=set([k[k.find('-'):] for k in x])
            for n in y:
                z=[k for k in x if (n in k)]
                if len(z==2):
                    pairs.append(list(z))
    imap=dbl.sortfiles(imap,'--')
    x=[k for k in imap if '_corrected_' in k]
    y=[k for k in imap if '_corrected_' not in k and '_raw_' not in k]
    for n in (x,y):
        for m in set([k[k.rfind('--')+2:k.rfind('_imap.csv')] for k in n]):
            f.write(m.replace('_corrected','')+'\n'+'\n'.join([k[:k.find('--')]+' '+k for k in n if m in k])+'\n\n')
    for p in pairs:
        i=0
        j=0
        while True:
            i=p[0].find('-',i)
            j=p[1].find('-',j)
            a=p[0][i:]
            b=p[1][j:]
            if a==b:
                break
            if len(a)>=len(b):
                i+=1
            if len(b)>=len(a):
                j+=1
        z=[[k,k.replace(p[0],p[1])] for k in imap if p[0] in k and '_raw_' not in k]
        f.write(p[0][:i]+'+'+p[1][:j]+a+'\n'+'\n'.join([k[0][:k[0].find('--')]+' '+k[0]+' '+k[1] for k in z if k[1] in imap])+'\n\n')
    f.write('# THRESHOLD\nInstructions: Only insertion sites with a frequency higher than this number in % will be taken into account.\n\n0.5\n\n')
    f.write('=== END OF CONFIGURATION FILE ===')
    f.close()
    print('\n  Edit the file '+fname+' before running insertmap '+args.command+' again !\n\n')

def mapconf(fname,args):
    f=open(fname,'w')
    f.write('=== INSERTMAP '+args.command.upper()+' CONFIGURATION FILE ===\n\n')
    f.write('# READ FILES\nInstructions: list prefix (to be used in output file names) and read file names, one pair of files (paired-end data) / one file (single end data) per line, separated by space or tab.\n\n')
    y=dbl.find_read_files()
    f.write('\n'.join(y)+'\n\n')
    f.write('# HOST GENOME\nInstructions: write name of the file containing the host genome sequence (FASTA format only).\n\n')
    x=glob('*.f*a')
    y=''
    if len(x)==1:
        y=x[0]
    elif len(x)>1:
        y=[dbl.fsize(k) for k in x]
        y=x[y.index(max(y))]
    if y:
        f.write(y+'\n\n')
    if args.command=='lampcr':
        f.write('# INSERT SITE COMMON SEQUENCE(S)\nInstructions: write the name and entire common sequence of each read preceding the host sequence (primer + sequence downstream), including any diversity sequence or tag (as NNNN...), one per line, name and sequence separated by space or tab.\n\n\n\n')
        f.write('# LINKER SITE COMMON SEQUENCE(S) (paired-end only)\nInstructions: write the name and entire common sequence of each read preceding the host sequence (primer + sequence downstream), including any diversity sequence or tag (as NNNN...), one per line, name and sequence separated by space or tab.\n\n\n\n')
    else:
        f.write('# INSERTION SEQUENCE(S)\nInstructions: write name(s) of file(s) containing the insert sequence(s), either a single multifasta file or multiple fasta files, one file name per line. Unknown or variable internal regions can be represented by stretches of N.\n\n')
        if len(x)>1:
            x.remove(y)
            f.write('\n'.join(x)+'\n\n')
    f.write('# PROBE LENGTH\nInstructions: minimum length in nt of sequences used as probes to identify insertions (integer between 10 and 50.\n\n10\n\n')
    f.write('=== END OF CONFIGURATION FILE ===')
    f.close()
    print('\n  Edit the file '+fname+' before running insertmap '+args.command+' again !\n\n')

def override(func):
    class OverrideAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string):
            func()
            parser.exit()
    return OverrideAction

def version():
    print('\n  Project: '+sys.argv[0][max(sys.argv[0].rfind('\\'),sys.argv[0].rfind('/'))+1:-3]+'\n  Version: '+__version__+'\n  Latest update: '+last_update+'\n  Author: '+author+'\n  License: '+license+'\n')

def probe_get(read,probes):
    for i in (0,-1,1):
        for n in probes:
            if read[probes[n][1]+i:].startswith(probes[n][0]):
                break
        else:
            continue
        break
    else:
        return '',-1
    return n,probes[n][1]+len(probes[n][0])+i

def seq_locate(A,dir,host,probe):
    if len(A)<probe:
        return ''
    B=dbl.revcomp(A)
    for i in range(probe,len(A)+1):
        if dir:
            a=A[:i]
            b=B[-i:]
        else:
            a=A[-i:]
            b=B[:i]
        d=(host+host[:len(a)-1]).count(a)+(host+host[:len(b)-1]).count(b)
        if d<=1:
            break
    x=[]
    q=0
    while True:
        w=False
        for n in (a,b):
            z=(host+host[:i-1]).find(n,q)
            if z==-1:
                continue
            q=z+1
            if (n==a and not dir) or (n==b and dir):
                z+=len(a)
                if z>len(host):
                    z-=len(host)
            x.append(z)
            w=True
        if not w:
            break
    return tuple(x)

def shortest_probe(seqs,lim,host,t):  #  move to dmbiolib !
    if lim<1:
        lim=1
    fail=''
    q=-1
    x=min([len(k) for k in seqs])
    y=set([k[-x:] for k in seqs])
    if len(y)!=len(seqs):
        fail='\n  Duplicate '+t+' found! '+t[0].upper()+t[1:]+'s must all be different when trimmed to their maximal common size!'
    if host and len([k for k in y if k in host+host[:x-1]]):
        fail+='\n  '+t[0].upper()+t[1:]+' found in the host genome!'
    if not fail:
        q=lim
        while True:
            y=set([k[-q:] for k in seqs])
            if len(y)==len(seqs) and max([k.count(p) for k in seqs for p in y])==1 and not len([k for k in y if k in host+host[:q-1]]):
                break
            q+=1
    return q,fail

def sortmix(x):
    if x[0]=='(':
        return 0
    else:
        return int(x)





if __name__ == '__main__':
    main()

