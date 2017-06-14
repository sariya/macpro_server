#
import re,sys

def check_microbe(microb_list,microb_object):
    print ""

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
def read_rdp_clsfctn(temp_rdpfile):
    sampleNnames_list=[] #store sample names in this
    
    with open(temp_rdpfile) as handle:
        for line in handle:
            line=(line.rstrip()).replace('"',"")
            split_array=filter(None,re.split('\s+',line))  #split it by tab, remove/filter the ones which are blank/tab...
            sample_name=parse_seqid(split_array[0])
            
            if not sample_name in sampleNnames_list:
                sampleNnames_list.append(sample_name)
            #--if ends for storing sample name
            print split_array
            
            for i in range(len(split_array[4:])):
                print split_array[4:][i]
                if split_array[i].lower() == "domain":
                    print ""
                if split_array[i].lower() == "phylum":
                    print ""
                if split_array[i].lower() == "class":
                    print ""
                if split_array[i].lower() == "order":
                    print ""
                if split_array[i].lower() == "family":
                    print ""
                if split_array[i].lower() == "genus":
                    print ""
                if split_array[i].lower() == "species":
                    print ""
            #--for iteration ends-------

                
            sys.exit()


        #--for loop ends
    #-with loop ends
    print "Total sample names in data ",len(sampleNnames_list)
    #----------------------------------
    #Date Added June 14 2017
    #---------------------------------
    
