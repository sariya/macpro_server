#!/usr/bin/env python

__date__="May 4 2017"
__location__="SEH 7th Floor"
__author__="Sanjeev Sariya"

long_description="""
This is used after dereplication and clustering step to identify species that are close
This print seqs id and their taxonomy that are found replicate after running VSEARCH

vsearch --derep_full extracted_seq.fasta  --output full_derep.fasta --log=log --sizeout --minuniquesize 1

vsearch -cluster_fast full_derep.fasta -id 1 --sizein --sizeout --relabel OTU_  --centroids otus.fna

vsearch -usearch_global extracted_seq.fasta -db otus.fna -strand plus -id 1 -uc otu_table_mapping.uc

Take tabtsv file generated from drive5 from Robert Edgar 
Take taxonomy file of seqs with or without header. If header present then run as:

#python find_duplicate_seqs/find_duplicateseq.py -o ./ -x 6_tax.txt -t tabotu_table.tsv -r #will make this variable True    

else
#python find_duplicate_seqs/find_duplicateseq.py -o ./ -x 6_tax.txt -t tabotu_table.tsv #will make this variable False      

"""
import sys,os, argparse,re
from Bio import SeqIO

def get_species_name(temp_taxonomy,header_flag):
    """
    take tsv taxonomy file and flag for header. Header may be present or may not be.
    Return dictionary with seqid and and its species name 
    """
    taxonomy_dict={} #store seqid and their taxonomy  and return
    
    with open(temp_taxonomy) as tax_handle:

        if header_flag==True:
            next(tax_handle) #skip first line if header present
        else:
            pass
        for line in tax_handle:
            split_array=re.split('\s+',line.rstrip())
            #taxonomy_dict[split_array[0]]='\t'.join(str(x) for x in split_array[1:])
            taxonomy_dict[split_array[0]]=split_array[7]
        #--for ends
    #--with ends

    return taxonomy_dict

    #-----------------------------------------
    #Function ends--<>>
    #---------------------------------
def get_seqids(temp_file):
    header="" #hold header
    
    seqid_dict={} #number and seqids stored and returned
    
    with open(temp_file) as read_handle:
        header=read_handle.readline().rstrip()
        #http://stackoverflow.com/a/1904455 #read only header of tsv file
    #--

    tab_array=re.split('\s+',header) #split by spaces

    for i in range(1,len(tab_array)):
        seqid_dict[i]=tab_array[i] #store in dictionary
    #---for iteration over split tab array ends

    return seqid_dict
    #------------------------
    #
    #----------------
def find_replicate_taxonomy(temp_dict_seqid,temp_tab,temp_tax_dict):

    with open(temp_tab) as handle:
        next(handle) # skip header
        for line in handle:
            line = line.rstrip()
            if "size=1;" in line:                
                count_array=re.split('\s+',line)
                index=count_array.index("1")
                #print temp_dict_seqid[index],temp_tax_dict[temp_dict_seqid[index]]
            else:

                count_array=re.split('\s+',line)
                indices=[ i for i,x in enumerate(count_array[1:]) if x=="1" ]
                #print len(indices),indices
                
                st=""
                for i in indices:
                    #print count_array[0],i, "is present in dict",temp_dict_seqid[i+1],temp_tax_dict[temp_dict_seqid[i+1]]
                    #st+=temp_tax_dict[temp_dict_seqid[i+1]]+"\t"
                    st=st+temp_dict_seqid[i+1]+"\t"+temp_tax_dict[temp_dict_seqid[i+1]]+"\t"
                #--
                print st
            #if size check ends
        #-for loop ends
    #-with handle ends
        
    #---------------------------------------------
    #
    #----------------------------------
if __name__=="__main__":

    parser=argparse.ArgumentParser("description")
    parser.add_argument ('-o', '--out_dir', help='output direct',required=True) # store output direc
    parser.add_argument ('-t', '--tabfile', help='tab delimited otu file',required=True) # store TSV file generated from drive5
    parser.add_argument ('-x', '--tax', help='taxonomy file',required=True) # store taxonomy file
    parser.add_argument ('-r', '--header', help='header in taxonomy, true or false',action='store_true',default=False) # store taxonomy file
    args_dict = vars(parser.parse_args()) # make them dict..
    
    taxonomy_file=os.path.abspath(args_dict['tax'])
    tab_file=os.path.abspath(args_dict['tabfile'])
    out_dir=os.path.abspath(args_dict['out_dir'])
    header_flag=args_dict['header'] #if header in taxonomy file present or not. Default False
    #python find_duplicate_seqs/find_duplicateseq.py -o ./ -x 6_tax.txt -t tabotu_table.tsv -r #will make this variable True
    #python find_duplicate_seqs/find_duplicateseq.py -o ./ -x 6_tax.txt -t tabotu_table.tsv #will make this variable False

    seqid_dict=get_seqids(tab_file) #gets seqid 1,2,3,4
    tax_dict=get_species_name(taxonomy_file,header_flag) #seqid and species name
    find_replicate_taxonomy(seqid_dict,tab_file,tax_dict)
