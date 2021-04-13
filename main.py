import csv
import itertools 
import operator
import numpy as np
import sys
import nltk
from nltk.tokenize import word_tokenize, RegexpTokenizer, WordPunctTokenizer
from nltk.probability import FreqDist
from datetime import datetime
from utils import *
import matplotlib.pyplot as plt

##define the variables 
vocabulary_size = 8000
unknown_token = "UNKNOWN_TOKEN"
sentence_start_token = "SENTENCE_START"
sentence_end_token = "SENTENCE_END"
match_tokenizer = RegexpTokenizer("[\w']+")
#################
##Part 1
##read the text source for self-supervision
tokenized_sentence = []
num_sentences = 0
print("Reading CSV File ...")
with open('data/reddit-comments-2015-08.csv','r') as f:
    reader = csv.reader(f, skipinitialspace = True)
    
    fields = next(reader) 
    for row in reader:

        ##different ways to tokeinze the sentence
        #tokens_nltk = word_tokenize(row[0])
        #tokens_split = row[0].split()
        #print("The length of the list with"len(tokens_nltk))
        #print(len(tokens_split))
        #print(len(match_tokenizer.tokenize(row[0])))
        
        ##words and punctuations tokenizer
        sentence = WordPunctTokenizer().tokenize(row[0])
        #print(len(sentence))
        temp = [sentence_start_token]+sentence+[sentence_end_token]
        #print(len(tokenized_sentence))
        #data_analysis = FreqDist(tokenized_sentence)
        #data_analysis.plot(100, cumulative=False)
        tokenized_sentence.append(temp)
        num_sentences += 1

#print("The number of sentences read is %d"%(num_sentences))
#print(tokenized_sentence)

##to get the freqency distribution
all_sentences = []
for x in tokenized_sentence:
    all_sentences += x 

#print(all_sentences)

data_analysis = FreqDist(all_sentences)
#print(data_analysis.items())
vocab = data_analysis.most_common(vocabulary_size-1)
vocab_words = [x[0] for x in vocab]
vocab_words.append(unknown_token)
#print(vocab[-1][0])
#print(len(vocab_words))
#print(vocab_words)

vocab_words_index = dict([(w,i) for i,w in enumerate(vocab_words)])
#print(vocab_words_index)

tokenized_sentence_new = []
for i in tokenized_sentence:
    tokenized_sentence_new.append([w if w in vocab_words_index else unknown_token for w in i])

#print(tokenized_sentence_new)
print("Eamples : %s"%tokenized_sentence_new[14999])

#####################
##Part 2
##create the training dataset

X_train = np.asarray([[vocab_words_index[w] for w in sen[:-1]] for sen in tokenized_sentence_new])
Y_train = np.asarray([[vocab_words_index[w] for w in sen[1:]] for sen in tokenized_sentence_new])

print(X_train[14999])

