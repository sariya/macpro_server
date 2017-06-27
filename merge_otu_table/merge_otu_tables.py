#!/usr/bin/env python

__date__="Sept 27 2016"
__location__="SEH 7th floor west offices, DC 20037"
__author__="Sanjeev Sariya"
__version__="0.2"
"""


Merge OTU tables from different runs for downstream analysis

OTU ids and sample names are stored in dictionary.. with value 0 to len of dict..
they are printed using dictionary value...

the 2d matrix created is based on index in otu-dict  and sample-dict.....

run name is needed by which merge file are created and  log files are written to current directory

It can take any number of otu files....
Run as:

python merge_otu_tables.py -o mini_april.txt,mini_aug_2.txt -dir ./

python ~/submit_git/merge_otu_table/merge_otu_tables.py -o ../../liupricelab_run_1/tabfile.tsv,../../liupricelab_run_2/new_tabfile.tsv -dir ./ -run genital
- it can allow tab file with path too now
-dir: directory is where all .txt input files are present

VSEARCH is used upstream 
OTU tables are created using python scripts from drive5 folder of robert edgar
 
"""
import os, argparse,re,sys
import logging

def get_column_count(array_otu_files, otu_dir):
    
    """
    column count is equal to the sample present.
    we'll read only the top row
    then store all samples in a dict where sample will be key and index will be value
    value starts from 0 ........
    """
    
    sample_name={}# -- create dictionary
    
    for i in array_otu_files:
        
        file_name=i
        #file_name=otu_dir+"/"+i

        with open(file_name) as handle:
            line = next(handle)#get only top line
            line=line.rstrip()
            
            array_split=line.split('\t')
            col_count=len(array_split)
        
            if col_count==0:
                print "Error with OTU table. No column present"
                sys.exit()
            #if loop check ends

            for i in array_split[1:]:
                    #[1:] because 0th position is OTuId
                if len(sample_name)==0:
                    #always set first index as 0.. keep in mind array
                    sample_name[i]=0
                else:
                    if not i in sample_name:
                        """
                        put sample as key and len as value
                        """
                        sample_name[i]=len(sample_name)
                    else:
                        #have to log it......
                        
                        logging.debug("already sample present " +i+ "  " + file_name )
                        
                    #if check ends not sample in dict
                #else for len of 0 for dict
            #for loop ends for array split
                    
            #with lop ends
    #loop over otu files ends
    
    return sample_name

    #-- function ends    
#-----------------###------------------------------->>

def get_row_counts(array_otu_files, otu_dir):
    
    temp_otus={}#hold all otu ids in a dictionary

    for i in array_otu_files:

        file_name=i
        #file_name=otu_dir+"/"+i
        with open(file_name) as handle:
            next(handle)#skip top row as it contains sample names
            
            for line in handle:
                line = line.rstrip()
                line_split=re.split('\t',line)
                #line_split[0] - otu name OTU_ blah.....
                
                if len(temp_otus)==0:
                    #if no element then .. have the value as 0 .. and then go ahead with 1, 2,....
                    temp_otus[line_split[0]]=0

                else: temp_otus[line_split[0]]=len(temp_otus)
                    #if check ends with len of dict and adding OTUs in the
                    #dictionary......
            
            #for loop over handle ends
        #with loop ends
    #---for loop ends for iterating over otu files
    
    return temp_otus
#------------------------------------------------
def create_matrix(row_count,col_count):
    
    import numpy
    return numpy.zeros((row_count,col_count))

#--------------------------##----------------->>

def check_dir(temp_dir):
    print ""
    
#----function ends--------------------------------->>

def check_otu_args(temp_list):
    
    if len(temp_list)!=1:
        logging.debug( "Space present in arguments")
        print "Check log file"
        sys.exit()
    #make sure you have only comma and no further crap
    
    files_name=re.split(',',temp_list[0])#store file names in an array
    comma_counts=temp_list[0].count(',') #get count of commas
    
    if comma_counts!=len(files_name)-1:
        
        logging.debug( "Mimatch in comma and input file names")
        print "Check log file"
        sys.exit(0)
    #-if ends for comma and array len check
    
    for i in range(len(files_name)):
        files_name[i]=os.path.abspath(files_name[i])
    #--make their path as absolute

    return files_name
#}function ends--------------------------------->>

def populate_matrix(temp_matrix,temp_otus,temp_samples,array_otu_files, otu_dir):
    
    for i in array_otu_files:
        
        sample_array=[]#store sample names in an array
        
        line_num=0
        file_name=i
        #file_name=otu_dir+"/"+i
        sample_array=[]
        """
        for each file sample_array will hold top line

        """
        
        with open(file_name) as handle:
            for line in handle:
                line=line.rstrip()
                line_split=re.split('\t',line)
                
                if line_num==0:
                        
                    sample_array=line_split[1:] #decalred for each file
                    
                #------only get sample names' row
                else:
                    
                    temp_otu_id=line_split[0]#store 0th position for otu id
                    
                    otu_counts_for_sample=line_split[1:]
                    """
                    store all counts of otus per sample
                    in another array for simplicity
                    """
                    
                    array_itr=0
                    
                    while array_itr<len(sample_array):
                        
                        col_index_matrix=temp_samples[sample_array[array_itr]] #get index of sample
                        row_index_matrix=temp_otus[temp_otu_id]#get index of OTU_id
                        
                        temp_matrix[row_index_matrix,col_index_matrix]=int(otu_counts_for_sample[array_itr])
                        
                        array_itr+=1
                        
                    #---while loop ends with array_itr
                line_num+=1
                
            #----for of handle -line ends
        #----with handle ends
    #---loping ends on otu files
#---------------------------------------------------------------->>>
def print_matrix(temp_matrix,temp_otus,temp_samples,run_name):

    temp_matrix=temp_matrix.astype(int)
    itr=0#iterate over otu dictionaru
    otu_string="OTUid"+'\t'

    while itr<len(temp_samples):
        for n in temp_samples:
            
            if temp_samples[n]==itr:
                otu_string=otu_string+n+'\t'
            #if for itr==value
            
        #--- for loop over 
        itr+=1
    #---while loop ends
    if os.path.exists(run_name+"_map.txt"):
        
        print run_name+"_map.txt"+ " File already present. Exiting!!!"
        sys.exit(0)
    #exit if .txt file alreay present .. this is to avoid files being over written
    
    
    with open(run_name+"_map.txt",'a') as write_handle:
        write_handle.write(otu_string+"\n")
    #with handle ends to write on curretn working directoy
    
        
    """
    iterate using keys....
    0, 1.. when the itr value matches value.. concatenate key value to the matrix string
    matrix string is the OTU_ID+all numbers...

    """
    
    itr=0
    while itr<len(temp_otus):
        matrix_str=""
        
        for n in temp_otus:
            if temp_otus[n]==itr:
                matrix_str=matrix_str+n+'\t'

        #n iterates over temp_otus dict... it is key......
        
                g=0 #iterate over row elements of matrix.....
                
                while g< len(temp_matrix[itr,:]):
                    matrix_str=matrix_str+str(temp_matrix[itr,g])+'\t'
                    g+=1
                #looping over matrix ro ends
            #---if value matches iterator....
        #------looping over temp_otus ends
        itr+=1
        
        with open(run_name+"_map.txt",'a') as write_handle:
            write_handle.write(matrix_str+"\n")
        #with handle ends for writing file to current working direcotry
    #while loop over its < dict leng ends
        
#---------------------------------------------------------------->>>
if __name__=="__main__":

    from time import strftime
    
    current_time=strftime("%Y%m%d%H%M%S")
    log_file_name="merge_otu_maps"+"_"+current_time+".log"
    
    logging.basicConfig(filename=log_file_name,format='%(asctime)s %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p',level=logging.DEBUG)
    
    parser=argparse.ArgumentParser("description")
    parser.add_argument('-o','--otu_table',nargs='+',required=True,type=str)
    
    """
    nargs to allow multiple arguments. Type = string  
    """
    
    parser.add_argument('-dir','--dir_otu_files',required=True)
    parser.add_argument('-run','--run_name',required=True) #run-name needed.. log files will be created using this.....
        
    """
    directory where all otu-tables are present
    """
    
    args_dict = vars(parser.parse_args()) # make them dict..
    otu_args= args_dict['otu_table']
    check_dir(os.path.abspath(args_dict['dir_otu_files']))
    otufiles_array=check_otu_args(otu_args)#verify if , and spaces or other stuff are present
    
    sample_name_dict=get_column_count(otufiles_array,os.path.abspath(args_dict['dir_otu_files']))

    """
    get sample names in a dictionary.. key sample name.. value index
    starting from 0
    """

    otu_ids_dict=get_row_counts(otufiles_array,os.path.abspath(args_dict['dir_otu_files']))
    """
    get otu name in a dict.. key otu name and value is index starting from 0
    """

    logging.debug("Row count " + str(len(otu_ids_dict))+ " column count " + str(len(sample_name_dict)) )
    
    two_dim_matrix=create_matrix(len(otu_ids_dict),len(sample_name_dict))
    
    """
    row and columns
    """
    
    populate_matrix(two_dim_matrix,otu_ids_dict,sample_name_dict,otufiles_array,os.path.abspath(args_dict['dir_otu_files']))
    
    """
    populate matrix using otu dict and sample dict..
    """
    print_matrix(two_dim_matrix,otu_ids_dict,sample_name_dict,args_dict['run_name'])
    logging.debug("Done with script " + args_dict['run_name'])
    print "Check log file "+ log_file_name

