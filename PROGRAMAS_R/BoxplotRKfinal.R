
#Leemos el fichero original

rkfinal2 <- read.csv("rkfinal2.csv", header = TRUE, sep = ';')
boxplot(rkfinal2)

rkfinaltot <- read.csv("rkfinaltodos.csv", header = TRUE, sep = ';')
boxplot(rkfinaltot)
