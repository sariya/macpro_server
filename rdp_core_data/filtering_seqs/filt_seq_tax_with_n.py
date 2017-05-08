#!/usr/bin/env python
__author__ = "Sanjeev Sariya"
__date__= "23 August 2016"
__maintainer__= "Sanjeev Sariya"
__status__= "development"

long_description= """

Filter sequences that have Ns in that from taxonomy and FASTA file
Take in tab delimited taxonomy file
take in fasta file 
 
"""

import sys, os, re, argparse,glob
import subprocess as sp 
from Bio import SeqIO
import numpy as np
#
if sys.version_info < (2,7):
    print "Python 2.7+ are needed for script"
    sys.exit()
##
def print_seq_stats(length_array):
    print "Minimum length is ", min(length_array)
    print "Max length ",max(length_array)
    print "mean of length is ", np.mean(length_array)
    print "median of length is ", np.median(length_array)
    print "Standard Dev of length is ", np.std(length_array)

#}}}function ends  
#}}}function ends
#
def open_fasta(fasta_file):
    
    seq_with_n=[] #array to store seq ids with Ns
    count=0 #total seqs --
    
    for record in SeqIO.parse(fasta_file,"fasta"):
        #add_seq_length.append(len(record))
        count+=1
        if (record.seq).find('N')!=-1 or (record.seq).find('n')!=-1:
            seq_with_n.append(record.id)
            #print (record.seq).count('N'), (record.seq).count('n')
        else:
            pass
        #if ends
    #for loop ends

    print "Sequences with Ns ",len(seq_with_n)
    for i in seq_with_n:
        print i
    #--for loop ends
    print "Total seqs in fasta file ",count
    #print_seq_stats(add_seq_length) #send seq-length array to calculate mean...
    print "Seqeucnes that can be used ",count-len(seq_with_n)
    
#
if __name__=="__main__": 
#{{{ main starts
    parser=argparse.ArgumentParser("description")
    parser.add_argument ('-f','--fasta',help='location/path of seqs file',required=True) # store seqs file
    parser.add_argument ('-t','--tax',help='location/path of taxonomy file',required=True) # store taxonomy file
    parser.add_argument ('-o','--out',help='location/path of output',required=True) # store output dir 
    args_dict = vars(parser.parse_args()) # make them dict.. 
    open_fasta(args_dict["fasta"])

#}}} main ends
