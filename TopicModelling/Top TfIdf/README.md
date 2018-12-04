# Top TfIdf terms per channel/per year

> Inspiration/example: https://pudding.cool/2017/09/hip-hop-words/

IPython notebook in this folder takes a cleaned csv of transcripts and merges the texts per channel per year into one document. Then it simply takes the top TfIdf words for each new document, so the channels can be compared over time.

## TfIdf options

- cutoff point was chosen on occurrence in one in 50, because channels span a lot of topics.
- Instead of linear term frequency (10 occurrences -> tf = 10), I followed the pudding in using sublinear term frequency (10 occurrences -> tf = 1 + log(9)). The basic idea is that a linear increase in use of a term does not linearly increase their importance. In terms of results, the linear term frequency yields a list of stop words per document. The sublinear tf returns a much more meaningful list.
- **TODO:** Lemmatize the words. I didn't have it available at the time, but knew someone else was working on it. As a result, I waited for the lemmatized set.

## Notebook contents

1. Top 10 per document
2. Top 100 in order to build networks of similarity. The networks this yields, however, are rather heavy, so that still needs finetuning.