import os
import json
import tarfile
from gensim import corpora
from gensim.corpora import TextCorpus
from StreamingPreprocesser import StreamingPreprocesser

DOCUMENT_MIN_TOKENS = 5
TOKEN_MIN_LEN = 2  # less than; not inclusive
TOKEN_MAX_LEN = 15 # equal to or larger tan


class StreamingCorpus(TextCorpus):
    """
    TextCorpus class 
    """
    def __init__(self, path, parse_strategy=None, clean_strategy=None, dictionary=None, metadata=False):
        self.path = path  # path to index file or main folder of docs
        self.metadata = metadata

        self.streaming_parser = parse_strategy if parse_strategy is not None else StreamingParser(self.path, 1, metadata=True)
        self.streaming_cleaner = clean_strategy if clean_strategy is not None else StreamingPreprocesser()

        self.dictionary = dictionary or corpora.Dictionary()

    def get_dictionary(self):
        return self.dictionary

    def get_texts(self):

        for tokens, metadata in self.process_entries():
            if self.metadata:
                yield tokens, metadata
            else:
                yield tokens

    def process_entries(self):

        for sources_texts, metadata in self.streaming_parser:

            # Clean the texts from all sources
            cleaned_text = []
            for token in self.streaming_cleaner.process(sources_texts):  # includes tokenizer
                cleaned_text.append(token)

            if len(cleaned_text) > 1:
                self.dictionary.add_documents([cleaned_text])
                yield cleaned_text, metadata
            else:
                continue
