#!/usr/bin/env python

#Sanjeev Sariya Sept 14 2016 Price Lab SEH 7th Floor, DC

long_description="""
run script as:
python remove_seq.py -fa fasta file

This script is used to get rid of sequences from input fasta file which 
failed Probe match test 
Takes input list of seq identifiers which don't have For & Rev primers hit

"""

import sys,re, argparse, os
from subprocess import Popen, PIPE
from Bio import SeqIO

def store_seq_id(in_list):
    
    id_list=[] #store seqs ids
    
    with open(in_list) as read:
        for line in read:
            if line.rstrip() not in id_list:
                id_list.append(line.rstrip())
            else:
                print "duplicate ",line.rstrip()
                sys.exit()#exit script
            #if check ends
        #for loop ends
    #} with ends
    return id_list
    #}
    
def remove_bad_seq(in_fasta,temp_list):
    
    #fasta file and array of seqs ids
    count_seqs_left=0
    for record in SeqIO.parse(in_fasta,"fasta"):
        if record.id not in temp_list:
            count_seqs_left+=1
            with open("seqs_remain.fasta",'a') as write_handle:
                write_handle.write(">"+str(record.description)+"\n"+str(record.seq)+"\n")
            #print record.id
        #if check ends
    #} for loop ends
    print "seqs left are  ", count_seqs_left
#} function ends---->
    
if __name__=="__main__":

    parser=argparse.ArgumentParser("description")
    parser.add_argument ('-fa', '--fasta', help='path for fasta file',required=True) # store fasta file
    parser.add_argument ('-l', '--list', help='path for input list',required=True) # store probe output file
    args_dict = vars(parser.parse_args()) # make them dict..

    seq_id=store_seq_id(os.path.abspath(args_dict['list']))
    remove_bad_seq(os.path.abspath(args_dict['fasta']),seq_id)
