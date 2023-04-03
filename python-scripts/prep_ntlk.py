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
try:
    # Try to download with SSL
    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
except ssl.SSLError:
    # If SSL fails, try downloading without SSL
    nltk.download('stopwords', ssl=False)
    nltk.download('punkt', ssl=False)
    nltk.download('averaged_perceptron_tagger', ssl=False)

