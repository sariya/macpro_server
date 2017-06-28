#!/usr/bin/env Rscript

#Created on June 2017
#Sanjeev Sariya
#
#This R script prints sum all counts in all classification from TSV file
#
# Rscript get_sum_clssfctn.R -f sample.txt

library("argparse") #install.packages("argparse")

parser <- ArgumentParser(description="Process classification TSV file to get counts of all cells")
parser$add_argument('-f',"--file",help="TSV file that is to be read",required=TRUE) #TSV file that is to be read

args <- parser$parse_args() #make it a data structure
taxonomy_file<-normalizePath(args$file) #make into full path and store it

table<-read.table(file = taxonomy_file, sep = '\t',fill = TRUE) #read file and make table

#fill = TRUE for empty value in first 7 rows

table<-tail(table,-7)


#sum(table) --canot do this because all variables are factor.
#convert factor to as.charcater and then to numeric

cat("Sum of all taxonomic counts",sum(sapply(table[,-1],function(x){
	if(is.factor(x) ) as.numeric(as.character(x))
	else x
			   } #--function ends
	) #-- sapply ends
				    )#--sum ends
   ,"\n"
   )#-cat ends
#-- -1 because we want to ignore name of all samples. B