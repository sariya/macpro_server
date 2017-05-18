#!/usr/bin/env python

__date__="May 18 2017"
__location__="SEH 7th Floor"
__author__="Sanjeev Sariya"

long_description="""
Take two txt files and find common, intesection, missing ids
This script comes handy when finding duplcaites, missing ids or any other usual tasks
"""
import sys,os, argparse,re

def read_seqs_id(temp_file):
    #read text file and return list
    seq_list=[] #store seqs ids

    with open(temp_file) as temphandle:
        for line in temphandle:
            seq_list.append(line.rstrip())
        #-for loop ends
    #-with loop ends
    print "Seq ids found ",len(seq_list)
    return seq_list
    #-----------------------
    #
    #------------------------

def find_missing(list1, list2):
    """
    List1 has more ids than list2
    """
    value=list(set(list1) - set(list2))
    print value
    #--------------------------
    #
    #----------------------
if __name__=="__main__":

    parser=argparse.ArgumentParser("description")
    parser.add_argument ('-t1', '--txt1', help='location for fasta file',required=True) # store input seqid file one
    #this has more ids than text2
    parser.add_argument ('-t2', '--txt2', help='output direct',required=True) # store input seqid file two
    args_dict = vars(parser.parse_args()) # make them dict..
    list_seqids_txt1=read_seqs_id(os.path.abspath(args_dict['txt1'])) #get seq ids list for txt1 file
    list_seqids_txt2=read_seqs_id(os.path.abspath(args_dict['txt2'])) #get seq ids list for txt2 file
    
    find_missing(list_seqids_txt1,list_seqids_txt2)
