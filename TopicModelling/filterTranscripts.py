import getTokens
import pandas as pd
import ast
import re
import getWord2VecModel
import numpy as np
from gensim.models import Word2Vec

def trainW2vTranscripts():
	""" train a column of strings to a word2vec model"""
	df = pd.read_csv('data/captions-filtered.csv', encoding='utf-8')
	model = getWord2VecModel.getWord2Vec(train=df['transcript_clean'])
	model.most_similar(positive=['muslim'])

def cleanTranscripts():
	""" filter the transcripts by removing stopwords and stemming """
	df = pd.read_csv('data/captions-clean.csv', encoding='utf-8')
	df['transcript_clean'] = np.nan
	datalength = len(df)
	print(df.head())
	li_transcripts = ['n'] * len(df)
	for index, transcript in enumerate(df['transcript']):
		transcript_clean = ast.literal_eval(transcript)
		transcript_clean = getTokens.getTokens(li_strings=(ast.literal_eval(transcript)), lemmatizing=True)
		li_transcripts[index] = transcript_clean
		if index % 200 == 0:
			df['transcript_clean'] = li_transcripts
			df.to_csv('data/captions-filtered.csv', encoding='utf-8')
			print('Completed video ' + str(index) + '/' + str(datalength))

def removeDuplicateEntries():
	""" remove the duplicate transcript entries """
	df = pd.read_csv('data/captions.csv', encoding='utf-8')
	df.columns = ['id', 'transcript']

	li_transcripts = []
	for transcript in df['transcript']:
		li_transcript = ast.literal_eval(transcript)
		li_transcript = li_transcript[0::3]
		li_transcripts.append(li_transcript)
	df['transcript'] = li_transcripts

	df.to_csv('data/captions-clean.csv', encoding='utf-8')