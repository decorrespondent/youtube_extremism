import argparse
import os
import time
import datetime
import string

# Gensim
import gensim

# Plotting tools
import pyLDAvis

# Wrappers
from StreamingCorpus import StreamingCorpus
from StreamingPreprocesser import StreamingPreprocesser
from StreamingParser import StreamingParser

# Enable logging for gensim
import logging
import warnings
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)
warnings.filterwarnings("ignore", category=DeprecationWarning)

def main(args):
    # --------------------------------------------------
    #
    # Initialize parameters
    #
    # --------------------------------------------------
    root = os.path.dirname(os.path.realpath(__file__))

    input_file = '{}/{}'.format(root, args.input)
    # input_file = os.path.dirname(os.path.realpath(__file__)) + "/temp.json"  # temp file for testing

    # Prepare stopwords and extend if applicable
    stopwords_path = '{}/{}'.format(root, args.stopwords_file)
    stopwords = open(stopwords_path, 'r').read().split('\n')

    # Add 'stopwords' manually; TODO: substitute with spacy lemmatiser
    stopwords.extend(['know', 'think', 'like', 'thats', 'well', 'dont',
                      'get', 'actually', 'would', 'say', 'yeah', 'want', 'going',
                      'said', 'speech', 'theres', 'way', 'could', 'see', 'something',
                      'people', 'really', 'okay', 'gonna', 'ive', 'mean', 'right',
                      'got', 'thing', 'one', 'theyre', 'stuff', 'kind', 'lot',
                      'good', 'lot', 'things', 'saying', 'hes', 'even', 'much',
                      'guy', 'whatever', 'back', 'everything', 'life', 'love',
                      'guys', 'great', 'time', 'video', 'sort', 'cant', 'maybe',
                      'point', 'lets', 'take', 'talk', 'probably', 'might', 'put',
                      'years', 'new', 'two', 'need', 'yes', 'left', 'look', 'talking',
                      'anything', 'guess', 'make', 'interesting', 'someone', 'obviously',
                      'ill', 'still', 'also', 'whats', 'find', 'certain', 'course',
                      'weve', 'part', 'first', 'done', 'many', 'around', 'never',
                      'show', 'went', 'little', 'ever', 'big', 'look', 'give',
                      'last'])

    #
    # dict_min = 4
    # dict_max = 0.6

    topic_num = args.topic_num
    model_name = args.model_name
    model_path = "{}/models/{}_{}".format(root, model_name, topic_num)
    if not os.path.isdir(model_path):
        print('Model directory not found, creating directory: {}'.format(model_path))
        os.mkdir(model_path)

    # Simple preprocesser
    parser = StreamingParser(input_file, 3, metadata=True)
    preprocessor = StreamingPreprocesser(stopwords=stopwords)

    corpus = StreamingCorpus(path=input_file,
                             parse_strategy=parser,
                             clean_strategy=preprocessor,
                             dictionary=None,
                             metadata=True)
    dictionary = corpus.get_dictionary()

    gensim.corpora.MmCorpus.serialize(os.path.join(
        model_path, '{}.mm'.format(model_name)), corpus, metadata=True)
    corpus = gensim.corpora.MmCorpus(os.path.join(model_path, '{}.mm'.format(model_name)))

    # dictionary.filter_extremes(dict_min, dict_max_relative)
    dictionary.save(os.path.join(model_path, '{}.dict'.format(model_name)))

    # --------------------------------------------------
    #
    # LDA model training and serialization
    #
    # --------------------------------------------------

    t1 = time.time()
    print('Starting generation of LDA model')

    lda = gensim.models.LdaMulticore(corpus=corpus,
                                     id2word=dictionary,
                                     num_topics=topic_num,
                                     random_state=100,
                                     # update_every=1,
                                     chunksize=100,
                                     passes=10,
                                     # alpha='auto',
                                     per_word_topics=True)
    lda.save('{}/{}.lda'.format(model_path, model_name))

    t2 = time.time()
    print('LDA model generation successful! Time elapsed: {}\n'.format(t2 - t1))

    # --------------------------------------------------
    #
    # Visualisation with pyLDAvis
    #
    # --------------------------------------------------

    # t1 = time.time()
    # print('Starting preparation of LDAvis visualisation')
    #
    # # Load gensim data to prepare for visualization
    # prepared_data = pyLDAvis.gensim.prepare(lda, corpus, dictionary, sort_topics=False)
    # # Save visualisation to HTML file
    # pyLDAvis.save_html(prepared_data, os.path.join(model_path, '{}_LDAvis.html'.format(model_name)))
    #
    # t2 = time.time()
    # print('LDAvis visualisation successful! Time elapsed: {}\n'.format(t2 - t1))

    # --------------------------------------------------
    #
    # Compute model perplexity and coherence score
    #
    # --------------------------------------------------

    t1 = time.time()
    print('\nStarting computation of perplexity score')

    perplexity_score = lda.log_perplexity(corpus)
    # A measure of how good the model generalises. Lower is better.
    print('Perplexity: ', perplexity_score)

    t2 = time.time()
    print('Perplexitiy computed successfully! Time elapsed: {}\n'.format(t2 - t1))

    t1 = time.time()
    print('\nStarting computation of coherence score')

    coherence_model_lda = gensim.models.CoherenceModel(
        model=lda, corpus=corpus, dictionary=dictionary, coherence='u_mass')
    coherence_lda = coherence_model_lda.get_coherence()
    print('Coherence Score: ', coherence_lda)

    t2 = time.time()
    print('Coherence score computed successfully! Time elapsed: {}\n'.format(t2 - t1))

    # --------------------------------------------------
    #
    # Saving parameters and scores to file
    #
    # --------------------------------------------------

    print('Writing settings and results to file...')
    with open(os.path.join(model_path, '{}_parameters.txt'.format(model_name)), 'w') as file:
        file.write('Model name: {}\n date: {}\n'.format(model_name, datetime.datetime.now()))

        file.write('Corpus statistics:\n'.format())
        file.write('\tNon-empty entries: {}\n'.format(len(corpus)))

        file.write('Model parameters: \n')
        file.write('\tNumber of topics:          {}\n'.format(topic_num))
        # file.write('\tDictionary min:            {}\n'.format(dict_min))
        # file.write('\tDictionary max (relative): {}\n'.format(dict_max_relative))

        file.write('Model scores:\n')
        file.write('\tPerplexity score = {}\n'.format(perplexity_score))
        file.write('\tCoherence score = {}\n'.format(coherence_lda))
        file.write(''.format())
    print('Done!')

    # Ngram models ------------------------------------------

    # bigram_phrases = gensim.models.Phrases(data_tokens, min_count=5, threshold=100)
    # trigram_phrases = gensim.models.Phrases(bigram_phrases[data_tokens], threshold=100)
    #
    # bigram_model = gensim.models.phrases.Phraser(bigram_phrases)
    # trigram_model = gensim.models.phrases.Phraser(trigram_phrases)
    #
    # print(trigram_model[bigram_model[data_tokens[0]]])

    # def make_bigrams(documents):
    #     return [bigram_model[document] for document in documents]
    #
    # def make_trigrams(documents):
    #     return [trigram_model[bigram_model[document]] for document in documents]
    #
    # t1 = time.time()
    # data_words_bigrams = make_bigrams(data_words_nostops)
    # t2 = time.time()
    # print('Bigrams created successfully! Time elapsed: {}'.format(t2 - t1))

    # Build MALLET LDA model and test coherence scores ------------------------------------------

    # mallet_path = 'path/to/mallet-2.0.8/bin/mallet'  # update this path
    # ldamallet = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=20, id2word=id2word)
    #
    # # Show Topics
    # pprint(ldamallet.show_topics(formatted=False))
    #
    # # Compute Coherence Score
    # coherence_model_ldamallet = CoherenceModel(model=ldamallet, texts=data_words_nostop, dictionary=id2word,
    #                                            coherence='c_v')
    # coherence_ldamallet = coherence_model_ldamallet.get_coherence()
    # print('\nCoherence Score: ', coherence_ldamallet)

    # Try different number of topics (k) and compare scores ------------------------------------------

    # Find dominant topic for each document ------------------------------------------

    # Find most representative document for each topic ------------------------------------------
    # Topic inference methods?


def parse_arguments():
    parser = argparse.ArgumentParser(description="""
    Wrapper for streaming topic model implementation by Gensim.
    TODO: make config.ini
    """)
    #####  Positional arguments  #####
    parser.add_argument("input", type=str, default="temp.json",
                        help="File or directory containing the data to be processed. ")
    # parser.add_argument("dictionary", type=str)
    # parser.add_argument("output_file", type=str, help="Optional. WIP")

    #####  Preprocessing parameters  #####
    preproccesing_parameters = parser.add_argument_group('preprocessing parameters')
    preproccesing_parameters.add_argument("stopwords_file", type=str,
                        default="stopwords.txt",
                        help="Path to file containing stopwords to be removed")
    preproccesing_parameters.add_argument("-m", "--term_min_freq", type=int,
                        help="remove all terms with specified frequency (or lower)")
    preproccesing_parameters.add_argument("-M", "--term_max_freq", type=int,
                        help="remove all terms with specified frequency (or larger)")

    #####  Topic modeling parameters  #####
    topicmodel_parameters = parser.add_argument_group('topic modeling parameters')
    topicmodel_parameters.add_argument("model_name", type=str,
                        help="The name of the model. I.e. the dataset name.")
    topicmodel_parameters.add_argument("topic_num", type=int,
                        help="The name of the model. I.e. the dataset name.")

    return parser.parse_args()

if __name__ == '__main__':
    main(parse_arguments())
