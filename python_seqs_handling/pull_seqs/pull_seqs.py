#!/usr/bin/env python

__date__="May 04 2017"
__location__="SEH 7th Floor"
__author__="Sanjeev Sariya"

long_description="""
take in seq ids in a text file
take in fasta file in fasta file
pull seqs of seq ids in text from FATA file. 
take output directory and print in a file
"""

import sys,os, argparse,re
from Bio import SeqIO

def get_ids(seqid_file):
    
    """
    Return list of seq ids
    """
    id_list=[] #store ids and return

    with open(seqid_file) as handle:
        id_list=[line.rstrip() for line in handle] #http://stackoverflow.com/a/20756176 Need to improve python with these kinds of hacks!!!
        
    #--with loop ends

    return id_list
    #-------------------------
    #
    #-----------------------
def print_seqs(temp_list,temp_fasta,temp_out):
    out_file=temp_out+"/"+"extracted_seq.fasta"

    for record in SeqIO.parse(temp_fasta,"fasta"):
        if record.id in temp_list:
            with open(out_file,'a') as w_handle:
                w_handle.write(str(">"+record.description+"\n"+record.seq)+"\n")
            #--with write ends
        #if found in seq list
    #--for loop for seqio ends

    #-------------------------
    #
    #-------------------------
if __name__=="__main__":

    parser=argparse.ArgumentParser("description")
    parser.add_argument ('-f', '--fasta_file', help='location for fasta file',required=True) # store input fasta file
    parser.add_argument ('-o', '--out_dir', help='output direct',required=True) # store output direc
    parser.add_argument ('-s', '--seqid', help='input seq id list',required=True) # store input seq id list
    args_dict = vars(parser.parse_args()) # make them dict..

    output_dir=os.path.abspath(args_dict['out_dir']) #output dir
    seqid_file=os.path.abspath(args_dict['seqid']) #seq id text file
    fasta_file=os.path.abspath(args_dict['fasta_file']) #fasta file
    
    id_list=get_ids(seqid_file)
    print_seqs(id_list,fasta_file,output_dir)
    print "Check output dir for extracted_seq.fasta"
