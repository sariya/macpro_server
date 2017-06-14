#
import re

def parse_seqid(temp_string):

    """
    This function is called from read_rdp_clsfctn
    returns sample name
    """
    temp_string=temp_string.replace("_DNA_end_none","") #replace end string with nothing 
    start_index=temp_string.index("strt_")
    return temp_string[start_index+len("strt_"):] #return same names

    #-----------------------------
    #
    #------------------------------
def read_rdp_clsfctn(temp_rdpfile):
    sampleNnames_list=[] #store sample names in this
    
    with open(temp_rdpfile) as handle:
        for line in handle:
            line=line.rstrip()
            split_array=re.split('\s+',line)
            sample_name=parse_seqid(split_array[0])
            
            if not sample_name in sampleNnames_list:
                sampleNnames_list.append(sample_name)
            #--if ends for storing sample name

        #--for loop ends
    #-with loop ends
    print "Total sample names in data ",len(sampleNnames_list)
    #-----------
    #Date Added June 14 2017
    #-----------
    
