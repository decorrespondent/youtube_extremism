# Preprocessing of captions

The attached ipython notebook cleans the csv files that were created straight from the .vtt files. They contain duplicates, sometimes combined in one line. Furthermore, since .csv does not support the python lists, these are saved as strings. 

**TODO:** Put the cleaning script straight in the script that reads the .vtt files.