
__author__="Sanjeev Sariya"
__date__="Feb 08 2016"

"""
microbome class

method variables start with and underscore

"""
from pprint import pprint

class Microbiome:
    """
    Microbiome is a taxonomy class. Taxonomy has 7 ranks here:
    domain, phylum, class, order, family, genus and species
    """
    
    def __init__(self):

        self.sample_counts={}
        """
        Dict holding Sample names that have same taxonomy
        """
        self.domain=""
        self.phylum=""
        self.class_m=""
        self.order=""
        self.family=""
        self.genus=""
        self.species=""
    #--------------------------
    #Date Added June 14 2017
    #--------------------------
    
    def update_microbe_sample(self,_sample_name):

        """
        One microbe taxonomy can be present multiple times in one sample [454's older pipeline]
        Update the count for the microbe taxonomy by either adding sample and initiating its value as one
        Or, update it by one
        """
        
        if _sample_name in self.sample_counts:
            self.sample_counts[_sample_name]+=1

        else:
            self.sample_counts[_sample_name]=1

    #--------------------------
    # Date June 14 2017
    #--------------------------
    def set_attributes(self,list_taxonomy,temp_sample_name):
        """
        Set attributes of the microbe object
        list_taxonomy has 7 elements  
        """
        self.domain=list_taxonomy[0] #domain
        self.phylum=list_taxonomy[1] #phylum 
        self.class_m=list_taxonomy[2] #class 
        self.order=list_taxonomy[3] #order 
        self.family=list_taxonomy[4] #family
        self.genus=list_taxonomy[5] #genus
        self.species=list_taxonomy[6] #species
        self.sample_counts[temp_sample_name]=1 #initlize with count as 1 for the sample
        
    #-------------------------------
    #Added June 15th 2017
    #-------------------------------

    def print_attributes(self):
        """
        Called by object itself to print its content
        """
        print "In the vars print methods"
        pprint(vars(self))
        print "Printed every thing here"
    #-------------------------------
    #Added June 15th 
    #-------------------------------
    def add_sample_count(self):

        return sum((self.sample_counts).values())
    #----------------------------
    # Added June 15th 2017
    #----------------------------
