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
if __name__=="__main__":

    parser=argparse.ArgumentParser("description")
    parser.add_argument ('-f', '--fasta_file', help='location for fasta file',required=True) # store input fasta file
    parser.add_argument ('-o', '--out_dir', help='output direct',required=True) # store output direc
    parser.add_argument ('-s', '--seqid', help='input seq id list',required=True) # store input seq id list
    args_dict = vars(parser.parse_args()) # make them dict..

    output_dir=os.path.abspath(args_dict['out_dir']) #output dir
    seqid_file=os.path.abspath(args_dict['seqid']) #seq id text file
    fasta_file=os.path.abspath(args_dict['fasta_file']) #fasta file
    
