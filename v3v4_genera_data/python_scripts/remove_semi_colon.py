#!/usr/bin/env python

__date__="March 8 2017"
__location__="SEH 7th floor west offices, DC 20037"
__author__="Sanjeev Sariya"

"""

This script will remove information in 
seqeunce identifuier after semi colon from RDP downloaded files.

>S000408406 Porphyromonas asaccharolytica; 090703/22-6225; AY360344

anything after asaccharolytica is removed

give count of input sequence
give count of output seq
give seq id of the seqs that have been filtered out

 
"""

def print_seqs(temp_fasta_file):

    for record in SeqIO.parse(temp_fasta_file,"fasta"):

        info=record.description #store all infor in info variable 
        split_array=re.split(';',info)
        seq_iden=split_array[0] #get first info 
        seq_iden=seq_iden.replace(';','') #replace ; with nothing
        seq_iden=seq_iden.replace('.','') #replace  dot with nothing in species name
        
        species_name=re.split('\s+',seq_iden) #after replacing stuff now split them based on space
        modified_Species_name= '_'.join(species_name[1:]) #get species name filled with underscore to have better name
        
        print ">"+species_name[0]+" "+modified_Species_name
        print (record.seq).upper()
    #--for loop ends
    #---------------------------
    #function ends
    #--------------------------
    
from Bio import SeqIO
import os, argparse,sys,re
    #--------function ends
if __name__=="__main__":
    
    parser=argparse.ArgumentParser("description")
    parser.add_argument ('-fa', '--fasta_file', help='location for fasta file',required=True) # store input fasta file
    
    args_dict = vars(parser.parse_args()) # make them dict..
    print_seqs(os.path.abspath(args_dict['fasta_file']))

    #---script ends
