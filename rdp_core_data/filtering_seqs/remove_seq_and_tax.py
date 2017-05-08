#!/usr/bin/env python

__date__="May 08th 2017"
__location__="SEH 7th Floor"
__author__="Sanjeev Sariya"

long_description="""
Take FASTA, taxonomy and seqids files.
Seq id file are ids that are duplicate or filterest after primer test.
Remove duplicates from FASTA and taxonomy file and print to output file

"""
import sys,os, argparse,re
from Bio import SeqIO
def get_seqid(temp_file):

    temp_list=[] #store ids and return
    with open(temp_file) as handle:
        for line in handle:
            line =line.rstrip()
            temp_list.append(line)
        #--for loop ends
    #---with ends
    return temp_list
#-----------
#
#-------------
def filter_seqs(temp_list,temp_fasta):

    for record in SeqIO.parse(temp_fasta,"fasta"):
        if not record.id in temp_list:
            print ">"+record.id
            print record.seq
    #--for ends
    #------------
    #
    #-----------------
if __name__=="__main__":

    parser=argparse.ArgumentParser("description")
    parser.add_argument ('-f', '--fasta', help='location for fasta file',required=True) # store input fasta file
    parser.add_argument ('-o', '--out_dir', help='output direct',required=True) # store output direc
    parser.add_argument ('-s', '--seq', help='location for text file',required=True) # store input file for seq ids
    parser.add_argument ('-t', '--tax', help='location for taxonomy file',required=True) # store input file for taxonomy file
    args_dict = vars(parser.parse_args()) # make them dict..
    
    seqid_file=os.path.abspath(args_dict['seq']) #store FASTA file
    fasta_file=os.path.abspath(args_dict['fasta']) #store fasta file
    output_dir=os.path.abspath(args_dict['out_dir']) #store output file
    tax_file=os.path.abspath(args_dict['tax']) #store taxonomy file
    seqid_list=get_seqid(seqid_file)

    filter_seqs(seqid_list,fasta_file)
