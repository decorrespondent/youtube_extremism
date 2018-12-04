import os
import time

# Gensim
from gensim import corpora, models, similarities
from gensim.corpora import Dictionary

# Plotting tools
import pyLDAvis
import pyLDAvis.gensim

# Enable logging for gensim - optional
import logging
import warnings
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)
warnings.filterwarnings("ignore", category=DeprecationWarning)


def main():
    root = os.getcwd()
    model_name = 'captions_right'
    topic_num = 50

    model_path = '{}/models/{}_{}'.format(root, model_name, topic_num)

    corpus = corpora.MmCorpus('{}/{}.mm'.format(model_path, model_name))
    lda = models.LdaMulticore.load('{}/{}.lda'.format(model_path, model_name))
    dictionary = Dictionary.load('{}/{}.dict'.format(model_path, model_name))

    t1 = time.time()
    print('Starting preparation of LDAvis visualisation')

    # # Load gensim data to prepare for visualization
    prepared_data = pyLDAvis.gensim.prepare(lda, corpus, dictionary, sort_topics=False)

    # Save visualisation to HTML file
    pyLDAvis.save_html(prepared_data, os.path.join(model_path, '{}_LDAvis.html'.format(model_name)))

    t2 = time.time()
    print('LDAvis visualisation successful! Time elapsed: {}\n'.format(t2 - t1))


if __name__ == '__main__':
    main()
