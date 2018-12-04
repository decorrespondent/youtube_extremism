import getTokens
import pandas as pd
import ast
import re
import numpy as np
from gensim.models import Word2Vec
from joblib import Parallel, delayed
import multiprocessing
from math import sqrt
from collections import defaultdict


class CallBack(object):
    completed = defaultdict(int)

    def __init__(self, index, parallel):
        self.index = index
        self.parallel = parallel

    def __call__(self, index):
        CallBack.completed[self.parallel] += 1
        print("done with {}".format(CallBack.completed[self.parallel]))
        if self.parallel._original_iterable:
            self.parallel.dispatch_next()

import joblib.parallel
joblib.parallel.CallBack = CallBack

def trainW2vTranscripts():
	""" train a column of strings to a word2vec model"""
	df = pd.read_csv('data/captions-filtered.csv', encoding='utf-8')
	model = getWord2VecModel.getWord2Vec(train=df['transcript_clean'])
	model.most_similar(positive=['muslim'])

def callable(df):
	df['transcript_clean'] = np.nan
	datalength = len(df)
	print(df.head())
	li_transcripts = ['n'] * len(df)
	for index, transcript in enumerate(df['transcript']):
		transcript_clean = ast.literal_eval(transcript)
		transcript_clean = getTokens.getTokens(li_strings=(ast.literal_eval(transcript)), lemmatizing=True)
		li_transcripts[index] = transcript_clean
	df['transcript_clean'] = li_transcripts
	return df

def cleanTranscripts():
	""" filter the transcripts by removing stopwords and stemming """
	dfs = pd.read_csv('data/captions-clean.csv', encoding='utf-8', chunksize=500, nrows=1, skiprows=range(1,40000))
	parallel = Parallel(n_jobs=multiprocessing.cpu_count())
	retlist = parallel(delayed(callable)(i) for i in dfs)
	df = pd.concat(retlist)
	# df['transcript_clean'] = np.nan
	# datalength = len(df)
	# print(df.head())
	# li_transcripts = ['n'] * len(df)
	# for index, transcript in enumerate(df['transcript']):
	# 	transcript_clean = ast.literal_eval(transcript)
	# 	transcript_clean = getTokens.getTokens(li_strings=(ast.literal_eval(transcript)), lemmatizing=True)
	# 	li_transcripts[index] = transcript_clean
	# 	if index % 200 == 0:
	# 		df['transcript_clean'] = li_transcripts
	# 		df.to_csv('data/captions-filtered.csv', encoding='utf-8')
	# 		print('Completed video ' + str(index) + '/' + str(datalength))
	# df['transcript_clean'] = li_transcripts
	df.to_csv('data/captions-filtered.csv', encoding='utf-8')
	# print('Completed video ' + str(index) + '/' + str(datalength))

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

cleanTranscripts()