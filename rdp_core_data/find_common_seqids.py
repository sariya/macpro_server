#!/usr/bin/env python

__date__="April 25 2017"
__location__="SEH 7th Floor"
__author__="Sanjeev Sariya"

long_description="""

Take Two FASTA files and find count in each
File one is the sink with which file two wiil be compared

Will be using sets to find intersection, duplicates

"""

import sys,os, argparse,re
from Bio import SeqIO

def get_seq_ids(temp_file):
    """

    Get FASTA file and extract their seq ids
    Check for duplicates And return them to the main function
 
    """
    temp_seq_list=[] #return this list
    
    for record in SeqIO.parse(temp_file,"fasta"):
        temp_seq_list.append(record.id)
    #--for loop ends

    if len(temp_seq_list)!=len(set(temp_seq_list)):
        print "We have duplicates in ",temp_file
    #--
    return temp_seq_list
    #-------
    ###------
    ###------------

def find_intersection(main_set,tocheck_set):

    value=(main_set).intersection(tocheck_set)
    print "Common seq ids ",len(value)
    for k in value:
        print k
    #--for loop ends -->>
    #-----
    #
    #-----
def find_difference(main_set,tocheck_set):
    """ 
    Find extra ids present in main fasta file
    Input recieved are list objects
    """
    value=list(set(main_set) - set(tocheck_ids))
    #Source: http://stackoverflow.com/questions/15455737/python-use-set-to-find-the-different-items-in-list
    
    print "Different Ids in main ",len(value)
    print value

    #--------------------
    #
    #---------------------
if __name__=="__main__":

    parser=argparse.ArgumentParser("description")
    parser.add_argument ('-f1', '--file1', help='location for fasta file',required=True) # store input fasta file one
    parser.add_argument ('-f2', '--file2', help='output direct',required=True) # store input FASTA file two
    args_dict = vars(parser.parse_args()) # make them dict..
    main_file=os.path.abspath(args_dict['file1'])
    file_to_check=os.path.abspath(args_dict['file2'])
    
    main_seqids=get_seq_ids(main_file)
    tocheck_ids=get_seq_ids(file_to_check)
    print "Received all seq ids in FASTA files"
    find_intersection(set(main_seqids),set(tocheck_ids))

    print "Found out the intesection of two seq ids"
    find_difference(main_seqids,tocheck_ids)
    print "Found out additional ids in main FASTA file"
