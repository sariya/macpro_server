#!/usr/bin/env python

__date__="May 3 2017"
__location__="SEH 7th Floor"
__author__="Sanjeev Sariya"

long_description="""

Take in genus name, take in species name
Take in FASTA file current_Bacteria_unaligned.fa
These seqeunces are to be printed in an output directory

These sequences will be merged with previous RDP work
Remeber to remove duplcaites
"""
import sys,os, argparse,re
from Bio import SeqIO

if __name__=="__main__":

    parser=argparse.ArgumentParser("description")
    parser.add_argument ('-o', '--out', help='location for output',required=True) # store output dir
    parser.add_argument ('-f', '--fasta_file', help='location for fasta file',required=True) # store input fasta file
    parser.add_argument ('-g', '--genus', help='genus name',required=True) # store output direc
    parser.add_argument ('-s', '--species', help='species name',required=True) # store input seq id list
    
    args_dict = vars(parser.parse_args()) # make them dict..
                        
