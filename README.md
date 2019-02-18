# youtube_extremism

This is a repository for the research into radical and extremist infospheres on YouTube.

The code consists of several modules, packages and collections of code.

## DataCollection 

DataCollection contains a library for, well, large scale data collection. The code takes a list of channels and collects, through the YouTube APIm, the following data types:
1. Channel information (basic statistics, relevant playlist ids and more)
2. Videos (statistics and descriptions)
3. Comments (all comments of the videos)
4. Recommendations (all recommendations for the gathered videos)
5. Transcripts (transcripts, if available, in English of the videos, gathered with the [youtube-dl library](https://rg3.github.io/youtube-dl/)

You'll find additional documentation in the DataCollection folder.

## RabbitHole

Contains scripts and notebooks to gather and analyse data we used for an experiment into the recommendation system of YouTube. 

## Notebooks

Contains all notebooks used for the analysis of the data on infospheres. There are many notebooks and see them as a source of inspiration.

## TopicModelling

Contains a lot of scripts, data and ideas for natural language processing. The transcripts are a real treasure. During two hackathons we've written code to get a grip on this data. 

## Finally

If you are interested in the data (we have gathered aroung 100GB, or 500.000 videos of far right and far left content), please drop me a line. 

All code is written in python3. 

Please let me know what we can do better. And please share your findings with us.
