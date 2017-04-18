#!/usr/bin/env python

__date__="April 5 2017"
__location__="SEH 7th Floor"
__author__="Sanjeev Sariya"

long_description="""
Take extracted seqeunces from RDP based on training set available online
and create a tab delimited taxonomy
 
"""

import sys,os, argparse,re
from Bio import SeqIO

count_genus_species={}

#- This will be used to store count of uncultured and other
# unidentified, conflicting species 

def compare_fasta(temp_rdp_fasta,temp_train_fasta,tempout):

    missings_ids=[]
    record_train = list(SeqIO.parse(temp_train_fasta, "fasta"))
    record_rdp = SeqIO.to_dict(SeqIO.parse(temp_rdp_fasta, "fasta"))
    
    print "Total records in RDP FASTA ",len(record_rdp)
    print "Total records in training FASTA ",len(record_train)

    rdp_record_ids=list(record_rdp.keys()) #get record ids
   
    ids_found_in_rdp=0
    
    for i in record_train:

        seq_id=re.split('\|',( (i.id).rstrip() )  )[1] #this is going to be used in dict later stages

        if seq_id in rdp_record_ids:
            ids_found_in_rdp+=1
        else:
            missings_ids.append(seq_id)
        #--if
    #-----For loop ends
    
    print "Check trainingids_missingRDPCore.txt in outut directory"
    
    with open(tempout+"/"+"trainingids_missingRDPCore.txt",'a') as missing_handle:
        for k in missings_ids:
            missing_handle.write(k+"\n")
        #--
    #----
    
    print "Length of missing training ids from RDP Dump", len(missings_ids) ,"Printed in file trainingids_missing.txt"
    print "Training Ids found in RDP FASTA ",ids_found_in_rdp
    #----
    #
    #
    #--------------------------------------------------
    
def print_fasta_file(temp_fasta,temp_out,temp_dict):

    #fasta file is RDP database. Temp dict is tax rank from training FASTA file
    
    seqid_fasta=0
    print "Check species_seq.fasta in output directory"
    for record in SeqIO.parse(temp_fasta,"fasta"):

        seqid_fasta+=1
        record_info=replace_special_chr((record.description))
        
        t=record_info.index("Lineage")
        record_info=record_info[:t-1] #take name until before space .
        
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
        #--add _ to different splits of species name if present
        
        while index<len(acn_sp_name):
            if index==1:
                new_spc=new_spc+acn_sp_name[index]
            else:
                new_spc=new_spc+"_"+acn_sp_name[index]
            index+=1
            
        #----Loop ends for joining strings
        #Kingdom Phylum Class Order Family Genus Species - 7 length of array for seq identifier

        seq_id=acn_sp_name[0] ###seq_id is thereafter used in dict and printing FASTA file
        
        if not seq_id in temp_dict:
            #if seq_id not present in training FASTA's dict.

            temp_dict[seq_id]=[None]*7
            temp_dict[seq_id][6]=new_spc
           
        else:
            #using information from training FASTA file
            temp_dict[seq_id][6]=new_spc
            
        #---store in dictionary for future use

        if not temp_dict[seq_id][6] == '-':
            
            with open(temp_out+"/"+"species_seq.fasta",'a') as wrt_handle:
                wrt_handle.write(">"+seq_id+"\n")
                wrt_handle.write(str(record.seq)+"\n")
            #--with write for sequences and species name ends ----
        else:
            print "No species level taxonomy ", seq_id

    #--for loop ends for FASTA file
    
    return temp_dict #-- send seq id and their species to main function called
        
    #---------------------
    #
    #----------------------

def replace_special_chr(temp_word):

    #-replace special characters!
    
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

def get_taxonomy(temp_fasta,dict_species_seqids,temp_out,list_train_seqids):

    #-fasta file is RDP database and not training FASTA
    count_species_not_found=0

    species_not_found=[] #list stores for which speices is not found in RDP big file
    #returned at the end of function
    
    for record in SeqIO.parse(temp_fasta,"fasta"):

        if not record.id in list_train_seqids:
            
            if "rootrank" in record.description:
                
                root_index=(record.description).index("rootrank") #find index
                tax_ranks=record.description[root_index+9:] # - trim ranks from that index
                
                tax_ranks=replace_special_chr(tax_ranks)
                tax_ranks=tax_ranks.replace(' ','_')
                ranks_array=re.split(';',tax_ranks)
            
                x=0 #iterate over array- position thing #length_ranks_array=len(ranks_array)
            
                for k in ranks_array:
                    
                    if k=="domain":
                        #0th index in array
                        dict_species_seqids[record.id][0]=ranks_array[x-1]
                    
                    if k=="phylum":
                        #1st index in array
                        dict_species_seqids[record.id][1]=ranks_array[x-1]
                    
                    if k=="class":
                        #2nd index in array
                        dict_species_seqids[record.id][2]=ranks_array[x-1]
                    
                    if k=="order":
                        #3rd index in array
                        dict_species_seqids[record.id][3]=ranks_array[x-1]
                    
                    if k=="family":
                        #4th index in array
                        dict_species_seqids[record.id][4]=ranks_array[x-1]
                    
                    if k=="genus":
                        #5th index in array
                        dict_species_seqids[record.id][5]=ranks_array[x-1]

                    x+=1
                #--for loop over rank array ends
                    
            #--if rootrank split
            else:
                print "We're having issues with record description ", record.id
        #--if check ends for id in train_seqids.
            
    #--for record bio loop ends
    print "Check tab_taxonomy.txt in output directory "    
    for seq_id in dict_species_seqids:
        
        taxonomy_string=""
        #--tab delimited to print in the end
        
        temp_array=dict_species_seqids[seq_id]

        index=0

        for p in temp_array:
            
            if p == "" and index==6:
                p=temp_array[5]+"_unclassifiedsp"
                print "Species missing ",seq_id
                dict_species_seqids[seq_id][index]=temp_array[5]+"_unclassifiedsp"
                
            if p==None:
                #genus, family whatever has no value would be set as -.
                #sometimes species will also be set as - so be mindful
                dict_species_seqids[seq_id][index]="-"
            #---if check ends
            
            index+=1
        #---for loop ends
        
        taxonomy_string=seq_id
        species_name=temp_array[6]
        parse_species(dict_species_seqids,species_name,temp_array[5])

        if not dict_species_seqids[seq_id][6]=='-':
            #if species not a dash
            for p in temp_array:
            
                taxonomy_string=taxonomy_string+"\t"+p
            #---for loop ends for concatenation

            with open (temp_out+"/"+"tab_taxonomy.txt",'a') as tax_handle:
                tax_handle.write(taxonomy_string+"\n")
            #---with loop ends for writing into file
        else:
            
            #all these are sequeneces that aren't found in RDP's database of 3 million

            index=0
            while index<6: #go until genus level as species name is -
                
                #for p in temp_array:       
                taxonomy_string=taxonomy_string+"\t"+temp_array[index]                 #---for loop ends for concatenation

                index+=1
            #--while looop ends
            
            taxonomy_string=taxonomy_string+"\t"+seq_id+"_"+temp_array[5]

            with open (temp_out+"/"+"tab_taxonomy.txt",'a') as tax_handle:
                tax_handle.write(taxonomy_string+"\n")
            #---with loop ends for writing into file

            #-
            species_not_found.append(seq_id)
            count_species_not_found+=1
    #dict for loop ends-------

    print "Species not found for training sequences ", count_species_not_found
    print "Check species_missing_ids.txt in output directory. These are missing from RDP's DUMP data "
    
    for k in species_not_found:
        with open(temp_out+"/"+"species_missing_ids.txt",'a') as species_handle:        
            species_handle.write(k+"\n")
        #-with write ends
    #--for loop ends
    
    return species_not_found
#-------------------->>>>>>>><<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>><<<<<<
    #-------------------------
    #
    #-------------------------

def parse_species(temp_dict,tempspecies,tempgenus):
    
    #called from another function
    genus_species={}  #hold species and their genus

    for key in temp_dict:
        tax_array=temp_dict[key]
        if tax_array[6]==tempspecies:
            if not tax_array[5] == tempgenus:
                #time to modify name of species
                tax_array[6]=str(tax_array[5])+'_'+tax_array[6]
                temp_dict[key]=tax_array
                
            #-if genus check
            
        #-if species check

    #--for loop ends for dict        
    #--------------------------------
    #
    #---------------------------------
    
def read_trained_fasta(temp_trainseq):

    #--this stores genus and other information from training FASTA file found
    
    count=0 #for genus level seqids
    total=0 #total seqd -ids
    
    seq_tax_ranks={} #return this after function ends
    
    for record in SeqIO.parse(temp_trainseq,"fasta"):
        total+=1
        
        id_array=re.split('\|',record.id)
        semi_count=(record.description).count(';')
        
        if semi_count==6: #proceed only if taxnomy rank found until genus else ditch it
            count+=1

            array_desc=re.split("Root",record.description)
            seq_id=re.split('\|',(array_desc[0].rstrip()))[1] #this is going to be used in dict later stages

            array_desc[1]=replace_special_chr(array_desc[1])
            array_desc[1]=array_desc[1].replace(' ','_')

            ranks_split=re.split(';',array_desc[1])
            
            index=1 #will start from second position in array. first one only stores ;
            seq_tax_ranks[seq_id]=[None]*7

            #--store phylum, class, order information.

            while index<7:

                seq_tax_ranks[seq_id][index-1]=ranks_split[index]
                index+=1
            #--while loop ends
            
        #----if ends for check on ; count

    #--for record loop ends for FASTA reading
    
    print "Total count of genus level classification from Trained",count

    #---------for loop of k seq_dict ends
    return seq_tax_ranks
    #------------------------------------
    #
    #------------------------------------

def print_species_missing(temptraining,temp_list,temp_out):
    #no spcies but taxonomy until genus present
    
    for record in SeqIO.parse(temptraining,"fasta"):
        
        #>AJ000684|S000004347
        
        record_id=re.split('\|',( (record.id).rstrip() )  )[1] #this is going to be used in dict later stages 

        if record_id in temp_list:
            with open(temp_out+"/"+"species_seq.fasta",'a') as m_handle:

                m_handle.write(">"+record_id+"\n")
                m_handle.write(str(record.seq)+"\n")
            #with ends
            
        #if check
            
    #for loop ends of record
    
    #-------------------------------------
    #
    #-------------------------------------

def find_missing_ids(new_fasta_file,training_fasta):

    #--find missing ids. Find printed seq ids and find total seq ids from training fasta
    #goal is to know the missing seq ids which don't have any species
    
    record_new=[] #new fasta file
    missing_seqids=[] #hold seq ids form training FASTA
    
    for new in SeqIO.parse(new_fasta_file, "fasta"):
        record_new.append(new.id)
    #--for loop ends

    print "New FASTA file has ",len(record_new)," sequences "
    
    training_fasta_info=list(SeqIO.parse(training_fasta,"fasta") )
    for x in training_fasta_info:
        record_id=re.split('\|',( (x.id).rstrip() )  )[1] #this is going to be used in dict later stages
        if not record_id in record_new:
            missing_seqids.append(record_id)
        #--
    #----

    print "Missing sequences from FASTA output are " , len(missing_seqids)
            
    #-----
    #----
    #-------------------------------
        
if __name__=="__main__":

    parser=argparse.ArgumentParser("description")
    parser.add_argument ('-t', '--trainingfasta', help='location for fasta file',required=True) # store input training FASTA file
    parser.add_argument ('-f', '--fasta_file', help='location for fasta file',required=True) # store input fasta file
    parser.add_argument ('-o', '--out_dir', help='output direct',required=True) # store output direc
                    
    args_dict = vars(parser.parse_args()) # make them dict..
    #create variables and store
    
    training_fasta_file=os.path.abspath(args_dict['trainingfasta'])
    output_dir=os.path.abspath(args_dict['out_dir'])
    rdp_dump_fasta=os.path.abspath(args_dict['fasta_file'])
    
    compare_fasta(rdp_dump_fasta,training_fasta_file,output_dir)
    species_dct=read_trained_fasta(training_fasta_file)

    training_seqids=list(species_dct.keys()) #store seqids that have taxonomy from training FASTA file

    #--we've genus names of around 1000 sequences from training fasta files
    
    seqid_species=print_fasta_file(rdp_dump_fasta,output_dir,species_dct)
    #fasta file is RDP database
    
    missing_species_list=get_taxonomy(rdp_dump_fasta,seqid_species,output_dir,training_seqids )
    #-fasta file sent is RDP database and not training FASTA

    #missing_species - list has list of IDs from training FASTA that don't have species from RDP's core. Genus lelve is present.  Will have to print their seqs from training seperately

    print_species_missing(training_fasta_file ,missing_species_list,output_dir)
    #print sequence id for which species are missing from RDP Dump - will

    record_trainnew=[] #store seqids from newly printed seqs

    find_missing_ids( output_dir+"/"+"species_seq.fasta",training_fasta_file )
    sys.exit()
    
    
    hmm=list(SeqIO.parse(os.path.abspath(args_dict['trainingfasta']),"fasta") )
    new_list=[]
    
    missing_seq=0

    for k in hmm:

        record_id=re.split('\|',( (k.id).rstrip() )  )[1] #this is going to be used in dict later stages
        if not record_id in record_trainnew:
            new_list.append(record_id)
        #
    #
    print len(new_list)

            
