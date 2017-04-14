#!/usr/bin/env python

from Bio import SeqIO
import os, argparse,sys,re

"""

take text file of seqs ids and fasta file
goal is to remove sequences and print them onto a new file 
on output directory

"""
__date__="March 16 2017"
__location__="SEH 7th floor west offices, DC 20037"
__author__="Sanjeev Sariya"

def filter_seqs(temp_text, temp_fasta,temp_out):

    seq_ids=[] #store seq ids in a list

    with open (temp_text) as id_handle:
        for line in id_handle:
            #print line
            line=line.rstrip()
            seq_ids.append(line)
            
        #--for loop ends
    ##--with ends
    
    #---read FASTA file
    for record in SeqIO.parse(temp_fasta,"fasta"):
        if record.id in seq_ids:
            with open (temp_out+"/"+"extracted_seqs.fa",'a') as write_handle:
                write_handle.write(">"+record.description+"\n")
                write_handle.write(str(record.seq)+"\n")
            #---with ends

        #--if loop ends for checking ids in list
    #-- for loop ends
            
    
    #-----------------
    #
    #----------------
if __name__=="__main__":
    
    parser=argparse.ArgumentParser("description")
    parser.add_argument ('-fa', '--fasta_file', help='location for fasta file',required=True) # store input fasta file
    parser.add_argument ('-t', '--text', help='location for text file',required=True) # store input text file
    parser.add_argument ('-o', '--out', help='location for output dir',required=True) # store output dir file
    args_dict = vars(parser.parse_args()) # make them dict..

    filter_seqs(os.path.abspath(args_dict['text']),os.path.abspath(args_dict['fasta_file']),os.path.abspath(args_dict['out']))

    print "<--Check output directory for extracted sequences-->"
