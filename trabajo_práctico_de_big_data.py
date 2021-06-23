# -*- coding: utf-8 -*-
"""Trabajo Práctico de Big Data.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DqiqBi4aIZzkEnhhroHnbMaTCVbYHWBU

# **COMPONENTE 1**

Como paso inicial del proyecto de big data, el alumno escribir un script que permita obtener una
lista de las últimas menciones de un handle o hashtag en Twitter a través de su API. Este
programa en Python deberá luego guardar los tweets en un archivo .csv para su posterior
análisis.
El archivo de salida deberá contener mínimamente: Texto del tweet, Autor, Timestamp, Número de Favs, Número de RTs
"""

import nltk
nltk.download('vader_lexicon')

!pip install langdetect

#importamos librerias
import tweepy
from textblob import TextBlob
from wordcloud import WordCloud, STOPWORDS
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
import datetime
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import SnowballStemmer
nltk.download('stopwords')
from nltk.corpus import stopwords
stopwords = set(stopwords.words('spanish'))
from sklearn.feature_extraction.text import CountVectorizer
from langdetect import detect

# Twitter Api Credentials
consumerKey = 'ogYNVLjPL8ygj4PO6vIyYVxyP'#log["key"][0]
consumerSecret = 'fS8uxKMb2hZ4GOpey1Y6AsbWDeQCIA9srJRetzCo9cAMAM6AbZ'#log["key"][1]
accessToken = '175984347-syxFReYiggzkhkr0gz5bKX4Asi5S91eNXKU0iIbV'#log["key"][2]
accessTokenSecret = '1LhUQr7jCEDxZ0BBQSs9TK2VaXiZq08f2pKMMoBPq1GkJ'#log["key"][3]

#creamos un objeto de autenticacion
authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret) 
    
# Seteamos el access token y access token secret
authenticate.set_access_token(accessToken, accessTokenSecret) 

#Creamos el objeto API mientras parseamos la informacion en auth  
api = tweepy.API(authenticate, wait_on_rate_limit = True)

#Pedimos que ingrese los tweets a buscar
print('Analizar Sentimientos de Tweets')
keyword = input("Ingrese el hastag o keyword que desea buscar: ")
nroTweet = int(input("Ingrese cuantos tweets desea buscar: "))

list = tweepy.Cursor(api.search, q=keyword ,tweet_mode='extended', lang='es').items(nroTweet)

#Almacenamos los tweets en una lista
tweet_list = []
for tweet in list:
    text = tweet._json["full_text"]
    #print(text)
    favourite_count = tweet.favorite_count
    retweet_count = tweet.retweet_count
    created_at = tweet.created_at
    author = tweet.author.name
    
    line = {'text' : text, 'author' : author, 'favourite_count' : favourite_count, 'retweet_count' : retweet_count, 'created_at' : created_at}
    tweet_list.append(line)

#Convertimos la lista a un DataFrame
dfTweets = pd.DataFrame(tweet_list)

#Seteamos la funcion para limpiar los tweets
def cleanTxt(text):
 text = re.sub('@[A-Za-z0–9]+', '', text) #Removing @mentions
 text = re.sub('#', '', text) # Removing '#' hash tag
 text = re.sub('RT[\s]+', '', text) # Removing RT
 text = re.sub('https?:\/\/\S+', '', text) # Removing hyperlink
 
 return text

#Limpiamos los tweets y renombramos las columnas
dfTweets = dfTweets.rename(columns={'text': 'Tweets', 'author': 'Author', 'favourite_count': 'Favourites', 'retweet_count': 'Retweets', 'created_at': 'Date'})
dfTweets['Tweets'] = dfTweets['Tweets'].apply(cleanTxt)

#Creamos el archivo csv
dfTweets.to_csv('tweets.csv')

dfTweets

"""# **COMPONENTE 2**

El alumno deberá crear un script en Python que calcule el sentimiento de cada tweet y
almacene los resultados en un archivo .csv. Además, se deberá calcular el sentimiento
promedio relacionado a las menciones.
"""

#creamos un data frame con unicamente los tweets
tweets = pd.DataFrame(dfTweets['Tweets'])

tweets.head()

# crear la funcion para obtener la subjectividad
def getSubjectivity(text):
   return TextBlob(text).sentiment.subjectivity

# Crear la funcion para obtener la polaridad
def getPolarity(text):
   return  TextBlob(text).sentiment.polarity


# Crear dos nuevas columnas 'Subjectividad' & 'Polaridad'
tweets['Subjectividad'] = tweets['Tweets'].apply(getSubjectivity)
tweets['Polaridad'] = tweets['Tweets'].apply(getPolarity)

# Show the new dataframe with columns 'Subjectivity' & 'Polarity'
tweets

# Crear una funcion para calcular negativo (-1), neutral (0) and positivo (+1) 
def getAnalysis(score):
  if score < 0:
    return 'Negativo'
  elif score == 0:
    return 'Neutral'
  else:
    return 'Positivo'

tweets['Analisis'] = tweets['Polaridad'].apply(getAnalysis)

#Convertimos el df en csv
tweets.to_csv('TweetsSentimentAnalysis.csv')

# Show the dataframe
tweets

#Porcentaje de Tweets Positivos
ntweets = tweets[tweets.Analisis == 'Positivo']
ntweets = ntweets['Tweets']
ntweets

round( (ntweets.shape[0] / tweets.shape[0]) * 100, 1)

#Porcentaje de Tweets Negativos
# Print the percentage of negative tweets
ntweets = tweets[tweets.Analisis == 'Negativo']
ntweets = ntweets['Tweets']
ntweets

round( (ntweets.shape[0] / tweets.shape[0]) * 100, 1)

#Porcentaje de Tweets Neutros
ntweets = tweets[tweets.Analisis == 'Neutral']
ntweets = ntweets['Tweets']
ntweets

round( (ntweets.shape[0] / tweets.shape[0]) * 100, 1)