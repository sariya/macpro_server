#!/usr/bin/env python

__date__="April 18 2017"
__location__="SEH 7th Floor"
__author__="Sanjeev Sariya"

long_description="""
Take list of seq ids in for of text file and 
get their taxonomy from RDP core unaligned FASTA file
Take putput as another input parameter
"""

import sys,os, argparse,re
from Bio import SeqIO

def replace_special_chr(temp_word):

    #-replace special characters!
    temp_word=temp_word.replace('T','') #replace Type strain info with blank
    temp_word=temp_word.replace("'",'')
    temp_word=temp_word.replace('"','')
    temp_word=temp_word.replace('(','')
    temp_word=temp_word.replace(')','')
    temp_word=temp_word.replace('.','')
    temp_word=temp_word.replace('+','')
    return temp_word

#-------------------------------------------------------------------------
#
#-------------------------------------------------------------------------
                                        
def get_species_rdpdump(seqids_list,temp_fasta,temp_out):

    taxonomy_dict={} #7 array and seq id
    complete_lineage={} #seqid and lineage string
    
    for record in SeqIO.parse(temp_fasta,"fasta"):

        if record.id in seqids_list:
            
            complete_lineage[record.id]=replace_special_chr(record.description)
            #store it in the dict and return later on
            
            record_info=replace_special_chr((record.description))
            lineage_index=record_info.index("Lineage")
            record_info=record_info[:lineage_index-1] #take name until before space .

            if ';' in record_info:
                accession_info=re.split(';',record_info) #--split if information before lineage
                #-- if ; prsent after lineage trim then you'd have

            else: #else do not split
                accession_info=record_info

            if type(accession_info) is list:
                acn_sp_name=re.split('\s+',accession_info[0])
                #-- if array after splitting using ; - if array then 0th position is accession number and speccies name

            else:
                acn_sp_name=re.split('\s+',accession_info)
                #-- else complete info in one piece          
            
            index=1 #0th is seq identifier
            new_spc="" #--temp spec name

            while index<len(acn_sp_name):
                if index==1:
                    new_spc=new_spc+acn_sp_name[index]
                else:
                    if acn_sp_name[index]:  #add only names and not spaces
                        new_spc=new_spc+"_"+acn_sp_name[index]
                index+=1
            seq_id=acn_sp_name[0] ###seq_id is thereafter used in dict and printing FASTA file

            if not seq_id in taxonomy_dict:
                #if seq_id not present in training FASTA's dict.

                taxonomy_dict[seq_id]=[None]*7
                taxonomy_dict[seq_id][6]=new_spc

            if not taxonomy_dict[seq_id][6] == '-':
                 with open(temp_out+"/"+"new_species_seq.fasta",'a') as wrt_handle:
                     wrt_handle.write(">"+seq_id+"\n")
                     wrt_handle.write(str(record.seq)+"\n")
                     #--with write for sequences and species name ends ----
            else:
                print "No species level taxonomy ", seq_id
                            
        #--if ends
    #for loop ends

    return (taxonomy_dict,complete_lineage)
    #--------------------------
    #
    #------------------------
    
def parse_lineage(tmp_species_dict,tmp_lineage):
    """
    For each seq id in lineage we'll parse lineage infor
    put into dict with genus and other array indices
    """

    for x in tmp_lineage:
        details=tmp_lineage[x]
        
        if "rootrank" in details:
            root_index=(details).index("rootrank") #find index      
            tax_ranks=details[root_index+9:] # - trim ranks from that index
            tax_ranks=replace_special_chr(tax_ranks)
            tax_ranks=tax_ranks.replace(' ','_')
            ranks_array=re.split(';',tax_ranks)
            
            index=0
            
            #------------------------------------>>><<<<<<<<<<<

            for k in ranks_array:
                
                if k=="domain":
                    #0th index in array
                    tmp_species_dict[x][0]=ranks_array[index-1]

                if k=="phylum":
                    #1st index in array
                    tmp_species_dict[x][1]=ranks_array[index-1]
                    
                if k=="class":
                    #2nd index in array
                    tmp_species_dict[x][2]=ranks_array[index-1]

                if k=="order":
                    #3rd index in array
                    tmp_species_dict[x][3]=ranks_array[index-1]
                                                                                                                                                        
                if k=="family":
                    #4th index in array
                    tmp_species_dict[x][4]=ranks_array[index-1]
                                                                                                                                                    
                if k=="genus":
                    #5th index in array
                    tmp_species_dict[x][5]=ranks_array[index-1]
                index+=1

            #-----------------------------------<<<<<>>>>>>>>>#################
        else:
            print "Root rank missing ",x 
        
    #--for loop ends
    return tmp_species_dict 
    
    #--------------------------------------------
    #
    #-------------------------------------------
def readtext(textfile):

    #
    # Read text file to get seqids.
    # Store them in list and return to main function
    #
    seqids_list=[]
    with open (textfile) as seq_handle:
        for line in seq_handle:
            line=line.rstrip()
            seqids_list.append(line)
        #--for loop ends
    #--with ends
    return seqids_list
    #----------------------
    #
    #----------------------
if __name__=="__main__":

    parser=argparse.ArgumentParser("description")
    parser.add_argument ('-f', '--rdpfasta', help='location for fasta file',required=True) # store input RDP fasta file
    parser.add_argument ('-o', '--out_dir', help='output direct',required=True) # store output direc
    parser.add_argument ('-t', '--text', help='location for text file',required=True) # store input text file                
    args_dict = vars(parser.parse_args()) # make them dict..
    text_file=os.path.abspath(args_dict['text'])
    output_dir=os.path.abspath(args_dict['out_dir'])
    rdp_dump=os.path.abspath(args_dict['rdpfasta'])

    seqids_list=readtext(text_file)
    #get seq ids..
    
    tax_dict,lineage_dict=get_species_rdpdump(seqids_list,rdp_dump,output_dir)
    #tax dict with seq id and species level info
    #lineage dict will have seq id and complete lineage
    
    tax_dict=parse_lineage(tax_dict,lineage_dict)

    #--print taxonomy ot in text file. Tab delimited
    for i in tax_dict:
        st=""
        st=i
        for k in tax_dict[i]:
            st=st+"\t"+k
            
        with open(output_dir+"/"+"newtaxonomy.txt",'a') as tax_handle:
            tax_handle.write(st+"\n")

        #--with ends
    #--for loop ends
    #-- print ends
    
    print "Missing ids from FASTA and tax file"
    print set(seqids_list).difference(set(tax_dict.keys()))
                        
    print "Check output directory for new_species_seq.fasta, newtaxonomy.txt"
