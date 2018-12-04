import re
import pandas as pd
import numpy as np
import re
import pickle
import operator
#import glove_python
from matplotlib.font_manager import FontProperties
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords

def getTokens(li_strings='', stemming=False, lemmatizing=False):
	if stemming:
		global di_stems
		di_stems = pickle.load(open('di_stems.p', 'rb'))

	# print('imported')
	#do some cleanup: only alphabetic characters, no stopwords
	# create separate stemmed tokens, to which the full strings will be compared to:
	li_comments_stemmed = []
	len_comments = len(li_strings)
	# print(len(li_strings))
	# print('Creating list of tokens per monthly document')
	for index, comment in enumerate(li_strings):
		#create list of list for comments and tokens
		if isinstance(comment, str):
			li_comment_stemmed = []
			li_comment_stemmed = getFilteredText(comment, stemming=stemming, lemmatizing=lemmatizing)
			li_comments_stemmed.append(li_comment_stemmed)
		#if index % 1000 == 0:
			#print('Stemming/tokenising finished for string ' + str(index) + '/' + str(len_comments))
	# print(len(li_comments_stemmed))

	if stemming:
		pickle.dump(di_stems, open('di_stems.p', 'wb'))
		df_stems = pd.DataFrame.from_dict(di_stems, orient='index')
		df_stems.to_csv('di_stems_dataframe.csv', encoding='utf-8')

	return li_comments_stemmed

def getFilteredText(string, stemming=False, lemmatizing=False):
	#first, remove urls
	if 'http' in string:
		string = re.sub(r'https?:\/\/.*[\r\n]*', ' ', string)
	if 'www.' in string:
		string = re.sub(r'www.*[\r\n]*', ' ', string)

	#use nltk's tokeniser to get a list of words
	# from nltk.tokeimport TreebankWordTokenizer
	# tokenizer = TreebankWordTokenizer()
	# tokenizer.PARENS_BRACKETS = []
	# tokens = [word.lower() for sent in nltk.sent_tokenize(string) for word in tokenizer.tokenize(sent)]
	tokens = re.findall("[a-zA-Z\-\)\(]{3,50}", string)
	stemmer = SnowballStemmer("english")
	#list with tokens further processed
	li_filtered_tokens = []
	# filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
	for token in tokens:
		token = token.lower()
		#print(len(tokens))
		#only alphabetic characters, keep '(' and ')' symbols for echo brackets, only tokens with three or more characters
		#if re.search('[a-zA-Z\-\)\(]{3,50}', token):
		if re.match('[a-zA-Z\-\)\(]{3,50}', token) is not None:
			#no stopwords
			if token not in stopwords.words('english'):
				#token = token.lower()
				#shorten word if it's longer than 20 characters (e.g. 'reeeeeeeeeeeeeeeeeeeeeeeee')
				if len(token) >= 20:
					token = token[:20]
				#stem if indicated it should be stemmed
				if stemming:
					token_stemmed = stemmer.stem(token)
					li_filtered_tokens.append(token_stemmed)

					#update lookup dict with token and stemmed token
					#lookup dict is dict of stemmed words as keys and lists as full tokens
					if token_stemmed in di_stems:
						if token not in di_stems[token_stemmed]:
							di_stems[token_stemmed].append(token)
					else:
						di_stems[token_stemmed] = []
						di_stems[token_stemmed].append(token)
				#if lemmatizing is used instead
				elif lemmatizing:
					lemmatizer = WordNetLemmatizer()
					token = lemmatizer.lemmatize(token)
					li_filtered_tokens.append(token)
				else:
					li_filtered_tokens.append(token)
	return li_filtered_tokens