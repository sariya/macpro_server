
#Date April 2017 12
#
#

#installed.packages()
library(taxize)
fileName <- "/Users/sariyasanjeev/Documents/files_work/rdp_core_march212017/RDPClassifier_16S_trainsetNo16_rawtrainingdata/missing_taxonomy.txt"
conn <- file(fileName,open="r")
lines_file <-readLines(conn)

for (i in 1:length(lines_file)){
  
  accession_id<-lines_file[i]
  uid<-tryCatch(genbank2uid(id = accession_id)[1],warning=function(w) NULL )
  
  if(is.null(uid)){
    
    print (paste(accession_id,"has issues getting taxonomy",collapse = "\t"))
  }
  
  if(!is.null(uid)){  #CP010424
    
    tax_rank<-classification(uid, db = 'ncbi') 
    
    label_tax<-tax_rank[[1]] #label's 1st thing 
    new_df_withoutrank<-label_tax[label_tax$rank!="no rank",]
    
    value<-"" #store scpecies name
    
    taxono_string<-vector(mode = "character",length = 8) #create vector of 7 length
    taxono_string[1]<- accession_id
    {
    
    #--iterate over 7 ranks of microbiome and get value stored
    if(length(which(new_df_withoutrank$rank=="superkingdom")) ==1){
      taxono_string[2]<-new_df_withoutrank[which(new_df_withoutrank$rank=="superkingdom"),1]
    }
    else{
      taxono_string[2]<-"-"
    }
    if(length(which(new_df_withoutrank$rank=="phylum")) ==1){
      taxono_string[3]<-new_df_withoutrank[which(new_df_withoutrank$rank=="phylum"),1]
    }
    else{
      taxono_string[3]<-"-"
    }
    if(length(which(new_df_withoutrank$rank=="class")) ==1){
      taxono_string[4]<-new_df_withoutrank[which(new_df_withoutrank$rank=="class"),1]
    }
    else{
      taxono_string[4]<-"-"
    }
    if(length(which(new_df_withoutrank$rank=="order")) ==1){
      taxono_string[5]<-new_df_withoutrank[which(new_df_withoutrank$rank=="order"),1]
    }
    else{
      taxono_string[5]<-"-"
    }
    if(length(which(new_df_withoutrank$rank=="family")) ==1){
      taxono_string[6]<-new_df_withoutrank[which(new_df_withoutrank$rank=="family"),1]
    }
    else{
      taxono_string[6]<-"-"
    }
    if(length(which(new_df_withoutrank$rank=="genus")) ==1){
      taxono_string[7]<-new_df_withoutrank[which(new_df_withoutrank$rank=="genus"),1]
    }
    else{
      taxono_string[7]<-"-"
    }
    if(length(which(new_df_withoutrank$rank=="species")) ==1){
      
      
      temp_sp<-new_df_withoutrank[which(new_df_withoutrank$rank=="species"),1]
      temp_sp<-gsub(" ","_",temp_sp)  
      taxono_string[8]<-temp_sp
    }
    else{
      taxono_string[8]<-paste(accession_id,"_unclassified")
    }
    #-- End iterate over 7 ranks of microbiome and get value stored
    }
    
    for (i in 1:length(taxono_string))
      #print (value)
      {
      value<-paste(value,taxono_string[i],collapse = "\t")
      print (value)
      }
    
    print(value)
    
  } #--if UID not nULL
  
}
close(conn)



#-----------------#-----------------#-----------------#-----------------#-----------------#-----------------#-----------------
t<-"D85479"

#genbank2uid(id = 'CP002122')
#class(genbank2uid(id = 'CP002122')) typeof(genbank2uid(id = 'CP002122'))

uid<-genbank2uid(id = "CP010424")[1]

tax_rank<-classification(uid, db = 'ncbi') #typeof(tax_rank[[1]])

jj<-tax_rank[[1]]

new_df_withoutrank<-jj[jj$rank!="no rank",]

value<-""


taxono_string<-vector(mode = "character",length = 6)
kik<-which(new_df_withoutrank$rank=="species")
length(kik)

if( is.null(kik)){
  print("waah re")
}
new_df_withoutrank[2,1]
{
if(length(which(new_df_withoutrank$rank=="species")) ==1){
  #print ("azaa")
  #print(which(new_df_withoutrank$rank=="species")),2)
  
  #print (new_df_withoutrank[which(new_df_withoutrank$rank=="species"),1])
  taxono_string[6]<-new_df_withoutrank[which(new_df_withoutrank$rank=="species"),1]
}
else{
  print("gandha hai sab")
}
if(length(which(new_df_withoutrank$rank=="genus")) ==1){
  print("mil gaya genus")
}
else{
  taxono_string[5]<-"-"
  print("genus not mila")
}
}

print( taxono_string)
for (k in taxono_string) print (k)

for(i in 1:nrow(new_df_withoutrank)){
  
  for(j in 1:ncol(new_df_withoutrank)){
    
    if(new_df_withoutrank[i,j] == "superkingdom"){
      
      print(new_df_withoutrank[i,j-1])
      value<-paste(value,new_df_withoutrank[i,j-1],collapse  = "\t")
    }
    if(new_df_withoutrank[i,j] == "phylum"){
      
      print(new_df_withoutrank[i,j-1])
      value<-paste(value,new_df_withoutrank[i,j-1],collapse  = "\t")
    }
    if(new_df_withoutrank[i,j] == "class"){
      
      print(new_df_withoutrank[i,j-1])
      value<-paste(value,new_df_withoutrank[i,j-1],collapse  = "\t")
    }
    if(new_df_withoutrank[i,j] == "order"){
      
      print(new_df_withoutrank[i,j-1])
      value<-paste(value,new_df_withoutrank[i,j-1],collapse  = "\t")
    }
    if(new_df_withoutrank[i,j] == "family"){
      
      print(new_df_withoutrank[i,j-1])
      value<-paste(value,new_df_withoutrank[i,j-1],collapse  = "\t")
    }
    if(new_df_withoutrank[i,j] == "genus"){
      
      print(new_df_withoutrank[i,j-1])
      value<-paste(value,new_df_withoutrank[i,j-1],collapse  = "\t")
    }
    if(new_df_withoutrank[i,j] == "species"){
      
      print(new_df_withoutrank[i,j-1])
      tempsp<-gsub(" ","_",new_df_withoutrank[i,j-1])
      
      value<-paste(value,tempsp,collapse  = "\t")
    }
    
  } #for loop for column ends
  
} #top for loop of rows ends

print(value)


#sessionInfo()
#tax_rank[[1]]$name

#o<-names(tax_rank)

#tax_rank$`553174`

#class(tax_rank$`553174`)


#myDf <- head(iris) nRowsDf <- nrow(myDf)
