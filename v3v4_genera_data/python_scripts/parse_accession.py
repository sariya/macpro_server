#!/usr/bin/env python

from Bio import SeqIO
import os, argparse,sys,re

"""

create tab delimited file for taxonomy input needed to 
generate RDP training set 
remove () with _
join species name with _ in them

"""
__date__="Sept 7 2016"
__location__="SEH 7th floor west offices, DC 20037"
__author__="Sanjeev Sariya"

def parse_fasta(temp_fasta):
    
    seq_taxonomy={} #hold seq id and its taxonomy
    taxonomy_count={} #store taxonomy and its occurance
    
    for record in SeqIO.parse(temp_fasta,"fasta"):
        desc_str=record.description
        desc_str=desc_str.replace(".","")#replace . with nothing
        desc_str=desc_str.replace("(","_")
        desc_str=desc_str.replace(")","_")
        array_semi=re.split(';',(desc_str)) #get until species name
        split_space=re.split('\s', array_semi[0])# split to get seq id and desc
        taxonomy_rank= "_".join(split_space[1:]) #hold the taxonomy. Join sp, PR and other things by _
        #print split_space
        seq_taxonomy[split_space[0]]=taxonomy_rank

        if taxonomy_rank in taxonomy_count:
            taxonomy_count[taxonomy_rank]+=1
        else:
            taxonomy_count[taxonomy_rank]=1
        #check ends if taxonomy exists in dict..
    #} for loop ends
    print "length of seq-taxo is ",len(seq_taxonomy)
    print "length of taxo count dict ",len(taxonomy_count)

    #print taxonomy-count to file
    for k in taxonomy_count:
        
        with open("tax_count.txt",'a') as tax_count_handle:
            tax_count_handle.write(k+"\t"+str(taxonomy_count[k])+"\n")

    #for loop ends for tax-count
    for i in seq_taxonomy:

        with open("sequence_tax.txt",'a') as seq_tax_handle:
            seq_tax_handle.write(i+"\t"+seq_taxonomy[i]+"\n")
        
#} function ends             ---->>

if __name__=="__main__":

    parser=argparse.ArgumentParser("description")
    parser.add_argument ('-fa', '--fasta_file', help='location for fasta file',required=True) # store input fasta file
    args_dict = vars(parser.parse_args()) # make them dict..
    parse_fasta(os.path.abspath(args_dict['fasta_file']))
                    
