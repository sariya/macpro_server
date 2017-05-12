#!/usr/bin/env python

__date__="May 12 2017"
__location__="SEH 7th Floor"
__author__="Sanjeev Sariya"

long_description="""
Take extracted seqeunce file and  seqid in arguments
Print length of seqid, if present
 
"""

import sys,os, argparse,re
from Bio import SeqIO

def print_length(temp_fasta, temp_id):
    
    found=0 #flag to check if seqid is foun
    
    for record in SeqIO.parse(temp_fasta,"fasta"):
        if record.id == temp_id:
            found=1
            print len(record.seq)
        #--if record id found
    #--for loop ends
    if found==0:
        print "Sequence id is not present in FASTA file provided!"
    #--if not found ..<>
    #---------------------
    #
    #----------------------
if __name__=="__main__":

    parser=argparse.ArgumentParser("description")
    parser.add_argument ('-f', '--fasta', help='location for fasta file',required=True) # store input fasta file
    parser.add_argument ('-s', '--seqid', help='seq id name',required=True) # store sequence id for which length is neede
    
    args_dict = vars(parser.parse_args()) # make them dict..
    fasta_file=os.path.abspath(args_dict['fasta'])
    seq_id=args_dict['seqid']
    
    print_length(fasta_file,seq_id)
    print "<-Done with finding length. Bye->"
    
