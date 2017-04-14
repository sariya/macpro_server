#!/usr/bin/env python

__date__="April 5 2017"
__location__="SEH 7th Floor"
__author__="Sanjeev Sariya"

long_description="""
Take list of seq ids that are to be extracted from  FASTA file
Output in new fasta file in output directory provided

Training FASTA from source forge RDP and current unaligned FASTA from RDP resources. 
We need to extract sequences only present in Training FASTA file
"""

import sys,os, argparse,re
from Bio import SeqIO

def read_seqs_id(temp_file):
    
    seq_list=[] #store seqs ids
    
    
    with open(temp_file) as temphandle:
        for line in temphandle:
            line=line.rstrip()
            seq_list.append(line)
        #--for loop ends
    #---with loop ends
    print len(seq_list)
    return seq_list
    #-----------------------
    #
    #-----------------------
def print_seqs(temp_list,temp_fasta,temp_out):

    count=0
    found_seqid=[]
    for record in SeqIO.parse(temp_fasta,"fasta"):
        
        if record.id in temp_list:

            with open(temp_out+"/"+"extracted_seq.fasta",'a') as write_handle:
                write_handle.write(">"+record.description+"\n")
                write_handle.write(str(record.seq)+"\n")
            #--with ends
    
            count+=1
            found_seqid.append(record.id)
        
        #--if check ends
    #--for loop ends

    print len(found_seqid)
    #---------------------
    #
    #---------------------
if __name__=="__main__":

    parser=argparse.ArgumentParser("description")
    parser.add_argument ('-f', '--fasta_file', help='location for fasta file',required=True) # store input fasta file
    parser.add_argument ('-o', '--out_dir', help='output direct',required=True) # store output direc
    parser.add_argument ('-s', '--seqid', help='input seq id list',required=True) # store input seq id list
            
    args_dict = vars(parser.parse_args()) # make them dict..

    list_seqids=read_seqs_id(os.path.abspath(args_dict['seqid']))
    print_seqs(list_seqids,os.path.abspath(args_dict['fasta_file']),os.path.abspath(args_dict['out_dir']))
    
