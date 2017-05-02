# Date May 01 2016
#Sanjeev Sariya
#source("https://bioconductor.org/biocLite.R")

#
#Annotate jamaican tree
# #ggtree v1.8.1 

#biocLite("ggtree")
#library('ggplot2')
#biocLite("ape")
#library(geiger)

library("ggtree")

library("ape")


phylip <-read.tree("kh.phy") #from ape library - read #https://www.r-phylo.org/wiki/HowTo/InputtingTrees

genotype <- read.table("country.txt", sep="\t", stringsAsFactor=F, header = TRUE)

country_name<-unique(genotype$Country)

rownames(genotype)<-genotype$X #assign taxa as row names #https://github.com/GuangchuangYu/ggtree/issues/48

genotype<-subset(genotype,select = c("Country"))

p<-ggtree(phylip)+geom_tiplab(align = T)+geom_treescale(offset = 10)

gheatmap(p,genotype,offset = 0.5,width = 0.1,font.size = 2) +
  scale_fill_manual(values=c("red", "yellow", "firebrick", "white", "red", "cyan", "orange", "grey"),
                    breaks=c("Jamaica","USA","UK","Indonesia","Laos","Australia","Vietname","Singapore") )

length(cbPalette)

length(country_name)


temp<-"/Library/Frameworks/R.framework/Versions/3.4/Resources/library/ggtree/examples/Genotype.txt"

jj<-read.table(temp, sep="\t", stringsAsFactor=F)
##########---------------##########---------------##########---------------##########---------------
getwd()

beast_file <- system.file("examples/MCC_FluA_H3.tree", package="ggtree")

beast_tree <- read.beast(beast_file)
genotype_file <- system.file("examples/Genotype.txt", package="ggtree")

genotype_y <- read.table(genotype_file, sep="\t", stringsAsFactor=F) 
colnames(genotype_y)
colnames(genotype_y) <- sub("\\.$", "", colnames(genotype_y))

p <- ggtree(beast_tree, mrsd="2013-01-01") + geom_treescale(x=2008, y=1, offset=2)
p <- p + geom_tiplab(size=2)

gheatmap(p, genotype, offset = 5, width=0.5, font.size=3, colnames_angle=-45, hjust=0) +
  scale_fill_manual(breaks=c("HuH3N2", "pdm", "trig"), values=c("steelblue", "firebrick", "darkgreen"))

