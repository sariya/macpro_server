#
import re,sys,logging
from microbiome import *

def check_microbe(taxonomy_list,microbe_dict):
    """
    Check if microbe taxonomy alread exists in the dictionary
    If not then return -1
    Else, return its key (that's an integer value)
    """
    
    found=-1 #by default not found microbe taxonomy in the dictionary

    for key,val in microbe_dict.items():
        if (taxonomy_list[0] == val.domain and
            taxonomy_list[1] == val.phylum and 
            taxonomy_list[2] == val.class_m and
            taxonomy_list[3] == val.order and
            taxonomy_list[4] == val.family and
            taxonomy_list[5] == val.genus and
            taxonomy_list[6] == val.species ):
            return key #return integer key number of the microbe config found
                
    #---for loop ends-----
    return found
    #------------------------
    #Added June 14 2017
    #------------------------
    
def parse_seqid(temp_string):

    """
    This function is called from read_rdp_clsfctn
    returns sample name
    """
    temp_string=temp_string.replace("_DNA_end_none","") #replace end string with nothing 
    start_index=temp_string.index("strt_")
    return temp_string[start_index+len("strt_"):] #return same names

    #-----------------------------
    #Added June 14 2017
    #------------------------------
def read_rdp_taxnmy(temp_rdpfile,temp_conf):
    
    sampleNnames_list=[] #store sample names in this
    store_microbes={} #this stores key as int value and microbe objects
    with open(temp_rdpfile) as handle:

        for line in handle:
            
            temp_list=[""]*7 #set empty array of 7 elements 

            line=(line.rstrip()).replace('"',"")

            split_array=filter(None,re.split('\s+',line))  #split it by tab, remove/filter the ones which are blank/tab...
            sample_name=parse_seqid(split_array[0])

            #pass_threshold=True # Flag to keep a check if threshold has passed or fail
            
            if not sample_name in sampleNnames_list:
                sampleNnames_list.append(sample_name)
            #--if ends for storing sample name
    
            for i in range(len(split_array)):

                if split_array[i].lower() == "domain":
                    
                #    if pass_threshold:
                    if float(split_array[i+1])>=temp_conf:
                        temp_list[0]=split_array[i-1]
                    else:
                        temp_list[0]=split_array[i-1]+"<"+str(temp_conf)
                        #pass_threshold=False
                        break
                        
                if split_array[i].lower() == "phylum":
                 #   if pass_threshold:
                    if float(split_array[i+1])>=temp_conf:            
                        temp_list[1]=split_array[i-1]
                    else:
                        temp_list[1]=split_array[i-1]+"<"+str(temp_conf)
                        #pass_threshold=False
                        break
                        
                if split_array[i].lower() == "class":
                  #  if pass_threshold:
                    if float(split_array[i+1])>=temp_conf:
                        temp_list[2]=split_array[i-1]
                        
                    else:
                        temp_list[2]=split_array[i-1]+"<"+str(temp_conf)
                        #pass_threshold=False
                        break
                        
                if split_array[i].lower() == "order":
                   # if pass_threshold:

                    if float(split_array[i+1])>=temp_conf:
                        temp_list[3]=split_array[i-1]
                    else:
                        temp_list[3]=split_array[i-1]+"<"+str(temp_conf)
                        #pass_threshold=False
                        break
                        
                if split_array[i].lower() == "family":
                    #if pass_threshold:
                    if float(split_array[i+1])>=temp_conf:
                        temp_list[4]=split_array[i-1]
                    else:
                        temp_list[4]=split_array[i-1]+"<"+str(temp_conf)
                        #pass_threshold=False
                        break
                        
                if split_array[i].lower() == "genus":
                    #if pass_threshold:
                    if float(split_array[i+1])>=temp_conf:
                        temp_list[5]=split_array[i-1]

                    else:
                        temp_list[5]=split_array[i-1]+"<"+str(temp_conf)
                        #pass_threshold=False
                        break
                        
                if split_array[i].lower() == "species":
                    #if pass_threshold:
                    if float(split_array[i+1])>=temp_conf:
                        temp_list[6]=split_array[i-1]

                    else:
                        temp_list[6]=split_array[i-1]+"<"+str(temp_conf)
                        #pass_threshold=False
                        break
            #--for iteration ends-------
            
            key_microbe_dict=check_microbe(temp_list,store_microbes) # found or not taxonomy
            
            if not key_microbe_dict  == -1:
                store_microbes[key_microbe_dict].update_microbe_sample(sample_name)
                
            else:
                microbe_object=Microbiome() #create new object 
                microbe_object.set_attributes(temp_list,sample_name) #set attributes 
                
                store_microbes[len(store_microbes)+1]=microbe_object
            #---if check ends for taxonomy. Found -1 or not 
        #--for loop ends for line
    #-with loop ends

    #print "Total sample names in data ",len(sampleNnames_list)
    #print "Confidence is ",temp_conf
    #print "Length of microbes stored ",len(store_microbes)
    #print "Total taxonomy classification are ",count_taxonomy(store_microbes)
    logging.debug("Total samples found through taxonomy file %s" %(len(sampleNnames_list)))
    logging.debug("Confidence used whilst parsing RDP taxonomy file %s" %(temp_conf))
    logging.debug("Length of microbes stored %s" %(len(store_microbes)))
    logging.debug("Total taxnmy classification seqs from RDP are %s" %(count_taxonomy(store_microbes)))
                  
    #----------------------------------
    #Added on Date June 14 2017
    #---------------------------------
    
def count_taxonomy(temp_dict):
    
    """
    Add count of samples in each taxonomy. This aims to get total classification. 
    If RDP has initial input as 100, then this should give 100 at the end
    """
    total_taxonomy=0
    for k in temp_dict: total_taxonomy+=temp_dict[k].add_sample_count()

    return total_taxonomy
    #-----------------------------
    #Added on Date June 15th 2017
    #------------------------------
    
