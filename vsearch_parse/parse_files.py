__author__ = "Sanjeev Sariya"
__date__= "08 Feb 2016"
__maintainer__= "Sanjeev Sariya"
__status__= "development"

from collections import OrderedDict,defaultdict
from microbiome import * 
from rep_seq import *
import logging,re
from pprint import pprint
import sys

def create_sample_list(_otu_array):
#{
    """
    Function returns an rep-seq object which has rep seq name, 
    and
    a dict which contains sample name, and its count
    """

    sample_count=OrderedDict() # used for Rep-seq object

    for x in _otu_array[1:]: #_otu_array[0] - is rep seq

        hold_position=[]# store all positions of _ .. added on 11 March
        # sample names can have _ in them...
        #_under_score=x.find("_")

        for pos,ch in enumerate(x):
            #http://stackoverflow.com/questions/2294493/how-to-get-the-position-of-a-character-in-python
            if "_" == ch:
                hold_position.append(pos)
        #-- for ends . hold all _ indices
        
        if len(hold_position)>0:

            _sample=x[:max(hold_position)] #parse sample name until last _ index
            
            if _sample in sample_count:
                sample_count[_sample]+=1
            else:
                sample_count[_sample]=1
            #-- ends for dict keeping
            
        else:
            logging.debug("_ missing from %s" %(x))
            logging.debug("Exiting! Look at %s for problem" %(x))
            sys.exit()
        # if underscore found

    #} For loop ends iterating over all Sample_1_34

    if len(sample_count) ==0:
        logging.debug("There are no sample is rep seq %s" %(_otu_array[0]))
        logging.debug("Exiting due to issue in dictionary !")
        sys.exit()
        
    rep_seq_object=Rep_seq(_otu_array[0],sample_count)    
    return rep_seq_object #return object

    #------------------------------------------
    #} function ends 
    #------------------------------------------------
def get_sample_array(map_file):
    """
    Added on 22 sept 2016

    return dictionary of sample names and their location
    """
    #first line is the otu-id and sample names
    
    sample_names_index={}#0 - otu-id, 1-s1, 2-s2.. so and so forth
    
    index=0 #to hold position
    with open(map_file, 'r') as f:
        first_line = f.readline().rstrip()#get only first line- headers
    array_names=re.split('\s+',first_line)#store in array

    for i in array_names:
        sample_names_index[index]=i#store by index
        index+=1
    #for loop ends
    return sample_names_index

    #------------------------------------------
    #} function ends 
    #------------------------------------------------
def create_sample_list2(t_array,sample_index):
    """
    t_array is line split from map file
    """

    index=1 #don't want to start from 0 as 0 is for otu-name/id
    
    sample_count=OrderedDict() # used for Rep-seq object
    otu=t_array[0]
    
    for x in t_array[1:]: #_otu_array[0] - is rep seq

        x=int(x)#convert into integer -- 
        temp_sample_name=sample_index[index]
        sample_count[temp_sample_name]=x
        index+=1
    #--for loop ends

    rep_seq_object=Rep_seq(otu,sample_count)

    return rep_seq_object

    #------------------------------------------
    #} function ends 
    #------------------------------------------------
def read_otu_map_file(_map_file):
#function begins
    
    """
    Read Rep Seq and sample Map file 
    Function creates a list of objects after parsing otu map file
 
    """
    #read MAP file #rep_sample_list=[] #hold objects
    
    rep_sample_list={} #hold objects
    sample_names_index=get_sample_array(_map_file)
    
    with open(_map_file) as _map_handle:
        next(_map_handle)#skip first line as vsearch
        #has headers of sample names and otu
        
        for line in _map_handle:
            otu_array=re.split('\s+',line.rstrip())
            rep_seq_obj=create_sample_list2(otu_array,sample_names_index)
            
            rep_sample_list[otu_array[0]]=rep_seq_obj #rep_seq_obj=create_sample_list(otu_array)
            
        #iteration ends of file
    #---with loop ends

    if len(rep_sample_list) ==0:
        logging.debug("Empty list for OTU map and rep seq")
        
    logging.debug("Rep sequence, and sample list file has been parsed")
    return rep_sample_list

    #------------------------------------------------
    #} function ends 
    #------------------------------------------------
def check_microbe(microb_list,microb_object):
    
#{ Function begins
    """
    This function checks if similar microboe confirguration is already present in the dict
    If present Then returns True, else False
    """
    
    present=False
    if len(microb_list) > 0:
        for key in microb_list:
            temp_object=microb_list[key]

            if temp_object.class_m==microb_object.class_m and temp_object.domain==microb_object.domain:
                if temp_object.phylum==microb_object.phylum and temp_object.order==microb_object.order:
                     if temp_object.family==microb_object.family and temp_object.genus==microb_object.genus:
                         if temp_object.species==microb_object.species:
                             logging.debug("microbiome exists like this " + str(temp_object.rep_seq) + str(microb_object.rep_seq))
                             (temp_object.rep_seq).append((microb_object.rep_seq)[0]) #add the firt element of the list
                             return True
                         #-if species name same
                #if phylum and order check
            #if domain and class name check
                        

    return present

    #------------------------------------------------
    #} function ends 
    #------------------------------------------------

def replace_space(temp_word):
    #added on Oct 6 2016
    replaced_word=temp_word.replace(" ","_")
    
    return replaced_word
    #---------------------------------------------
    #function ends--->>
    #---------------------------------------------
def read_rdp_file(temp_rdp_file,conf_thresh):
#{
    """
    Function to read RDP file, and do further process
    """
    diversity_microbe={}
    """
    Have microbe object in dictionary way
    1 , microb object
    2, object ....
    """
    
    counter=0
    """
    This counter is key for microbiome objects that are stored in dictionary
    """
    
    with open(temp_rdp_file) as handle_rdp:
        for line in handle_rdp:
            
            pass_threshold=True # Flag to keep a check if threshold has passed or fail
            line=(line.rstrip()).replace('"',"")
            line_array=filter(None,re.split('\t',line) ) #split it by tab, remove/filter the ones which are blank/tab...
            microb_obj=Microbiome() 
            """
            Microbe object has: rep_seq null list, domain, phylum, class_m, sub_class
            order, sub_order, family, sub_family, genus and species. Everything is set to NULL initially
            """
            (microb_obj.rep_seq).append(line_array[0]) # store rep seq - can be int, can be string.. let's keep it string by default every where
            
            """
            We are not keeping suborder, sub family and sub class
            """
            
            for i in range(len(line_array)):

                if line_array[i].lower() == "domain":
                    if pass_threshold:
                        #if threshold is still True
                        
                        if float(line_array[i+1]) >= conf_thresh:
                            #added >= on Oct 10 2016
                            
                            domain_str=replace_space(line_array[i-1])#replace space
                            microb_obj.domain=domain_str
                        else:
                            
                            domain_str=replace_space(line_array[i-1])#replace space if present
                            microb_obj.domain=domain_str+"<"+str(conf_thresh) # Fermicutes<0.80
                            pass_threshold=False
                #if loop for domain ends
                            
                if line_array[i].lower() == "phylum":
                    if pass_threshold:
                        if float(line_array[i+1])>= conf_thresh:
                            phylum_str=replace_space(line_array[i-1])#replace space
                            microb_obj.phylum=phylum_str
                        else:
                            phylum_str=replace_space(line_array[i-1])#replace space
                            microb_obj.phylum=phylum_str+"<"+str(conf_thresh)  #Fermicutes<0.80              
                            pass_threshold=False
                #if loop ends for phylum
                                                       
                if line_array[i].lower() == "class":
                    if pass_threshold:
                        #if threshold is still True 
                        if float(line_array[i+1]) >=conf_thresh:
                            class_str=replace_space(line_array[i-1])#replace space if present
                            microb_obj.class_m=class_str
                        else:
                            class_str=replace_space(line_array[i-1])#replace space if prsent
                            microb_obj.class_m=class_str+"<"+str(conf_thresh)#Fermicutes<0.80
                            pass_threshold=False
                #if loop for class ends

                if line_array[i].lower() == "order":
                    if pass_threshold:
                        #if threshold is still True
                        if float(line_array[i+1])>= conf_thresh:
                            order_str=replace_space(line_array[i-1])#replace space if prseent
                            microb_obj.order=order_str
                        else:
                            order_str=replace_space(line_array[i-1])#replace space if present
                            microb_obj.order=order_str+"<"+str(conf_thresh)#Fermicutes<0.80
                            pass_threshold=False
                #if loop for order ends
                            
                if line_array[i].lower() == "family":
                    if pass_threshold:
                        #if threshold is still True 
                        if float(line_array[i+1])>= conf_thresh:
                            family_str=replace_space(line_array[i-1])#replace space
                            microb_obj.family=family_str 
                        else:
                            family_str=replace_space(line_array[i-1])#replace space
                            microb_obj.family=family_str+"<"+str(conf_thresh) #Fermicutes<0.80
                            pass_threshold=False
                #if loop for family ends
                                                        
                if line_array[i].lower() == "genus":
                    if pass_threshold:
                        if float(line_array[i+1])>=conf_thresh:
                            genus_str=replace_space(line_array[i-1])#replace space
                            microb_obj.genus=genus_str
                            
                        else:
                            genus_str=replace_space(line_array[i-1])#replace space
                            microb_obj.genus=genus_str+"<"+str(conf_thresh) #Fermicutes<0.80
                            pass_threshold=False
                #if loop for genus ends
                            
                if line_array[i].lower() == "species":
                    if pass_threshold:
                        #if threshold is still True 
                        if float(line_array[i+1]) >= conf_thresh:
                            species_str=replace_space(line_array[i-1])#replace space
                            microb_obj.species=species_str 
                        else:
                            species_str=replace_space(line_array[i-1])#replace space
                            microb_obj.species=species_str+"<"+str(conf_thresh) #Fermicutes<0.80
                            pass_threshold=False
                    #if loop for threshold ends
                #if loop for species
                
            # -- for loop ends
            #pprint(vars(microb_obj)) #print everything
            
            if(check_microbe(diversity_microbe,microb_obj)== False):
                """
                check_microbe is function which check if exact taxonomy is present already in the 
                dictionary
                """
                
                diversity_microbe[counter]=microb_obj

                """
                Will have key from 0
                """
                counter+=1
            #} if ends for check_microbe -- false/true
    #} with ends

    #for k in diversity_microbe:
        #print k,diversity_microbe[k].domain,diversity_microbe[k].phylum,diversity_microbe[k].class_m,diversity_microbe[k].order,diversity_microbe[k].family,diversity_microbe[k].genus,diversity_microbe[k].species
        
    return diversity_microbe #return to the main python

    #---------------------------------------------------
    #
    #--------------------------------------------------

def get_sample(otu_map):
#{
    """
    Collect sample names from the rep_seq otu map
    a list of sample name is returned
    """
    sample_list=[]
    """
    otu_map is a dict with rep seq name as key.. 
    value is object with sample count, rep seq name
    """
    
    for key in otu_map:
        for sample in otu_map[key].sample_count_dict:
            if not sample in sample_list:
                sample_list.append(sample)
                
            # -- if ends    
        #iteration over sample dict ends        
    #iteration over list of rep seqn ends

    logging.debug("Sample list has been created and sending. Length %d"%(len(sample_list)))
    return sample_list
    #---------------------------------------------
    #function ends--->>
    #---------------------------------------------
def print_microb_matrix(microb_matrix,sample_list,list_microb_objects,
                        run_name,conf_thresh,type_clsfc):
#{
    """
    This function prints matrix created in tsv format
    File name begins with run name, and the confidence 
    threshold provided
    type of clasfction: genus, spcs. This is to be used in output tsv file

    """
    #import xlwt
    line_domain=line_phylum="\t"
    line_class=line_order="\t"
    line_family=line_genus="\t"
    line_species="\t"
    
    for m in list_microb_objects:
        """
        Create headers for tsv file.. 
        """
        #print m
        #pprint (vars(list_microb_objects[m]))
        #print m, "Domain ", list_microb_objects[m].domain,"Phylum ",list_microb_objects[m].phylum ,"Class ", list_microb_objects[m].class_m,"Order ", list_microb_objects[m].order,"Family ",list_microb_objects[m].family," Genus ",list_microb_objects[m].genus,"Species ",list_microb_objects[m].species
        
        if not list_microb_objects[m].domain: #if empty string
            line_domain+=""+"\t"
        else:
            line_domain+=list_microb_objects[m].domain+"\t"

        if not list_microb_objects[m].phylum:  #if empty string
            line_phylum+=""+"\t"
        else:
            line_phylum+=list_microb_objects[m].phylum+"\t"
        
        if not list_microb_objects[m].class_m:  #if empty string
            line_class+=""+"\t"
        else:
            line_class+=list_microb_objects[m].class_m+"\t"
        
        if not list_microb_objects[m].order:  #if empty string
            line_order+=""+"\t"
        else:
            line_order+=list_microb_objects[m].order+"\t"

        if not list_microb_objects[m].family:  #if empty string
            line_family+=""+"\t"
        else:
            line_family+=list_microb_objects[m].family+"\t"
        
        if not list_microb_objects[m].genus:  #if empty string
            line_genus+=""+"\t"
        else:
            line_genus+=list_microb_objects[m].genus+"\t"

        if not list_microb_objects[m].species:  #if empty string
            line_species+=""+"\t"
        else:
            line_species+=list_microb_objects[m].species+"\t"

        #line_domain+=list_microb_objects[m].domain+"\t"
        #line_phylum+=list_microb_objects[m].phylum+"\t"
        #line_class+=list_microb_objects[m].class_m+"\t"
        #line_order+=list_microb_objects[m].order+"\t"
        #line_family+=list_microb_objects[m].family+"\t"
        #line_genus+=list_microb_objects[m].genus+"\t"
        #line_species+=list_microb_objects[m].species+"\t"
        
    #----for loop ends --->>>>>><<<<<<<<<<

    with open(run_name+"_"+str(conf_thresh)+"_"+type_clsfc+'.tsv', 'a') as out_file:

        out_file.write(line_domain+"\n"+line_phylum+"\n"+line_class+"\n"+line_order+"\n")
        out_file.write(line_family+"\n"+line_genus + "\n"+line_species+"\n")

        for i in range(len(sample_list)):
            """
            Remember each sample is individually a row in matrix
            """
            line=sample_list[i]+"\t"

            for j in range(len(list_microb_objects)):
                line+=str(microb_matrix[i][j])+"\t"
            out_file.write(line+"\n") 
    # rows count - sample.. variable here the microb diversity
    #------------------------------------------------------
    #} function ends 
    #---------------------------------------------------------------
def create_microb_matrix(rep_sample_map,list_microb_objects):
#{
    import numpy
    """
    rep_sample_map: rep seq dict for sample and their counts
    microb_objects - list with microbiome objects
    """
    sample_list=get_sample(rep_sample_map)
    """
    samplelist contains all sample names/ids 
    Index of sample is used further to populate matrix
    """
    
    microb_matrix=numpy.zeros((len(sample_list),len(list_microb_objects) )) #create 2D matrix
    """
    Number of rows - total samples present
    Number of variable to be the microbiome types present
    """

    for key in list_microb_objects:
        col=key
        temp_rep_seq_list=list_microb_objects[key].rep_seq
        """
        There can be multiple rep seqs having same microbiome config
        """
        for x in temp_rep_seq_list:
            sample_count_list=rep_sample_map[x].sample_count_dict
            """
            Each rep seq has sample and sample's count stored in dict
            """
            
            for s in sample_count_list:
                try:
                    row=sample_list.index(s) #get indices
                    microb_matrix[row][col]+=sample_count_list[s]
                    """
                    Increase the value.. 
                    Rep 1, 2 seq have sample 43 -> 23 and 5 resp.. 
                    Both Rep 1, and 2 have same taxonomic assignment.. 
                    Total count for the taxonomy for sample 43 should be 28!!
                    """
                except Exception as e:
                    print "Execution has to be stopped. Printing Matrix"
                    logging.debug("Having issues for %s %d row %d col " %(s,row, col))
                    logging.debug(e)
                    
            #iterating over samples in rep seq ends 
        #iterating over list of Rep Seq ends
    # iterating over microbe objects ends
    
    logging.debug("Matrix has been created with number of line %d and number of column %d"%(len(sample_list),len(list_microb_objects)))
    return microb_matrix,sample_list #return to the main python file
    #----------------------------------------------------
    #}  function ends 
    #--------------------------------------------
