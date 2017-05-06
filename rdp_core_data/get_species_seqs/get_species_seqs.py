#!/usr/bin/env python

__date__="May 3 2017"
__location__="SEH 7th Floor"
__author__="Sanjeev Sariya"

long_description="""

Take in genus name, take in species name
Take in FASTA file current_Bacteria_unaligned.fa
These seqeunces are to be printed in an output directory

These sequences will be merged with previous RDP work
Remember to remove duplicates after printing these seqs and taxonomy--

current_Bacteria_unaligned.fa version 11.5 is used to get sequences
genus name and species name are case sensitive in input

python get_species_seqs.py -g Staphylococcus -s aureus -o ./ -f current_Bacteria_unaligned.fa
"""
import sys,os, argparse,re
from Bio import SeqIO

def replace_special_chr(temp_word):

    #-replace special characters!
    temp_word=temp_word.replace('T','') #replace Type strain T info with blank
    temp_word=temp_word.replace("'",'')
    temp_word=temp_word.replace('"','')
    temp_word=temp_word.replace('(','')
    temp_word=temp_word.replace(')','')
    temp_word=temp_word.replace('.','')
    temp_word=temp_word.replace('+','')
    
    return temp_word

    #--------------------------------------
    #
    #----------------------------------------
def check_taxonomy(temp_array,temp_seqid):
    
    """called from parsetaxonomy function to see if any value is None
    """
    for k in range(0,len(temp_array)):
        if temp_array[k] is None:
            temp_array[k]="-"
            print "Issues with ",temp_seqid
        else:
            pass
        #--if ends
    #for loop ends---->>>
    return temp_array #return edited or however it was --
    #---------------------------------------------
    #
    #------------------------------------------------
def parse_taxonomy(temp_desc,temp_file_name,seqid):
    """
    Called from get_seqs function
    This function will parse taxonomy and print it out in an output file
    """
    
    temp_desc=replace_special_chr(temp_desc)
    taxonomy_array=[None]*7 #store ranks in it and use it to print info
    
    lineage_indx=temp_desc.index("Lineage")
    temp_spc_name=temp_desc[:lineage_indx-1] #get info until lineage. it has seqid in it too

    species_name="" #store species name in this variable
    
    if ";" in temp_spc_name:
        #if semi colon present
        semi_colon_inx=temp_spc_name.index(";") #get index of semi colon .
        seq_temp_spc=temp_spc_name[:semi_colon_inx] #get string until first semi colon

        #print seqid,(seq_temp_spc[len(seqid)+1:]).replace(" ","_" ) # get species name for the seq id
        species_name=((seq_temp_spc.rstrip())[len(seqid)+1:]).replace(" ","_" ) #strip to remove extra space after (T) replacement
    else:
        #if no semi colon present ----
        #print seqid,(temp_spc_name[len(seqid)+1:]).replace(" ","_") #get speices name for the seq id
        species_name=((temp_spc_name.rstrip())[len(seqid)+1:]).replace(" ","_") #strip to remove extra space after (T) replacement

        #--got hold of species name
        #--time to parse other ranks -----
    #-----if for ; ends

    rootrank_index=temp_desc.index("rootrank;")
    
    taxonomy_string=temp_desc[rootrank_index+len("rootrank;"):] 
    split_tax_string=re.split(";",taxonomy_string)

    #--iterate over split taxonomy string
    index=0
    for k in range(0,len(split_tax_string)): #this I should have used ages ago!!
        if split_tax_string[k]=="domain":
            taxonomy_array[0]=split_tax_string[k-1]

        if split_tax_string[k]=="phylum":
            taxonomy_array[1]=split_tax_string[k-1]

        if split_tax_string[k]=="class":
            taxonomy_array[2]=split_tax_string[k-1]

        if split_tax_string[k]=="order":
            taxonomy_array[3]=split_tax_string[k-1]

        if split_tax_string[k]=="family":
            taxonomy_array[4]=split_tax_string[k-1]

        if split_tax_string[k]=="genus":
            taxonomy_array[5]=split_tax_string[k-1]

    #--for loop ends ----->>>>>>>>>>>>>
    taxonomy_array[6]=species_name #store species name in the end ---

    taxonomy_array=check_taxonomy(taxonomy_array,seqid)
    """
    If any of the index in array is None then replaced by - 
    """
    with open(temp_file_name,'a')as t_handle:
        t_handle.write(seqid+"\t"+"\t".join(x for x in taxonomy_array)+"\n")
        
    #--with write ends ------>>><<<<<<<

    #
    #
    #
def get_seqs(genus,species, fasta, outputdir):
    """
    This function prints seqs of your genus and species
    This also calls fucntion to get taxonomy and prints taxonomy
    """
    count=0 #keep count of seqs found
    
    seqs_file=outputdir+"/"+genus.lower()+"_"+species+"_seq.fasta"
    tax_file=outputdir+"/"+genus.lower()+"_"+species+"_tax.txt"

    for record in SeqIO.parse(fasta,"fasta"):
        if genus+";genus" in record.description:
            if genus+" "+species in record.description:
                parse_taxonomy(record.description,tax_file,record.id)
                
                with open(seqs_file,'a') as w_handle:
                    w_handle.write(">"+record.id+"\n"+str(record.seq)+"\n")
                #-with print ends
                count+=1
            #check if species name in description
        #check if genus name is of our interest and is present in the the description
    #--for loop ends for current file
    print "Sequences found of your genus and speies ",count
    #------------------------
    #
    #-----------------------
    
if __name__=="__main__":

    parser=argparse.ArgumentParser("description")
    parser.add_argument ('-o', '--out', help='location for output',required=True) # store output dir
    parser.add_argument ('-f', '--fasta', help='location for fasta file',required=True) # store input fasta file
    parser.add_argument ('-g', '--genus', help='genus name',required=True) # store output direc
    parser.add_argument ('-s', '--species', help='species name',required=True) # store input seq id list
    
    args_dict = vars(parser.parse_args()) # make them dict..
    output_dir=os.path.abspath(args_dict['out']) #output dir
    fasta_file=os.path.abspath(args_dict['fasta']) #fasta file
    genus_name=args_dict['genus'] #genus name
    species_name=args_dict['species'] #species nanme
    get_seqs(genus_name,species_name,fasta_file,output_dir)
    print "Check output dir with genus and species name files for sequences and taxonomy!"
    print "<<--Bye-Bye-->>"
