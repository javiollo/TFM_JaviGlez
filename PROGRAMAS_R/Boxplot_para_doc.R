# cargar librerias
tweets <- read.csv("../DATA_SALIDA/fichero_salida.txt", sep = '|')
tweets$n = 1

library(ggplot2)
# Basic barplot
p<-ggplot(data=tweets, aes(x=tipo, y=n)) +
  geom_bar(stat="identity", colorbar("blue"))
p

library(sqldf)
library(ggplot2)

DF = sqldf('select tipo, count(*) as cuenta from tweets group by tipo')
qplot(DF$tipo,data=DF, geom="histogram")

ggplot(DF, aes(x=tipo, y=cuenta)) +
  # draw the bar plot
  geom_bar(stat="identity") +
  geom_text(aes(label=cuenta), vjust=-0.2)
