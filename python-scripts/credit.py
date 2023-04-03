#!/usr/bin/env python3

import sqlite3
import pandas as pd
import ssl
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder, TrigramAssocMeasures, TrigramCollocationFinder
import re

os.environ['SSL_CERT_FILE'] = '/Users/danipan/cacert.pem'
conn = sqlite3.connect('/Users/danipan/Desktop/chat.db')

cur = conn.cursor()

#cur.execute(" select name from sqlite_master where type = 'table'")
#for name in cur.fetchall():
#    print(name)

#query = pd.read_sql_query("select * from chat limit 30", conn)


ofd_msg_query = pd.read_sql_query("select message_body from Friendship_Reserve_Feb14 WHERE member_name = 'OFD'", conn)

# setup OFD's text sum
#cur.execute("select GROUP_CONCAT(message_body) from Friendship_Reserve_Feb14 WHERE member_name = 'OFD'")
cur.execute("select GROUP_CONCAT(message_body) from Friendship_Reserve_Feb14")
data = cur.fetchall()

data = str(data)
ofd_data = re.sub(r'[^\w\s]', '', data)

try:
    # Try to download with SSL
    nltk.download('stopwords')
    nltk.download('punkt')
except ssl.SSLError:
    # If SSL fails, try downloading without SSL
    nltk.download('stopwords', ssl=False)
    nltk.download('punkt', ssl=False)


ofd_tokens = word_tokenize(ofd_data)


# remove stopwords
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
#stop_words.update(['like', 'dont', 'Im', 'need', 'na', 'think', 'one', 'get', 'lol','dan', 'make', 'guys', 'know', 'im', 'ill', 'Ill', 'good', 'people', 'go','want', 'got', 'love', 'also', 'if'])
ofd_tokens = [word for word in ofd_tokens if word.lower() not in stop_words]


# counter
from collections import Counter
freq = Counter(ofd_tokens)
sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
n = 10
top_n_freq = sorted_freq[:n]
print(top_n_freq)



bigram_measures = BigramAssocMeasures()
finder = BigramCollocationFinder.from_words(ofd_tokens)
finder.apply_freq_filter(3)
finder.apply_word_filter(lambda w: w in ('like', 'dont'))
finder.apply_ngram_filter(lambda w1, w2: 'wan' in (w1, w2))
finder.apply_ngram_filter(lambda w1, w2: 'na' in (w1, w2))
finder.apply_ngram_filter(lambda w1, w2: 'Laughed' in (w1, w2))
finder.apply_ngram_filter(lambda w1, w2: 'imageLaughed' in (w1, w2))
finder.apply_ngram_filter(lambda w1, w2: 'Ill' in (w1, w2))
finder.apply_ngram_filter(lambda w1, w2: 'give' in (w1, w2))
finder.apply_ngram_filter(lambda w1, w2: 'Loved' in (w1, w2))
finder.apply_ngram_filter(lambda w1, w2: 'Im' in (w1, w2))
bigrams = finder.nbest(bigram_measures.raw_freq, 10)

trigram_measures = TrigramAssocMeasures()
finder = TrigramCollocationFinder.from_words(ofd_tokens)
finder.apply_freq_filter(3)
finder.apply_ngram_filter(lambda w1, w2, w3: 'Im' in (w1, w2, w3))
finder.apply_ngram_filter(lambda w1, w2, w3: 'gon' in (w1, w2, w3))
finder.apply_ngram_filter(lambda w1, w2, w3: 'na' in (w1, w2, w3))
finder.apply_ngram_filter(lambda w1, w2, w3: 'dont' in (w1, w2, w3))
trigrams = finder.nbest(trigram_measures.raw_freq, 10)

# Count the frequency of each bigram
freq = Counter(bigrams)

# Print the top 10 bigrams
print(freq.most_common(10))

tfreq = Counter(trigrams)
print(tfreq.most_common(10))
