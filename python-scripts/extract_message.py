#!/usr/bin/env python3


import sqlite3
import pandas as pd
import ssl
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder, TrigramAssocMeasures, TrigramCollocationFinder
import string
import re


conn = sqlite3.connect('/Users/danipan/Desktop/Friendship-Reserve/chat.db')
c = conn.cursor()

egg_msg_query = pd.read_sql_query("select text from merged_egg_2023_q1", conn)

# setup text sum
c.execute("select GROUP_CONCAT(text) from merged_egg_2023_q1 WHERE strftime('%Y', date) = '2023' AND strftime('%m', date) BETWEEN '01' AND '03'")
data = c.fetchall()

raw_data = str(data)
egg_data = re.sub(r'[^\\n*]', '', raw_data)
egg_data = raw_data

egg_tokens = word_tokenize(egg_data)

#print(egg_tokens)

# remove stopwords
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
stop_words.update(['Laughed', 'Loved', 'like', 'Liked', 'Disliked', 'dont', 'Im', 'need', 'na', 'think', 'one', 'get', 'lol','dan', 'make', 'guys', 'know', 'im', 'ill', 'Ill', 'good', 'people', 'go','want', 'got', 'love', 'also', 'if', 'Emphasized'])
punctuation = set(string.punctuation)
stop_words = stop_words.difference(punctuation)
stop_words.update(['’', "''", '“', '”', '..'])
stop_words.update(['https', 'http', 'image', 'video', 'The', 'You', 'Dan', 'Mario', 'That', 'I', 'Sadie', 'Edd', 'Tien', 'Marcella', 'Giulie'])
stop_words.update(['It', 'He', 'She', 'How', 'Will', 'What', 'This', 'That', 'Just', 'Is', 'Are', 'Am', 'am', 'is', 'are', 'and', 'And'])
egg_tokens = [word.replace('\\n', '') for word in egg_tokens]
egg_tokens = [word for word in egg_tokens if word not in punctuation]
egg_tokens = [word for word in egg_tokens if word not in stop_words]
egg_tokens = [word for word in egg_tokens if word.strip()]



#print(punctuation)
#print(egg_tokens)

# counter
from collections import Counter
freq = Counter(egg_tokens)
sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
n = 10
top_n_freq = sorted_freq[:n]

#print(top_n_freq)


# BIGRAM lambda 2
bigram_measures = BigramAssocMeasures()
finder = BigramCollocationFinder.from_words(egg_tokens)
finder.apply_freq_filter(3)
#finder.apply_ngram_filter(lambda w1, w2: 'wan' in (w1, w2))
#finder.apply_ngram_filter(lambda w1, w2: 'na' in (w1, w2))
#finder.apply_ngram_filter(lambda w1, w2: 'Laughed' in (w1, w2))
#finder.apply_ngram_filter(lambda w1, w2: 'Disliked' in (w1, w2))
#finder.apply_ngram_filter(lambda w1, w2: 'imageLaughed' in (w1, w2))
#finder.apply_ngram_filter(lambda w1, w2: 'Ill' in (w1, w2))
#finder.apply_ngram_filter(lambda w1, w2: 'give' in (w1, w2))
#finder.apply_ngram_filter(lambda w1, w2: 'Loved' in (w1, w2))
bigrams = finder.nbest(bigram_measures.raw_freq, 24)


trigram_measures = TrigramAssocMeasures()
finder = TrigramCollocationFinder.from_words(egg_tokens)
finder.apply_freq_filter(2)
#finder.apply_ngram_filter(lambda w1, w2, w3: 'Im' in (w1, w2, w3))
#finder.apply_ngram_filter(lambda w1, w2, w3: 'gon' in (w1, w2, w3))
#finder.apply_ngram_filter(lambda w1, w2, w3: 'na' in (w1, w2, w3))
#finder.apply_ngram_filter(lambda w1, w2, w3: 'dont' in (w1, w2, w3))
trigrams = finder.nbest(trigram_measures.raw_freq, 25)

freq = Counter(bigrams)
tfreq = Counter(trigrams)


for item, count in tfreq.most_common():
    phrase = " ".join(item)
    print(f"'{phrase}': {count}")

