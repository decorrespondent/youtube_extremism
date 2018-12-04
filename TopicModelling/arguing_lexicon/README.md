Arguing Lexicon Filter
======================

Filters transcripts to only include text that contains argument lexicon.
For details about this lexicon please [read here](https://github.com/fako/spacy_arguing_lexicon#how-it-works).


Prerequisites
-------------

* Conda


Installation
------------

Make sure you are with a terminal inside ```arguing_lexicon```. Then setup your environment with:

```conda env create -f environment.yml```

Original data was the [captions_metadata.csv](https://drive.google.com/drive/folders/13f2fYPIsiednDBTMhd7rvCyikD_R6405) from the right_wing folder.
Place the data you want to work with inside the ```data``` folder and make sure it uses the same columns as the original data. 
Note that it simply copies most columns and only really needs the ```content``` column.

After that you should be able to start a Jupyter session with:

```jupyter notebook```

