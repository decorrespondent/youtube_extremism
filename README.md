# youtube_extremism

This is a repository for the research into radical and extremist infospheres on YouTube. We have used this code for a series of stories at de Volkskrant ([link to stories](https://volkskrant.nl/youtube)) and de Correspondent ([link to stories](https://decorrespondent.nl/collectie/extreme-politieke-bewegingen))

The code consists of several modules, packages and collections of code.

## DataCollection 

DataCollection contains a library for, well, large scale data collection. The code takes a list of channels and collects, through the YouTube API, the following data types:
1. Channel information (basic statistics, relevant playlist ids and more)
2. Videos (statistics and descriptions)
3. Comments (all comments of the videos)
4. Recommendations (all recommendations for the gathered videos)
5. Transcripts (transcripts, if available, in English of the videos, gathered with the [youtube-dl library](https://rg3.github.io/youtube-dl/)

You'll find additional documentation in the [DataCollection folder.](https://github.com/dtokmetzis/youtube_extremism/tree/master/DataCollection)

## RabbitHole

Contains scripts and notebooks to gather and analyse data we used for an experiment into the recommendation system of YouTube. This codes still needs a lot of work.

## Notebooks

Contains some notebooks used for the analysis of the data on right and left wing 'infospheres.' They just scratch the surface of possible analyses, but they can help you along.

## TopicModelling

Contains a lot of scripts, data and ideas for natural language processing. The transcripts are a real treasure. During two hackathons we've written code to get a grip on this data. There is still a lot that need to be done, so please consider these scripts as suggestions.

## Finally

If you are interested in the data (we have gathered aroung 100GB, or 500.000 videos of far right and far left content), please drop me a line. We won't share our comment data without a clear agreement on how to process those safely, because they are really sensitive data. 

All code is written in python3. 

Please let me know what we can do better. And please share your findings with us.
