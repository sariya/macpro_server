#!/usr/bin/env python

from Bio import SeqIO
import os, argparse,sys,re

__date__="Sept 7 2016"
__location__="SEH 7th floor west offices, DC 20037"
__author__="Sanjeev Sariya"


"""

take input fasta file which has been fiiltered from all N,W,Y
Take probe match output file 
Get forward and reverse cordinates for each sequence
trim the respective sequence and append it it an output file

"""
def get_seq_ids(fasta_file):
    
    """
    Get only seq ids and return in the list

    """
    record_dict = SeqIO.to_dict(SeqIO.parse(fasta_file, "fasta"))
    ids_list=list(record_dict)

    return ids_list
    #--------------->
def get_cordinates(p_file,seq_list):    

    coord_seq_forward={}#seq and forward coordinates
    coord_seq_reverse={}#seq and reverse coordinates
    coord_list=[]#array to hold reverse and forward coord dict
    
    
    """

    create 2 dicts which will hold forward and reverse primer's location
    append forward and reverse primer location to values in doct

    """
    with open(p_file) as p_handle:
        for line in p_handle:
            line=line.rstrip()
            array=re.split('\t',line)#split probe output file by tab

            #array[3] - is reverse/forward
            #array[0] is seq id
            if array[0] in seq_list:
                
                if array[3]=="reverse":

                    if not array[0] in coord_seq_reverse:
                        coord_seq_reverse[array[0]]=int(array[4])
                    else:
                        print "Some issue with ", array[0], " reverse"
                        sys.exit(0)
                        
                #--reverse coordinate ends
                
                if array[3]=="forward":
                    
                    if not array[0] in coord_seq_forward:
                        coord_seq_forward[array[0]]=int(array[4])
                    else:
                        print "Some issue with ", array[0], " forward"
                        sys.exit(0)
                #--forward coordinates ends
                
            #--if seq exists in fasta file's list

        #-- for loop ends
        
    #with loop ends
    
    if len(coord_seq_reverse)!=len(coord_seq_forward):
        print "Coordinates misisng in one of the dicts"
        sys.exit()

    #--if ends for lengths of rev and for coord dict
    coord_list.append(coord_seq_forward)#append to the list
    coord_list.append(coord_seq_reverse)#second element is reverse coord dict
    return coord_list

#-- function ends---------------------------------------

def trim_seq(temp_coord_list,temp_fasta):

    temp_for_coord=temp_coord_list[0]
    temp_rev_coord=temp_coord_list[1]#second item of list is reverse cordinates

    for record in SeqIO.parse(temp_fasta,"fasta"):
        
        f_coord=temp_for_coord[record.id] #get respective forward coord
        r_coord=temp_rev_coord[record.id] #get respective reverse coord
        
        if r_coord<f_coord:
            #if reverse coordinate is smaller than forward.. exit
            print "Have some issue with coordinates"
            sys.exit()
        #--if check ends
        
        with open("trimmed_seq.fasta",'a') as write_h:
            write_h.write(">"+record.description+"\n")
            write_h.write(str(record.seq[f_coord-1:r_coord])+"\n")

        #--with handle ends to write
        
    #---for loop ends for fasta file

#--function ends

if __name__=="__main__":
    
    parser=argparse.ArgumentParser("description")
    parser.add_argument ('-fa', '--fasta_file', help='location for fasta file',required=True) # store input fasta file
    parser.add_argument ('-pr', '--probe_file', help='location for probe output file',required=True) # store input fasta file
    args_dict = vars(parser.parse_args()) # make them dict..
    
    seq_ids_list=get_seq_ids(os.path.abspath(args_dict['fasta_file']))
    list_coord=get_cordinates(os.path.abspath(args_dict['probe_file']),seq_ids_list)

    j="hello-sanjeev"
    print j,j[2:8]
    trim_seq(list_coord,os.path.abspath(args_dict['fasta_file']))
