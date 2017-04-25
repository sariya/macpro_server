#!/usr/bin/env python

__date__="April 25th 2017"
__location__="SEH 7th Floor"
__author__="Sanjeev Sariya"

long_description="""
Take taxonomy file and seqids file.
Seq id file are ids that are duplicate.
Remove duplcaites from taxonomy file and print in output file
"""

import sys,os, argparse,re

def get_seqid(temp_file):
    
    temp_list=[] #store ids and return
    with open(temp_file) as handle:
        for line in handle:
            line =line.rstrip()
            temp_list.append(line)
        #--
    #---
    return temp_list

    #-----------
    #
    #-------------


def parse_taxonomy(temp_list,temp_taxonomy):
    
    with open(temp_taxonomy) as handle:
        for line in handle:
            split_array=re.split('\s+',line.rstrip())

            if not split_array[0] in temp_list:
                print line.rstrip()
            #-if ends
        #for loop ends
    #--with open ends
    #--------------------
    #
    #--------------------
if __name__=="__main__":

    parser=argparse.ArgumentParser("description")
    parser.add_argument ('-o', '--out_dir', help='output direct',required=True) # store output direc
    parser.add_argument ('-t', '--tax', help='location for text file',required=True) # store input taxonomy file
    parser.add_argument ('-s', '--seq', help='location for text file',required=True) # store input seq id file    
    args_dict = vars(parser.parse_args()) # make them dict..

    seqid_file=os.path.abspath(args_dict['seq'])
    tax_file=os.path.abspath(args_dict['tax'])
    output_dir=os.path.abspath(args_dict['out_dir'])

    seqid_list=get_seqid(seqid_file)
    parse_taxonomy(seqid_list,tax_file)
    
