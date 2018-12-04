import string


class StreamingPreprocesser(object):

    def __init__(self, stopwords=None, processes=None):
        self.source_generator = None

        self.stopwords = stopwords if stopwords is not None else open('stopwords-nl.txt', 'r').read().split('\n')

        punctuation = string.punctuation
        punctuation += '`’‘”“'
        self.punctuation_table = str.maketrans('', '', punctuation)

        spacers = '\n\r\t'
        self.spacers_table = str.maketrans(spacers, ' ' * len(spacers))

        self.processes = processes
        if self.processes is None:
            self.processes = [
                              # self.process_string,
                              self.encode_doc_to_ascii,
                              self.remove_punctuation,
                              self.remove_spacers,
                              self.to_lower_case,
                              self.tokenise,
                              self.remove_stopwords,
                              self.remove_digit_terms,
                              self.remove_min_len
                              ]

    def __iter__(self):
        for tokens in self.process(self.source_generator):
            yield tokens

    def add_processor(self, process):
        if callable(process):
            self.processes.append(process)

    def process(self, text):
        pipeline = text
        pipeline = [pipeline] if type(pipeline) == str else pipeline
        for processor in self.processes:
            pipeline = processor(pipeline)
        return pipeline

    def encode_doc_to_ascii(self, texts):
        for text in texts:
            yield text.encode('ascii', errors='ignore').decode('utf8')
            # List all non ascii characters and translate/filter them out

    def remove_punctuation(self, texts):
        for text in texts:
            yield text.translate(self.punctuation_table)

    def remove_spacers(self, texts):
        for text in texts:
            yield text.translate(self.spacers_table)

    def to_lower_case(self, texts):
        for text in texts:
            yield text.lower()

    def tokenise(self, texts):
        for text in texts:
            for token in text.split():
                yield token

    def remove_stopwords(self, tokens):
        for token in tokens:
            if token not in self.stopwords:
                yield token
            else:
                continue

    def remove_digit_terms(self, tokens):
        for token in tokens:
            if not token.isdigit():
                yield token
            else:
                continue

    def remove_min_len(self, tokens):
        for token in tokens:
            if len(token) > 2:  # self.token_min
                yield token
            else:
                continue
