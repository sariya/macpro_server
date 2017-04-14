#!/usr/bin/env python

#Sanjeev Sariya
#Mar 9th 2017
#Price Lab SEH 7th Floor, DC

long_description="""
run script as:
python parse_probe_match.py -p probe_output.txt 

This script takes output from parse_probe_match.py script. 
Input is text file and FASTA file.

Goal - it would throw sequences from FASTA file
 
"""

import sys,re, argparse,glob, os
from subprocess import Popen, PIPE
from Bio import SeqIO

def get_list_seq_ids(temp_probe):

    seq_ids_array=[] #store seq ids from parsed probe output
    
    with open(temp_probe,'r') as probe_handle:
        for line in probe_handle:

            line=line.rstrip() #remove new line
            line_array=re.split('\s+',line) #split line by spaces

            if len(line_array)!=3:
                print "Got issue with line " #more splits
                sys.exit()
            #---if for length ends
            
            if line_array[2] in seq_ids_array:
                print line_array[2], " already present  "
                sys.exit() #if duplicates present
            #---if for seq id check if duplicate present
            
            seq_ids_array.append(line_array[2]) #append seq id to array
            
        #---for loop ends
    #---with ends
    
    return seq_ids_array
    #--------
    #Function ends
    #-------

def filter_seq(temp_list,temp_fast_file):

    for record in SeqIO.parse(temp_fast_file,'fasta'):
        
        if not record.id in temp_list:
            print ">"+record.description
            print record.seq

        #--if check for seq ids
    #--for loop for fasta sequence


    #---------------------
    #Function ends
    #----------------------
if __name__=="__main__":

    parser=argparse.ArgumentParser("description")
    parser.add_argument ('-p', '--probe', help='path for probe output file',required=True) # store probe output file
    parser.add_argument ('-fa', '--fasta', help='FASTA file',required=True) # store FASTA file
    args_dict = vars(parser.parse_args()) # make them dict..
    seq_ids_list=get_list_seq_ids(os.path.abspath(args_dict['probe']))

    filter_seq(seq_ids_list,os.path.abspath(args_dict['fasta']))
    #---script ends     #-------->
