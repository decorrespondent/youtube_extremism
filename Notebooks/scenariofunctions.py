# Functions needed

# Clean socialblade data
# Plot bars
# Select topics in tags
# Select topics in comments
# Include commenters
# Exclude commenters
# Include channels
# Excude channel

import pandas as pd
from tqdm import tqdm_notebook as tqdm
import matplotlib.pyplot as plt 
import datetime as dt
import scenariofunctions as sf
import glob 
import csv 
import re
import sys
import os
import config

def socialblade_ranking(channels):
     '''takes a messy social blade dataframe
     and cleans it up'''
     
     channels['Source Url'] = channels['Source Url'].str.replace('https://socialblade.com/youtube/channel/', '')
     channels['Subscriber_Rank'] = channels['Subscriber_Rank'].replace('\D', '', regex=True).apply(pd.to_numeric)
     channels['Video_View_Rank'] = channels['Video_View_Rank'].replace('\D', '', regex=True).apply(pd.to_numeric)
     channels['Sb_Rank'] = channels['Sb_Rank'].replace('\D', '', regex=True).apply(pd.to_numeric)
     channels['earnings_low'], channels['earnings_high'] = channels['Estimated_Yearly_Earning'].str.split('-', 1).str
     channels['earnings_low'] = channels['earnings_low'].replace('st|th|rd|nd', '', regex=True)
     channels['earnings_high'] = channels['earnings_high'].replace('st|th|rd|nd', '', regex=True)
     channels = channels.rename(columns={'Source Url': 'channel_id',
                                   'Subscriber_Rank': 'subscriber_rank',
                                   'Video_View_Rank': 'video_view_rank',
                                   'Sb_Rank': 'sb_rank',
                                   'Grade': 'grade'
                              })
     channels = channels[['channel_id', 'subscriber_rank', 'video_view_rank', 'sb_rank', 'grade']]

     return channels


def socialblade_growth(channel_history):

     pattern = re.compile('(\d{4}-\d{2}-\d+,\d+)')
     channel_history['daily_views'] = channel_history['Date_Daily_Views'].str.findall(pattern)
     channel_history['daily_subs'] = channel_history['Date_Total_Subs'].str.findall(pattern)
     channel_history = channel_history.rename(columns={'User':'channel_id'})
     daily_views = channel_history.set_index('channel_id') \
               .daily_views.apply(pd.Series) \
               .stack() \
               .reset_index(level=-1, drop=True) \
               .reset_index()
     
     daily_views['date'], daily_views['views'] = daily_views[0].str.split(',', 1).str
     daily_views = daily_views[['channel_id', 'date', 'views']]

     daily_subs = channel_history.set_index('channel_id') \
               .daily_subs.apply(pd.Series) \
               .stack() \
               .reset_index(level=-1, drop=True) \
               .reset_index()

     daily_subs['date'], daily_subs['subs'] = daily_subs[0].str.split(',', 1).str
     daily_subs = daily_subs[['channel_id', 'date', 'subs']]

     daily_stats = pd.merge(daily_subs, daily_views,  how='left', left_on=['channel_id', 'date'], right_on = ['channel_id', 'date'])
     daily_stats['yearmonth'] = pd.to_datetime(daily_stats['date']).dt.to_period('M')
     
     return daily_stats


def channel_filter(dataframe, selection):
     filtered_data = dataframe[dataframe['video_channel_title'].isin(selection)]
     print('deze selectie levert ' + str(len(filtered_data)) + ' videos op.')
     return filtered_data


def add_years_months_to_videos(dataframe):
     dataframe.loc[:,('year')] = pd.to_datetime(dataframe.loc[:,('video_published')]).dt.to_period('Y')
     dataframe.loc[:,('yearmonth')] = pd.to_datetime(dataframe.loc[:,('video_published')]).dt.to_period('M')

     return dataframe


def plot_views_per_year(dataframe):
     views_per_year = dataframe.groupby(['year'])['video_view_count'].agg('sum')
     fig = plt.figure(figsize=(10,5))
     width = 0.4
     ax = fig.add_subplot(111) 
     views_per_year.plot(kind='bar', color='red', width=width, grid=True)
     ax.set_ylabel('number of videos published')
     ax.set_xlabel('year')

     return plt.show()

def plot_top_channels(dataframe):
     top_channels = dataframe['video_channel_title'].value_counts()[0:20]
     fig = plt.figure(figsize=(20,10)) # Create matplotlib figure
     width = 0.4
     ax = fig.add_subplot(111) 
     top_channels.plot(kind='bar', color='red', width=width, grid=True)
     ax.set_ylabel('number of videos published')
     ax.set_xlabel('channels')
     
     return  plt.show()

def plot_users(dataframe):
     top_users = dataframe['author_display_name'].value_counts()[0:20]
     fig = plt.figure(figsize=(20,10)) # Create matplotlib figure
     width = 0.4
     ax = fig.add_subplot(111) 
     top_users.plot(kind='bar', color='red', width=width, grid=True)
     ax.set_ylabel('number of videos published')
     ax.set_xlabel('channels')
     
     return  plt.show()


def topic_filter(dataframe, query, query_topic):
     pattern = '|'.join([s for s in query])
     mask = dataframe['video_tags'].str.contains(pattern, regex=True, case=False, na=False)
     topic = dataframe[mask]
     print('found ' + str(len(topic)) + ' videos with ' + query_topic)
     
     return topic

def zoom_in_on_commenter(dataframe, name):
     result = dataframe[dataframe['author_display_name'] == name]
     return result


def extract_tags(dataframe):
     vidtags = dataframe[['video_id', 'video_title', 'video_tags', 'year']]

     video_tags = vidtags['video_tags'].str.replace(r"\[|\]|\'|-", '') \
                    .str.lower() \
                    .str.split(', ', expand=True) \
                    .merge(vidtags, right_index = True, left_index = True) \
                    .drop(["video_tags"], axis = 1) \
                    .melt(id_vars = ['video_id', 'video_title', 'year'], value_name = "tag") \
                    .drop(['variable'], axis=1) \
                    .dropna()

     video_tags = video_tags[~video_tags['tag'].str.contains('not set')]
     video_tags.sort_values('tag', inplace=True)
     video_tags['tag'] = video_tags['tag'].str.replace('"', '')
     print('found ' + str(video_tags.tag.nunique()) + ' unique tags')
     return video_tags

def tag_filter(dataframe, tag):
     result = dataframe[dataframe['tag'].str.contains(tag)]
     print('found ' + str(len(result)) + ' tags')
     return result

def get_comments_by_video_id(query, sphere):
     if sphere == 'nl_right':
          path = config.PATH_NL
     if sphere == 'left':
          path = config.PATH_LEFT
     elif sphere == 'right':
          path = config.PATH_RIGHT
     else:
          print('sphere not found \n please try again')

     iter_csv = pd.read_csv(path + 'comments_' + sphere + '.csv', 
                        chunksize=1000000, 
                        sep='¶',
                        quotechar='þ',
                        engine='python')
     result = pd.concat([chunk[chunk['video_id'].isin(query)] for chunk in iter_csv])
     result['sphere'] = sphere
     result.loc[:,('year')] = pd.to_datetime(result.loc[:,('comment_time')]).dt.to_period('Y')
     result = result[['video_id', 'comment_id', 'author_display_name', 'author_channel_id', 'comment_text', 'comment_time', 'year', 'sphere']]
     print('found ' + str(len(result)) + ' comments \n and ' + str(result.author_channel_id.nunique()) + ' unique commenters')
     return result

def get_comments_by_author(query, sphere):
     if sphere == 'nl_right':
          path = config.PATH_NL
     if sphere == 'left':
          path = config.PATH_LEFT
     elif sphere == 'right':
          path = config.PATH_RIGHT
     else:
          print('sphere not found \n please try again')

     iter_csv = pd.read_csv(path + 'comments_' + sphere + '.csv', 
                        chunksize=1000000, 
                        sep='¶',
                        quotechar='þ',
                        engine='python')
     result = pd.concat([chunk[chunk['author_channel_id'].isin(query)] for chunk in iter_csv])
     result['sphere'] = sphere
     result.loc[:,('year')] = pd.to_datetime(result.loc[:,('comment_time')]).dt.to_period('Y')
     result = result[['video_id', 'comment_id', 'author_display_name', 'author_channel_id', 'comment_text', 'comment_time', 'year', 'sphere']]
     print('found ' + str(len(result)) + ' comments \n and ' + str(result.author_channel_id.nunique()) + ' unique commenters')
     return result