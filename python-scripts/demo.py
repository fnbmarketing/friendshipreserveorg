#!/usr/bin/env python3


import sqlite3
import pandas as pd
import ssl
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder, TrigramAssocMeasures, TrigramCollocationFinder
from nltk.corpus import stopwords
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

tagged_tokens = nltk.pos_tag(egg_tokens)


# extract pairs
from collections import Counter
freq = Counter(tagged_tokens)
pairs = []
for i in range(len(tagged_tokens) - 1):
    word1, pos1 = tagged_tokens[i]
    word2, pos2 = tagged_tokens[i+1]
    if (pos1.startswith('JJ') or pos1.startswith('RB')) and pos2.startswith('NN'):
        pairs.append((word1, word2))

# Print the extracted pairs
#print(pairs)


from collections import Counter

freq = Counter(pairs)
sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
top_10_freq = sorted_freq[:20]


for item, count in top_10_freq:
    phrase = " ".join(item)
    print(f"'{phrase}': {count}")
