#!/usr/bin/env Rscript

#Find unique species or genus count
#
#Date May 01 2017
#-mention rank: species, genus and this script will provide you count of unique ranks.

# Run from command line  ./extract_taxonomy_rank.R -t tsv_file -r rank
# rank could be species or genus

addTaxonomy<-function(tempTaxonomyName, taxonomyVector){
  
  #Function takes taxonomic value and a vector. Function finds out if value is 
  #already present in it. If not then it adds it else nothing and returns the vector. 
  
  temp_vector<-taxonomyVector  #return this at the end
    
  if(is.na(tempTaxonomyName) | tempTaxonomyName==""){
    
    #---do nothing if value is NA or null
    #print("we have issues here") #print(tempTaxonomyName)
  }
  else{
      
      if(! (gsub("<.*","",tempTaxonomyName) %in%temp_vector) ){
        
        temp_vector<-c(gsub("<.*","",tempTaxonomyName), temp_vector)    
      }
      #if taxonomy not present-----<><>
      
  }
  return(temp_vector)
}
#--------------------------------------------------
#
#--------------------------------------------------
library("argparse") #install.packages("argparse")
parser <- ArgumentParser(description='Process classification TSV file')
parser$add_argument('-t',"--tax",help="Provide TSV output from processing of RDP txt file",required=TRUE)
parser$add_argument('-r',"--rank",help="genus or species rank of which you'd like to know unique and counts",required=TRUE)
args <- parser$parse_args() #make it a data structure

#args$tax - access taonomy file

rank<-tolower(args$rank) #convert to lower case
taxonomy_file<-normalizePath(args$tax) #make into full path and store it

table<-read.table(file = taxonomy_file, sep = '\t') #read file

cat(paste("Taxonomy file loaded\n"))
cat(paste("Number of samples in the tsv file ",nrow(table)-7,"\n"  ))

taxonomy_names<-vector(length = 0) #this is used to store genus/spcies names. Length is printed in the end

if(rank == "genus"){
  
  cat(paste("We'll extract 6th row only","\n"))
  
  for (i in table[6,]){
    taxonomy_names <-addTaxonomy(i,taxonomy_names)
  }
  #--iterate through only 6th row
  
} else if(rank == "species"){
  
  cat(paste("We'll extract 7th row only","\n")) #table[7,]
  
  for (i in table[7,]){
    taxonomy_names <-addTaxonomy(i,taxonomy_names)
  }
}else{
  cat(paste("Invalid rank provided. Quiting!\n"))
  quit()
}

length(taxonomy_names) 
print("The values are")

#print(taxonomy_names)
#for (i in 1:length(taxonomy_names)){
#  print ("Print value")
 # print(taxonomy_names[i])
#}
