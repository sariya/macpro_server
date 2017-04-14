#!/usr/bin/env python

#Sanjeev Sariya
#Sept 8 2016
#Price Lab SEH 7th Floor, DC

long_description="""
run script as:
python parse_probe_match.py -p probe_output.txt 

"""

import sys,re, argparse,glob, os
from subprocess import Popen, PIPE
from Bio import SeqIO

def parse_probe_output_file(probe_op):

    seq_present={}
    with open(probe_op) as handle:
        handle.next() #skip headers
        
        for line in handle:
            
            line=line.rstrip()
            tab_array=re.split('\t',line)
            
            #parse into array, tab_array[3] is reverse or forward
            #tab_array[0] is seq id
            
            if tab_array[3] == "reverse":
                if tab_array[0] in seq_present:
                    seq_present[tab_array[0]]-=1
                    
                    """
                    make it zero

                    """
                else:
                    
                    """
                    For reverse the key assigned is negative
                    """
                    
                    seq_present[tab_array[0]]=-1
            #if for reverse
            
            elif tab_array[3] == "forward":

                if tab_array[0] in seq_present:
                    seq_present[tab_array[0]]+=1
                    
                else:
                    seq_present[tab_array[0]]=1
                    
                #if present
            #else for forward
                
        #} for loop ended
    #with handle ended
    
    #print len(seq_present)
    
    for k in seq_present:

        if seq_present[k] == -1:
            print "Only Reverse " , k
            
        if seq_present[k] == 1:
            print "Only forward ", k
#} def function ends

if __name__=="__main__":

    parser=argparse.ArgumentParser("description")    
    parser.add_argument ('-p', '--probe', help='path for probe output file',required=True) # store probe output file
    args_dict = vars(parser.parse_args()) # make them dict..
    parse_probe_output_file(os.path.abspath(args_dict['probe']))
