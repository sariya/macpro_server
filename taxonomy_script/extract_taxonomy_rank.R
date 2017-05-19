#!/usr/bin/env Rscript

#Find unique species or genus count
#
#Date May 01 2017
#-mention rank: species, genus and this script will provide you count of unique ranks.

# Run from command line Rscript  extract_taxonomy_rank.R 
#

library("argparse") #install.packages("argparse")
parser <- ArgumentParser(description='Process classification TSV file')
parser$add_argument('-t',"--tax",help="Provide TSV output from processing of RDP txt file")

print("Helloooo")
args <- parser$parse_args() #make it a data structure



