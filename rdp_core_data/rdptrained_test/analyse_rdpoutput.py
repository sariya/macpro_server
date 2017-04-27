#!/usr/bin/env python

__date__="April 25 2017"
__location__="SEH 7th Floor"
__author__="Sanjeev Sariya"


global genera_int
genera_int=["Prevotella","Porphyromonas","Dialister","Mobiluncus","Negativicoccus","Peptoniphilus","Finegoldia","Anaerococcus","Peptostreptococcus","Murdochiella"] #interested

global genus_misclassified
genus_misclassified=0
global species_misclassified
species_misclassified=0

long_description="""

Take classification file from trained RDP and 
compare it with input tab delimited taxonomy file used to create lineage
 

"""
import argparse, os, re,sys

def store_taxonomy(temp_tabtaxonomy):
    
    """
    Read tab delimited taxonomy file 
    Store it in dict and return it
    """
    dict_seqid={}
    with open(temp_tabtaxonomy,'r') as read_handle:
        
        next(read_handle) #skip forst header line
        for line in read_handle:
            line = line.rstrip()
            tax_array=re.split('\s+',line)
            dict_seqid[tax_array[0]]=tax_array[1:]
            
        #--for ends
    #-with ends
    return dict_seqid
    #------------------------
    #
    #-----------
def check_assgnmnt(cls_taxonomy,tab_taxonomy,tmp_genus_index):
    """
    Function called from compare classification
    Called after confirming genus is present in line 
    """

    if tab_taxonomy[5] != cls_taxonomy[tmp_genus_index-1]:
        globals()['genus_misclassified']+=1
        print "We are having issues with genus classification "
        print cls_taxonomy,tab_taxonomy
    else:
        if tab_taxonomy[6] != cls_taxonomy[tmp_genus_index+2]:
            if cls_taxonomy[tmp_genus_index-1] in genera_int :
                globals()['species_misclassified']+=1
                #print "We are having issues with species classification "
                print "Assigned ", cls_taxonomy[tmp_genus_index+2],"Actual ",tab_taxonomy[6],cls_taxonomy[0]
    

    #------------------------------------------
    #
    #-------------------------------------------
def compare_clasfctn(tax_dict,temp_classfctn):

    cnt_genus=0 #count for genus less than 80%
    cnt_misng_genus=0 #count of missing genus assignment
    
    """
    Take dictionary of tab delimited taxonomy and classfiction file from trained RDP
    """

    with open (temp_classfctn,'r') as cls_handle:
        for line in cls_handle:
            line = line.rstrip()
            if  "genus" in line:
                
                split_array=re.split('\s+',line)
                seq_id=split_array[0]
                genus_index=split_array.index("genus") #get index of genus
                genus_conf=float(split_array[genus_index+1]) #get confidence of genus assignment
                if genus_conf < 0.8:
                    cnt_genus+=1
                    print "Not good assignment for genus level at 80%",line
                #--if ends
                else:
                    #pass
                    check_assgnmnt(split_array,tax_dict[seq_id],genus_index)
                #--else ends
            else:
                cnt_misng_genus+=1
                print "Genus is out of place misclassified",line
        #--for loop ends
    #with ends
    
    print "Missing genus count ",cnt_misng_genus
    print "Less than 80% assignment ",cnt_genus
    print "Total classification ",len(tax_dict)

    #-----------------------------
    #
    #---------------------------
if __name__=="__main__":

    parser=argparse.ArgumentParser("description")
    parser.add_argument ('-c', '--class', help='location for output by RDP',required=True) # store input classification file
    parser.add_argument ('-o', '--out', help='Output directory',required=True) # store output destination
    parser.add_argument ('-t', '--taxonomy', help='TSV taxonomy file',required=True) # store input TSV tab file
    args_dict = vars(parser.parse_args()) # make them dict..
    
    classfctn_file=os.path.abspath(args_dict['class']) #classfication file
    out_dir=os.path.abspath(args_dict['out']) #output directory
    tab_tax_file=os.path.abspath(args_dict['taxonomy']) #tab delimited taxonomy file
    
    tab_tax_dict=store_taxonomy(tab_tax_file)
    
    compare_clasfctn(tab_tax_dict,classfctn_file)
    print "Genus misclassified ",genus_misclassified
    print "Speceis misclass ",species_misclassified
