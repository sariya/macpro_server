#
import re,sys,logging
from microbiome import *
from collections import OrderedDict,defaultdict

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
    
    #sampleNnames_list=[] #store sample names in this
    sampleNnames_dict=OrderedDict()  #create order dict for sample names-- 
    #store_microbes={} #this stores key as int value and microbe objects
    store_microbes=OrderedDict() #this stores key as int value and microbe objects

    with open(temp_rdpfile) as handle:

        for line in handle:
            
            temp_list=[""]*7 #set empty array of 7 elements 

            line=(line.rstrip()).replace('"',"")

            split_array=filter(None,re.split('\s+',line))  #split it by tab, remove/filter the ones which are blank/tab...
            sample_name=parse_seqid(split_array[0])

            pass_threshold=True # Flag to keep a check if threshold has passed or fail
            
            if not sample_name in sampleNnames_dict:
                #sampleNnames_list.append(sample_name)
                #sampleNnames_dict[len(sampleNnames_dict)+1]=sample_name
                sampleNnames_dict[sample_name]= len(sampleNnames_dict)
            #--if ends for storing sample name
    
            for i in range(len(split_array)):

                if split_array[i].lower() == "domain":
                    
                    if float(split_array[i+1])>=temp_conf:
                        temp_list[0]=split_array[i-1]
                    else:
                        temp_list[0]=split_array[i-1]+"<"+str(temp_conf)
                        break

                        
                if split_array[i].lower() == "phylum":

                    if float(split_array[i+1])>=temp_conf:            
                        temp_list[1]=split_array[i-1]
                    else:
                        temp_list[1]=split_array[i-1]+"<"+str(temp_conf)
                        break
                        
                        
                if split_array[i].lower() == "class":
                    
                    if float(split_array[i+1])>=temp_conf: temp_list[2]=split_array[i-1]
                    else:
                        temp_list[2]=split_array[i-1]+"<"+str(temp_conf)
                        break
                        
                if split_array[i].lower() == "order":

                    if float(split_array[i+1])>=temp_conf: temp_list[3]=split_array[i-1]
                    else:
                        temp_list[3]=split_array[i-1]+"<"+str(temp_conf)
                        break
                        
                if split_array[i].lower() == "family":

                    if float(split_array[i+1])>=temp_conf: temp_list[4]=split_array[i-1]
                    else:
                        temp_list[4]=split_array[i-1]+"<"+str(temp_conf)
                        break
                    
                if split_array[i].lower() == "genus":
                    
                    if float(split_array[i+1])>=temp_conf: temp_list[5]=split_array[i-1]
                    else:
                        temp_list[5]=split_array[i-1]+"<"+str(temp_conf)
                        break
                    
                if split_array[i].lower() == "species":
                    
                    if float(split_array[i+1])>=temp_conf: temp_list[6]=split_array[i-1]
                    else:
                        temp_list[6]=split_array[i-1]+"<"+str(temp_conf)
                        break

            #--for iteration ends-------
            
            key_microbe_dict=check_microbe(temp_list,store_microbes) # found or not taxonomy
            
            if not key_microbe_dict  == -1:
                store_microbes[key_microbe_dict].update_microbe_sample(sample_name)
                
            else:
                microbe_object=Microbiome() #create new object 
                microbe_object.set_attributes(temp_list,sample_name) #set attributes 
                
                store_microbes[len(store_microbes)]=microbe_object
            #---if check ends for taxonomy. Found -1 or not 
        #--for loop ends for line
    #-with loop ends

    logging.debug("Total samples found through taxonomy file %s" %(len(sampleNnames_dict)))
    logging.debug("Confidence used whilst parsing RDP taxonomy file %s" %(temp_conf))
    logging.debug("Unique taxonomy stored %s" %(len(store_microbes)))
    logging.debug("Total taxnmy classification seqs from RDP are %s" %(count_taxonomy(store_microbes)))
    return (sampleNnames_dict,store_microbes)
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

def create_matrx(row_count,col_count):
    
    import numpy    
    return numpy.zeros((row_count,col_count)) #create 2D matrix

    #-----------------------------------
    #Date June 16th 2017
    #-----------------------------------
    
def populate_matrx(temp_matrx,_temp_taxnmy_dict,_temp_sample_dict):

    import numpy 
    """
    Populate counts of taxnmy found. We're using ordered dict with sample names and taxnmy. index and ket value are
    utilized to access row and column indices. 
    """
    for key, val in _temp_taxnmy_dict.iteritems():
        matrx_colmn_index=key 
        
        for _sampleName,_sample_count in (val.sample_counts).iteritems():
            """
            Iterate through dict microbiome objt has. 
            """
            matrx_row_index=_temp_sample_dict.keys().index(_sampleName) # get index of sample stored in _temp_sample_dict
            
            """
            Get index of sample name from its dictionary. After extracting index of sample name, store it
            Stored index of sample name is going to be row number that's to be updated in matrix
            Column would be key for the iterating taxonomy. Key starts from 0...goes until unique taxonomy
            """
            try:
                temp_matrx[matrx_row_index][matrx_colmn_index]+=_sample_count
            
            except Exception as e:
                print "Having issues with updating mtrx "
                sys.exit()
            #--try ends
        #--For loop ends for dict in taxonomy object 
    #--for loop for taxnmy dictnry
    logging.debug("Doing sum of all elements of matrix." )
    logging.debug("Sum of all elements that should be same as RDP seqs count %s" %(numpy.sum(temp_matrx)))

    
    #---------------------------------
    #Date June 16th 2017
    #--------------------------------

def print_populated_matrx(temp_matrx,_temp_taxnmy_dict,_temp_sample_dict,run_name,temp_conf,type_clsfctn):

    import numpy
    """
    First get tab delimited headers of taxonomy
    temp_matrx - contains counts
    _temp_txnmy_dict - clasfctn dictnry
    _temp_sample_dict contains sample names
    run_name - name provided by user
    type_clsfctn can be genus or species

    """
    line_domain=line_phylum="\t"
    line_class=line_order="\t"
    line_family=line_genus="\t"
    line_species="\t"
    
    for key, val in _temp_taxnmy_dict.iteritems():

        if not val.domain: line_domain+=""+"\t"
        else: line_domain+=val.domain+"\t"

        if not val.phylum: line_phylum+=""+"\t"
        else: line_phylum+=val.phylum+"\t"

        if not val.class_m: line_class+=""+"\t"
        else: line_class+=val.class_m+"\t"

        if not val.order: line_order+=""+"\t"
        else: line_order+=val.order+"\t"

        if not val.family: line_family+=""+"\t"
        else: line_family+=val.family+"\t"

        if not val.genus: line_genus+=""+"\t"
        else: line_genus+=val.genus+"\t"

        if not val.species: line_species+=""+"\t"
        else: line_species+=val.species+"\t"
        
    ##--For loop ends to create header-->>

    col_counts=numpy.shape(temp_matrx)[1] # get colmn counts 
    with open(run_name+"_"+str(temp_conf)+"_"+type_clsfctn+'.tsv', 'a') as out_file:
        
        out_file.write(line_domain+"\n"+line_phylum+"\n"+line_class+"\n"+line_order+"\n")
        out_file.write(line_family+"\n"+line_genus + "\n"+line_species+"\n")
    
        for sampleName, index_sampleName in _temp_sample_dict.iteritems():
            matrx_line="" #concatenate counts to this string
            
            matrx_line+=sampleName+"\t"
            
            #index_sampleName is row index. 
            for i in range(col_counts): matrx_line+=str(temp_matrx[index_sampleName][i])+"\t"

            out_file.write(matrx_line+"\n")
        
        #----iterate over row.
    #--with handle ends to write output
    #print _temp_sample_dict
    #------------------------
    #Date June 16th 2017
    #------------------------
