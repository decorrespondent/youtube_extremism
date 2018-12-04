import pandas as pd
import ast
import pickle as p
from gensim.models import Word2Vec

def getW2vModel(train='', load='', modelname='', min_word=200):
	"""
	Trains or loads a word2vec model. Input must be a list of strings.
	Keyword arguments:
	train -- when provided, trains, saved (in binary) and returns a model
	load -- when provided, loads and returns a model (usually stored in .model.bin)
	modelname -- name of the saved model
	min_word -- the minimum amount of occurances of words to be included in the model. Useful for filtering out bloat.
	"""

	if train != '':
		print('Training ' + modelname)
		# train model
		# neighbourhood?
		model = Word2Vec(train, min_count=min_word)
		# pickle the entire model to disk, so we can load&resume training later
		model.save(modelname + '.model')
		#store the learned weights, in a format the original C tool understands
		model.wv.save_word2vec_format(modelname + '.model.bin', binary=True)
		return model
	elif load != '':
		model = Word2Vec.load(load)
		return model

def getStrings():
	df = pd.read_csv('data/captions-filtered-final.csv', encoding='utf-8')
	li_transcripts = df['transcript_clean']
	li_str_transcripts = []

	for full_transcript in li_transcripts:
		li_full_transcript = ast.literal_eval(full_transcript)
		for sent_transcript in li_full_transcript:
			#li_transcript = ast.literal_eval(sent_transcript)
			str_transcript = ' '.join(sent_transcript)
			li_str_transcripts.append(str_transcript)
	print(li_str_transcripts[:10])
	p.dump(li_str_transcripts, open('li_str_transcripts.p', 'wb'))
	return li_str_transcripts

li_str_transcripts = getStrings()
model = getW2vModel(train = li_str_transcripts, modelname='youtube-transcripts')
print(model.most_similar)