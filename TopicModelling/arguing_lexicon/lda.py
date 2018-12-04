import sys
sys.path.append("../")

import pickle

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# Lazy data reader into DataFrame
def read_argument_captions():
    transcripts_reader = pd.read_csv("data/captions_arguments.csv", chunksize=10)
    for batch in transcripts_reader:
        for ix, caption in batch.iterrows():
            text = ""
            for fragment, argument_label in zip(str(caption["content"]).split("\n"), str(caption["argument_labels"]).split("\n")):
                if argument_label:
                    text += fragment + " "
            yield text


with open("models/vectorizer.pkl", "rb") as count_file:
    vectorizer = pickle.load(count_file)
with open("models/vectorizer_matrix.pkl", "rb") as matrix_file:
    matrix = pickle.load(matrix_file)

lda_model = LatentDirichletAllocation(n_topics=50, max_iter=500, verbose=3, n_jobs=-1, learning_method="online")
lda_model.fit(matrix)

# Saving progress
with open("models/lda.50.pkl", "wb") as lda_file:
    pickle.dump(lda_model, lda_file)

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" | ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
        print()
        print()
    print()

print_top_words(lda_model, feature_names, 50)
