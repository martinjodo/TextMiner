"""
PYTHON 3 - T E X T  M I N E R - v 1.0
by Martin Doden - October 2018
"""

import string
import re
#import pandas as pd
from collections import Counter 
from nltk.corpus import wordnet 
from nltk.stem import WordNetLemmatizer


# LOAD NECESSARY DATA FILES
stopwords_file = open("stopwords_onix.txt", "r")
stopwords = stopwords_file.read().split()
expressions = ('rt', 'quote')
http_prefixes = ('http', 'https', 'htt', 'www')
wnl = WordNetLemmatizer()
# - - - - - - - - - - - - - - - - - - - - - - - - - - METHOD SECTION - - - - - - - - - - - - - - - - - - - - - - - - - - 

# 1) PREPROCESSING OPERATIONS / DATA CLEANING

# METHOD SECTION - ALL PREPROCESSING METHODS USED IN PROGRAM
def remove_punctuation(value_string):
    result = ""
    for c in value_string:
        if c not in string.punctuation:
            result += c
        else:
            result += " "
    return result

def remove_digits(value_string):
    result = ""
    for c in value_string:
        # If char is not digits, add it to the result.
        if c not in string.digits:
            result += c
        else:
            result += " "
    return result

def remove_3chars(string_split):
    return ' '.join([w for w in string_split if len(w)>3])

def remove_whitespace(value_string):
    return re.sub('\s+',' ',value_string).strip()

def remove_stopwords(string_split):
    return ' '.join([w for w in string_split if w not in stopwords])

def remove_expressions(string_split):
    return ' '.join([w for w in string_split if w not in expressions])

def remove_http(string_split):
    return ' '.join([w for w in string_split if not w.startswith(http_prefixes)])

# 2) LEMMATIZATION OF TEXT STRING

def lemmatizer(value_string):
    return ' '.join([wnl.lemmatize(w, get_pos(w)) for w in value_string.split()])

def get_pos(word):
    w_synsets = wordnet.synsets(word)
    pos_counts = Counter()
    pos_counts["n"] = len(  [ item for item in w_synsets if item.pos()=="n"]  )
    pos_counts["v"] = len(  [ item for item in w_synsets if item.pos()=="v"]  )
    pos_counts["a"] = len(  [ item for item in w_synsets if item.pos()=="a"]  )
    pos_counts["r"] = len(  [ item for item in w_synsets if item.pos()=="r"]  )
    most_common_pos_list = pos_counts.most_common(3)
    return most_common_pos_list[0][0]

# - - - - - - - - - - - - - - - - - - - - - - - - - - DATA INPUT SECTION - - - - - - - - - - - - - - - - - - - - - - - 

# SIMPLE TXT FILE

# CSV TABLE
# data = pd.read_csv('SKYW.csv', sep=',')
# data = data['FullContent']
# count_row = data.shape[0]

# - - - - - - - - - - - - - - - - - - - - - - - - - - MAIN SECTION - - - - - - - - - - - - - - - - - - - - - - - - - - 
def main():

    # Preprocessing TXT file
    file = open("Textfile.txt", "r")
    string_data = file.read()
    string_output = open("TextMining_result.txt", "w+")

    # To Lower Case
    string_data = string_data.lower()

    # Remove Punctuation
    string_data = remove_punctuation(string_data)

    # Remove Digits
    string_data = remove_digits(string_data)

    # Remove Words with < 3 chars
    string_data = remove_3chars(string_data.split())

    # Remove Whitespace
    string_data = remove_whitespace(string_data)

    # Remove Stopwords
    string_data = remove_stopwords(string_data.split())

    # Remove HTTP etc
    string_data = remove_http(string_data.split())

    # Remove Expressions (e.g. RT)
    string_data = remove_expressions(string_data.split())

    # Lemmatize preprocessed string
    string_data = lemmatizer(string_data)

    print(string_data)

    string_output.write(string_data)
    string_output.close()
    file.close()

if __name__ == "__main__":
    main()
