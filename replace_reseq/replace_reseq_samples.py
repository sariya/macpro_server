#!/usr/bin/env python

__date__="June 27 2017"
__location__="SEH 7th Floor"
__author__="Sanjeev Sariya"

long_description="""
- take tab delimited text file that has two coloumns. 
Columns 1st - has sample names that are to be replaced with the one in 2nd column
- Take otu table made after vsearch and robert egdar script

- We have to use this temprary script for sample names mis-named on wet lab side. 
- We'd - removed in samples that were re-sequenced. Processed and found there appropriate names via excel and made tab delimited
file

"""
import sys,os, argparse,re

def store_replacmnt(temp_textFile):
    """
    temp_textFile has two columns
    """
    replcmnt_dict={} #store key and value key is to be replace, value to be replaced by
    
    with open(temp_textFile)as temp_textFile:
        for line in temp_textFile:
            line = line.rstrip() 
            arry_splt= re.split('\s+',line) #array split by space 
            replcmnt_dict[arry_splt[0]]=arry_splt[1]
        #-for loop ends
    #-with loop ends
    print "we have ", len(replcmnt_dict), "samples to be replaced "
    
    return replcmnt_dict
    #---------------------
    #
    #----------------------

def process_sample_replcmnt(temp_dict,temp_tabFile):

    changes_made=0
    """
    temp_dict from store_replcmnt functn
    temp_tabFile has otu from vsearch and roEdga scripts 
    return new header after fnction ends 
    """
    
    new_header="" #return with replaced sample names
    
    with open(temp_tabFile) as otu_handle:
        
        sample_header=next(otu_handle) #store only the header 
        header_split=re.split('\s+',sample_header.rstrip())

        for sample in header_split:

            if sample in temp_dict:
                new_header=new_header+"\t"+temp_dict[sample]
                changes_made+=1
            else: new_header=new_header+"\t"+sample

            #-if check ends for temp_dict presence
        #--for loop ends
    #--with loop ends
    print "Total changes made ",changes_made
    return new_header.lstrip()
    #-----------------------
    #
    #-------------------------
def print_new_tab(temp_header,temp_tabFile,temp_out):

    new_file=temp_out+"/"+"new_tabfile.tsv"
    with open (new_file,'a') as tsv_handle:
        tsv_handle.write(temp_header+"\n")

        with open(temp_tabFile) as tab_file_handle:
            next(tab_file_handle) #store only the header
            for line in tab_file_handle:
                tsv_handle.write(line)
            #--for loop ends for tab counts
        #--with ends to read OTU tab  file
    #--with handle ends for writing new OTU table with new headers

        
    #------------------------------------
    #
    #------------------------------------
if __name__=="__main__":

    parser=argparse.ArgumentParser("description")
    parser.add_argument ('-o', '--out', help='location for output folder',required=True) # store output directry
    parser.add_argument ('-t', '--tab', help='TAB otu table',required=True) # store OTU table
    parser.add_argument ('-r', '--repl', help='location for text file that has two columns for replacement',required=True) # store input columnar text file 
    args_dict = vars(parser.parse_args()) # make them dict..
    dict_replamnt=store_replacmnt(args_dict['repl'])
    new_header=process_sample_replcmnt(dict_replamnt,args_dict['tab'])
    print_new_tab(new_header,args_dict['tab'],args_dict['out'])
    print "Check for new_tabfile.tsv file in output directory"
    print "<<--Done-->>"
