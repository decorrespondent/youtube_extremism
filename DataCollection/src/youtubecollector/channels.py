import csv as _csv
from collections import namedtuple as _namedtuple
from .util import is_empty_file as _is_empty_file
from .util import convert_to_dictionary as _convert_to_dictionary

channel = _namedtuple("channel", ('channel_id',
                                  'channel_title',
                                  'channel_description',
                                  'channel_default_language',
                                  'channel_country',
                                  'channel_uploads',
                                  'channel_viewcount',
                                  'channel_commentcount',
                                  'channel_subscribercount',
                                  'channel_videocount',
                                  'channel_topic_ids',
                                  'channel_topic_categories',
                                  'channel_branding_keywords'))


def _get_channel_header():
    return channel._fields


def _get_channel(channel_id, youtube_client):
    """Queries the youtube API and gets a json in return"""

    return youtube_client.channels().list(
        part='snippet,contentDetails,topicDetails,statistics,brandingSettings',
        id=channel_id
    ).execute()


def _convert_to_channel(response) -> channel:
    """Extracts the needed variables from the returned json"""
    response_channel = response['items'][0]
    return channel(channel_id=response_channel['id'],
                   channel_title=response_channel['snippet']['title'],
                   channel_description=response_channel['snippet']['description'],
                   channel_default_language=response_channel['snippet'].get('defaultLanguage', 'not set'),
                   channel_country=response_channel['snippet'].get('country', 'not set'),
                   channel_uploads=response_channel['contentDetails']['relatedPlaylists'].get('uploads', ''),
                   channel_viewcount=response_channel['statistics']['viewCount'],
                   channel_commentcount=response_channel['statistics']['commentCount'],
                   channel_subscribercount=response_channel['statistics']['subscriberCount'],
                   channel_videocount=response_channel['statistics']['videoCount'],
                   channel_topic_ids=response_channel['topicDetails'].get('topicIds', 'not set'),
                   channel_topic_categories=response_channel['topicDetails'].get('topicCategories', 'not set'),
                   channel_branding_keywords=response_channel['brandingSettings']['channel'].get('keywords', 'not set')
                   )


def get_channels(channel_seeds, youtube_client):
    channels = list()
    for channel_id in channel_seeds['channel_id']:
        response = _get_channel(channel_id, youtube_client)
        next_channel = _convert_to_channel(response)
        channels.append(next_channel)
        print(channel_id)

    return channels


def write_channels(channels, channel_filename):
    with open(channel_filename, "a") as csv_file:
        writer = _csv.DictWriter(csv_file, fieldnames=_get_channel_header())
        if _is_empty_file(channel_filename):
            writer.writeheader()

        for channel_row in channels:
            writer.writerow(_convert_to_dictionary(channel_row))
