#!/usr/bin/env python

__date__="April 18 2017"
__location__="SEH 7th Floor"
__author__="Sanjeev Sariya"

long_description="""
Take list of seq ids in for of text file and 
get their taxonomy from RDP core unaligned FASTA file
Take putput as another input parameter
"""

import sys,os, argparse,re
from Bio import SeqIO

if __name__=="__main__":

    parser=argparse.ArgumentParser("description")
    parser.add_argument ('-f', '--rdpfasta', help='location for fasta file',required=True) # store input RDP fasta file
    parser.add_argument ('-o', '--out_dir', help='output direct',required=True) # store output direc
    parser.add_argument ('-t', '--text', help='location for text file',required=True) # store input text file                
    args_dict = vars(parser.parse_args()) # make them dict..
    text_file=os.path.abspath(args_dict['text'])
    output_dir=os.path.abspath(args_dict['out_dir'])
    rdp_dump=os.path.abspath(args_dict['rdpfasta'])

    print output_dir,rdp_dump,text_file
    

    
                        
