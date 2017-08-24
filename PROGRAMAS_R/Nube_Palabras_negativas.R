# cargar librerias
library(tm)
library(wordcloud)
library(dplyr)

tweets <- read.csv("../DATA_SALIDA/fichero_salida.txt", sep = '|')
tweetsneg <- filter(tweets, value < 0)
tweetsneg <- filter(tweetsneg, tipo != "Publicidad")
tweetsneg <- filter(tweetsneg, tipo != "Excluir")
hist(tweetsneg$value)

# obtiene el texto de los tweets
txt = tweetsneg$txtnosw

##### inicio limpieza de datos #####
# remueve retweets
txtclean = gsub("(RT|via)((?:\\b\\W*@\\w+)+)", "", txt)
# remove @otragente
txtclean = gsub("@\\w+", "", txtclean)
# remueve simbolos de puntuación
txtclean = gsub("[[:punct:]]", "", txtclean)
# remove números
txtclean = gsub("[[:digit:]]", "", txtclean)
# remueve links
txtclean = gsub("http\\w+", "", txtclean)

txtclean = gsub("seguro", "seguros", txtclean)
txtclean = gsub("seguross", "seguros", txtclean)
##### fin limpieza de datos #####

# construye un corpus
corpus = Corpus(VectorSource(txtclean))

# convierte a minúsculas
corpus = tm_map(corpus, tolower)
# remueve palabras vacías (stopwords) en español
corpus = tm_map(corpus, removeWords, c(stopwords("spanish"), "camila_vallejo"))
# carga archivo de palabras vacías personalizada y lo convierte a ASCII
#sw <- readLines("stopwords_es.txt",encoding="UTF-8")
sw <- read.csv("../DATA_ENTRADA/stopwords_es.txt")
sw = iconv(sw, to="ASCII//TRANSLIT")
# remueve palabras vacías personalizada
corpus = tm_map(corpus, removeWords, sw)
# remove espacios en blanco extras
corpus = tm_map(corpus, stripWhitespace)

# crea una matriz de términos
tdm <- TermDocumentMatrix(corpus)

# convierte a una matriz
m = as.matrix(tdm)

# conteo de palabras en orden decreciente
wf <- sort(rowSums(m),decreasing=TRUE)
head(wf, 15)
# crea un data frame con las palabras y sus frecuencias
dm <- data.frame(word = names(wf), freq=wf)

# grafica la nube de palabras (wordcloud)
wordcloud(words = dm$word, freq = dm$freq, min.freq = 50,
          max.words=50, random.order=FALSE, rot.per=0.35, 
          colors=brewer.pal(8, "Dark2"))

head(dm, 10)

barplot(dm[1:10,]$freq, las = 2, names.arg = dm[1:10,]$word,
        col ="lightblue", main ="Palabras más frecuentes",
        ylab = "Frecuencia")


dtm <- DocumentTermMatrix(corpus)
freq <- colSums(as.matrix(dtm))
length(freq)
ord <- order(freq,decreasing=TRUE)
freq[head(ord)]
