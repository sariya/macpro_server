#!/usr/bin/env Rscript

#Date 07 June 2017
#Get count of species in any genus from TSV file that is being processed from RDP output
#Run it as: rscript species_per_genus.R 

#-R version 3.4.0 (2017-04-21) -- "You Stupid Darkness"
#-------------------------------------------------------------------------------->>>>>

library("argparse") #install.packages("argparse")
parser <- ArgumentParser(description='Process classification TSV file to get unique taxonomy at a certain rank')
parser$add_argument('-t',"--tax",help="Provide TSV output from processing of RDP txt file",required=TRUE)
parser$add_argument('-g',"--genus",help="genus for which which you'd like to know unique and counts species",required=TRUE)
args <- parser$parse_args() #make it a data structure

print(args$genus)