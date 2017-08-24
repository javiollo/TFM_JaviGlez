# -*- coding: utf-8 -*-
# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

from nltk.corpus import stopwords
import re
import string
from stop_words import get_stop_words
import csv
import nltk
import datetime
from dateutil import parser

def h(text):
    text = text.replace('\\', '')
    text = text.replace('`', '')
    text = text.replace('*', '')
    text = text.replace('_', '')
    text = text.replace(':', '')
    text = text.replace('{', '')
    text = text.replace('}', '')
    text = text.replace('[', '')
    text = text.replace(']', '')
    text = text.replace('(', '')
    text = text.replace(')', '')
    text = text.replace('>', '')
    text = text.replace('#', '')
    text = text.replace('+', '')
    text = text.replace('«', '')
    text = text.replace('»', '')
    text = text.replace('|', '')
    text = text.replace('\'', '')
    text = text.replace('...', ' ')
    #text = text.replace('-', '')
    text = text.replace('…', '')
    text = text.replace(',', ' ')
    text = text.replace(';', ' ')
    text = text.replace('  ', ' ')
    text = text.replace('"', '')
    text = text.replace('!', '')
    text = text.replace('¡', '')
    text = text.replace('¿', '')
    text = text.replace('?', '')
    text = text.replace('$', '')
    text = text.replace('@', '')
    text = text.replace('á', 'a')
    text = text.replace('é', 'e')
    text = text.replace('í', 'i')
    text = text.replace('ó', 'o')
    text = text.replace('ú', 'u')
    text = text.replace('Á', 'A')
    text = text.replace('É', 'E')
    text = text.replace('Í', 'I')
    text = text.replace('Ó', 'O')
    text = text.replace('Ú', 'U')
    text = text.replace('º', '')
    text = text.replace('º', '')
    text = text.replace('à', 'a')
    text = text.replace('\xc3\xb1', 'ñ')
    return text

def remove_urls (vTEXT):
    vTEXT = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', vTEXT, flags=re.MULTILINE)
    return(vTEXT)

def asignavalor(vartexto):
    valor = 0
    palneg = 0
    palneu = 0
    palpos = 0
    for word in vartexto.split():
        if scores.has_key(word):
            valor = valor + scores.get(word)
            if scores.get(word)<0:
                palneg+=1
            elif scores.get(word)>0:
                palpos+=1
            else:
                palneu+=1
        else:
            valor = valor + 0

    return {'valor':valor, 'pneg':palneg ,'ppos':palpos, 'pneu':palneu }

#Creamos una lista con las stop words en castellano
stop_words2 = get_stop_words('es')
stop_words2 = get_stop_words('spanish')

#CReamos un diccionario con las palabras para lematizar
fich = open('DATA_ENTRADA/lemmatization-es-2.txt')
diclemesp = {} # initialize an empty dictionary
for line in fich:
     key, val = line.split("\t") # The file is tab-delimited.
     diclemesp[key]=val
     
#Leemos el diccionario con las notas y las palabras lematizadas
file = open("DATA_ENTRADA/LEMATIZO_AFINN.txt")
scores = {} # initialize an empty dictionary
for line in file:
    line = line.strip()
    try:
        term, score = line.split('\t') # The file is comma delimited.
        scores[term] = int(score) # Convert the score to an integer
    except ValueError:
        print('Ignoring: malformed line: "{}"'.format(line))

#Creamos una lista con usuarios a excluir
malones = ['AddingConsultor',
	   'arpem_com',
	   'Asegurarelauto',
	   'CADENA100',
	   'carpecol',
	   'Carramolinos',
	   'CESVIMAP',
	   'DriveSmartES',
	   'elmejorseguro',
	   'FutureBrand_Es',
	   'GrupoAseguranza',
	   'Inese_seguros',
	   'Infopolizas_com',
	   'InsareInsurance',
	   'IreneGarciaSaez',
	   'JoseLuisBernal',
	   'Netijam',
	   'planetaseguros',
	   'popupmusica',
	   'potenciadinero',
	   'RockFM_ES',
	   'SegurAutoArahal',
	   'segurostv',
	   'TalyTendencias',
	   'VertiRun']

# We use the file saved from last step as example
#tweets_filename = 'DATA_ENTRADA/fichero_entrada_corto.txt'
tweets_filename = 'DATA_ENTRADA/fichero_entrada.txt'
tweets_file = open(tweets_filename, "r")

#Imprimimos la cabecera
print("username|date|retweets|favorites|text|geo|mentions|hashtags|tid|fecha|anyo|mes|dia|horacomp|hora|minuto|value|palapos|palaneg|txtnosw|tipo|twpos|twneu|twneg")

#Comienza el lio
for line in tweets_file:
    try:

	tweet = (line.split(";"))

	#Nombramos los campos
	username = tweet[0]
	date = tweet[1]
	retweets = tweet[2]
	favorites = tweet[3]
	geo = tweet[5]
	mentions = tweet[6]
	hashtags = tweet[7]
	tid = tweet[8]
	permalink = tweet[9]

	text = tweet[4].lower()
	text = remove_urls(text)
	#Quitamos links
	text = re.sub(r'http\S+', '', text)
	text = re.sub(r'pic.twitter.com\S+', '', text)
	text = re.sub(r'ow.ly\S+', '', text)
	#QUitamos caracteres rarunos.
	text = h(text).decode('utf-8')

	#Tratamos la fecha
	f = parser.parse(date)
	fecha = str(f.date())
	anyo = str(f.year)
	mes = str(f.month)
	dia = str(f.day)
	horacomp = str(f.time())
	hora = str(f.hour)
	minuto = str(f.minute)

	#print(f, fecha, anyo, mes, dia, horacomp, hora, minuto)

	if text != "":
    		lista = [i for i in text.decode('utf-8').split() if i not in stop_words2]

	#print lista
	txtnosw = ""
	for j in lista:
	    txtnosw += str(j) + " "
        txtnosw = txtnosw.replace('.', '')
        txtnosw = txtnosw.replace('/', '')
        txtnosw = txtnosw.replace('-', '')

   	value = str(asignavalor(txtnosw)['valor'])
	palaneg = str(asignavalor(txtnosw)['pneg'])
	palapos = str(asignavalor(txtnosw)['ppos'])

	#Tipificamos los tweets segun quien lso emite y a quien
	tipo = ""
	if username in ("vertiseguros") and len(mentions) == 0:
	   tipo = "Publicidad"
	elif username == "vertiseguros" and len(mentions) > 0:
	   tipo = "Respuestas"
	elif username in malones:
	   tipo = "Excluir"
	elif mentions.replace('@','') in malones:
	   tipo = "Excluir"
	else:
	   tipo = "Clientes"

	#print(tipo, username, mentions)
    
	twpos = 0
	twneu = 0
	twneg = 0

	if int(value) > 0:
	   twpos = 1
	elif int(value) < 0:
	   twneg = 1
	else:
	   twneu = 1	

	#print(value, twpos, twneu, twneg)

	parte1 = username +"|"+ date +"|"+retweets +"|"+favorites +"|"+text +"|"+geo
	parte2 = mentions +"|"+hashtags +"|"+tid
	parte3 = fecha +"|"+ anyo +"|"+ mes +"|"+ dia +"|"+ horacomp +"|"+ hora +"|"+ minuto
	parte4 =  value + "|" + palapos+"|"+ palaneg+"|"+ txtnosw+ "|" + tipo 
	parte5 = str(twpos)+"|"+ str(twneu)+"|" + str(twneg)

	todo = parte1  +"|"+ parte2  +"|"+  parte3  +"|"+  parte4 +"|"+ parte5
	

	if len(username)>0:
	   print( todo )

    except:
	# Por si casca
	continue

