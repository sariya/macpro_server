#!/usr/bin/env python
__author__ = "Sanjeev Sariya"
__date__= "08 May 2017"
__maintainer__= "Sanjeev Sariya"
__status__= "development"

long_description= """

Filter sequences that have Ns in that from taxonomy and FASTA file
Take in tab delimited taxonomy file
take in fasta file and output direcory 
 
"""

import sys, os, re, argparse,glob
import subprocess as sp 
from Bio import SeqIO
import numpy as np
#
if sys.version_info < (2,7):
    print "Python 2.7+ are needed for script!"
    sys.exit()
##

#
def open_fasta(fasta_file,outdir,name):
    """
    Name is prefix for fasta and taxonomy file
    outdir - output path for fasta file
    fasta_file input fasta file
    return list with seqids that have Ns
    """
    filtered_file=outdir +"/filtered_"+name+"_seq.fasta" #new fasta file
    seq_with_n=[] #array to store seq ids with Ns
    count=0 #total seqs --
    
    for record in SeqIO.parse(fasta_file,"fasta"):

        count+=1
        if (record.seq).find('N')!=-1 or (record.seq).find('n')!=-1:
            seq_with_n.append(record.id)

        else:
            with open(filtered_file,'a') as w_handle:
                w_handle.write(">"+record.description+"\n"+str(record.seq)+"\n")
            #--with write ends
        #if ends
    #for loop ends

    print "Sequences with Ns ",len(seq_with_n)
    
    for i in seq_with_n:
        print i
    #--for loop ends
    print "Total seqs in fasta file ",count
    print "Seqs that can be used ",count-len(seq_with_n)
    return seq_with_n #return 
    #-----------------------------------------------
    #
    #------------------------------------------
def print_filtered_tax(temp_list,temp_out,prefix_name,tax_file):
    """
    Take list that has seq ids that have Ns 
    take output dir, taxonomy file
    """
    new_tax_file=filtered_file=temp_out +"/filtered_"+prefix_name+"_tax.txt" #new taxonomy file
    with open(tax_file,'r') as handle:
        for line in handle:
            line = line.rstrip()
            line_array=re.split('\s+',line)
            if not line_array[0] in temp_list:
                with open(new_tax_file,'a') as t_handle:
                    t_handle.write(line+"\n")
                #--with ends
            #if seq id not in list with Ns
        #-for loop ends
    #--with loop ends
        
    #-------------------
    #
    #------------------

if __name__=="__main__": 
#{{{ main starts
    parser=argparse.ArgumentParser("description")
    parser.add_argument ('-f','--fasta',help='location/path of seqs file',required=True) # store seqs file
    parser.add_argument ('-t','--tax',help='location/path of taxonomy file',required=True) # store taxonomy file
    parser.add_argument ('-o','--out',help='location/path of output',required=True) # store output dir
    parser.add_argument ('-p','--prefix',help='prefix for output file',required=True) # store prefix for output file 
    args_dict = vars(parser.parse_args()) # make them dict..
    fasta_file=os.path.abspath(args_dict['fasta'])
    output_dir=os.path.abspath(args_dict['out'])
    tax_file=os.path.abspath(args_dict['tax'])
    prefix_file=args_dict['prefix']
    ids_with_n=open_fasta(fasta_file,output_dir,prefix_file)
    print_filtered_tax(ids_with_n,output_dir,prefix_file,tax_file)
#}}} main ends
