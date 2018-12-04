import ast
import csv
import json
import sys


class StreamingParser(object):
    """
    Wrapper class for different approaches to loading texts.

    Included approaches:
    - Directory iteration
    - JSON iteration (evaluate per line, search for certain keys)
    """
    def __init__(self, file_path, iter_methods_index, metadata=False):
        self.path = file_path
        iter_methods = [self.directory_iterator, self.json_iterator, self.frog_iterator, self.csv_iterator]
        self.iter_method = iter_methods[iter_methods_index]
        self.metadata = metadata
        self.empty_counter = 0

    def __iter__(self):
        if self.metadata:
            for text, metadata in self.iter_method():
                yield text, metadata
        else:
            for text in self.iter_method():
                yield text

    def directory_iterator(self):
        """
        Iterable object (generator) for aggregating plain text files in a given directory.
        """
        for filename in os.listdir(self.path):
            with open(os.path.join(self.path, filename), 'r') as file:
                # date = file.readline()
                yield file.read()

    def frog_iterator(self):
        """
        Parser method for parsing frog tar.gz archives.
        """
        print("Loading input from Frog file")

        with tarfile.open(self.path, 'r:gz') as tf:
            for i, entry in enumerate(tf):
                print(i)
                if not entry.isdir():
                    _id = os.path.basename(entry.name)

                    file_path = '{}{}{}'.format(self.path, '/extracted_data/docs/', _id)
                    with open(file_path, 'r') as f:
                        _id = f.readline()
                        _name = f.readline()
                        _collection = f.readline()
                        _type = f.readline()
                        _classification = f.readline()
                        _date = f.readline()

                    entry_string = []
                    for line in tf.extractfile(entry):
                        line = line.decode('utf-8').split('\t')
                        if line[0] is not '\n':
                            if line[4][0] == 'N':
                                entry_string.append(line[2])
                    yield ' '.join(entry_string), (_id, _name, _collection, _type, _classification, _date)

    def json_iterator(self):
        """
        Iterable object (generator) for aggregations of ORI (Elasticsearch) data.
        The aggregations are in JSON format, with each line containing one entry.
        The StreamingJSON object iterates over all lines contained in the file that was
        passed as a parameter.
        Iter yields only the raw text from the object, in this case
        the description field per source. If more than one source is found,
        Iter concatenates the results to one string. This string is then returned,
        and control is yielded to the caller. If no description is found, the
        KeyError exception is caught and a message is printed to the console.
        """
        print("Loading input as JSON formatted file")

        with open(self.path) as json_file:
            for index, line in enumerate(json_file):
                print("extracting line {}".format(index))
                json_data = json.loads(line)

                # Extract all descriptions of the sources and append them to the main data list
                doc_data = ''

                try:
                    _id = json_data['_id']
                    _name = json_data["_source"].get('name', "").replace('\n', '').replace('\r', '').replace(',', '')
                    _collection = json_data["_source"].get('meta', {}).get('collection', "No Collection available")
                    _type = json_data['_type']
                    _classification = json_data["_source"].get('classification', "No classification in data")
                    _date = json_data["_source"].get('end_date', "No end_date in data")

                    for source in json_data['_source']['sources']:
                        # Add description of data as input
                        doc_data = ' '.join([doc_data, source['description']])

                    if self.metadata:
                        yield doc_data, (_id, _name, _collection, _type, _classification, _date)
                    else:
                        yield doc_data
                except KeyError:
                    print("No sources key detected!")
                    self.empty_counter += 1

    def csv_iterator(self):
        """
        Parser of CorrespondentEx cleaned csv files.
        """
        print("Loading input as JSON formatted file")
        with open(self.path) as csv_file:
            csv_data = csv.reader(csv_file)

            # Skip the column names
            next(csv_data)
            # Increase the csv max field size
            csv.field_size_limit(sys.maxsize)

            for index, row in enumerate(csv_data):
                # if not index % 1000:
                print("extracting line {}".format(index))

                # For some reason the index got duplicated, hence counting from 1 (blasphemy!)
                _id = row[1]
                _text = ast.literal_eval(row[2])

                terms = []
                for caption in _text:
                    for term in caption.split():
                        terms.append(term)

                if self.metadata:
                    yield terms, (_id,)
                else:
                    yield ''.join(terms)
