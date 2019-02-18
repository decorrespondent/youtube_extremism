import csv as _csv
from collections import namedtuple as _namedtuple

from .util import is_empty_file as _is_empty_file
from .util import convert_to_dictionary as _convert_to_dictionary

video = _namedtuple('video', ('video_id',
                              'video_published',
                              'channel_id',
                              'video_title',
                              'video_description',
                              'video_channel_title',
                              'video_tags',
                              'video_category_id',
                              'video_default_language',
                              'video_duration',
                              'video_view_count',
                              'video_comment_count',
                              'video_likes_count',
                              'video_dislikes_count',
                              'video_topic_ids',
                              'video_topic_categories'
                              ))


def _get_video_header():
    return video._fields


def get_more_videos(channel_uploads, youtube_client, next_page_token, max_results=None):
    """takes the id of the uploads_playlist
    in channel data"""

    return youtube_client.playlistItems().list(
        part='snippet,contentDetails',
        playlistId=channel_uploads,
        maxResults=50,
        pageToken=next_page_token
    ).execute()


def get_videos(channel_uploads, youtube_client, max_results=None):
    return youtube_client.playlistItems().list(
        part='snippet,contentDetails',
        playlistId=channel_uploads,
        maxResults=50
    ).execute()


def _get_video_metadata(video_id, youtube_client):
    return youtube_client.videos().list(
        part='snippet,contentDetails,statistics,topicDetails',
        id=video_id
    ).execute()


def _get_topic_ids(metadata):
    if "topicDetails" in metadata:
        return metadata['topicDetails'].get('relevantTopicIds', "not set")
    else:
        return "not set"


def _get_topic_categories(metadata):
    if "topicDetails" in metadata:
        return metadata['topicDetails'].get('topicCategories', "not set")
    else:
        return "not set"


def convert_to_videos(response, youtube_client):
    videos = list()
    for data in response['items']:
        video_id = data['contentDetails']['videoId']
        video_metadata = _get_video_metadata(video_id, youtube_client)
        metadata = video_metadata['items'][0]

        next_video = video(video_id=video_id,
                           video_published=data['snippet']['publishedAt'],
                           channel_id=data['snippet']['channelId'],
                           video_title=data['snippet']['title'],
                           video_description=data['snippet'].get('description', 'not set'),
                           video_channel_title=data['snippet']['channelTitle'],
                           video_tags=metadata['snippet'].get('tags', 'not set'),
                           video_category_id=metadata['snippet'].get('categoryId', 'not set'),
                           video_default_language=metadata['snippet'].get('defaultLanguage', 'not set'),
                           video_duration=metadata['contentDetails']['duration'],
                           video_view_count=metadata['statistics'].get('viewCount', 0),
                           video_comment_count=metadata['statistics'].get('commentCount', 0),
                           video_likes_count=metadata['statistics'].get('likeCount', 0),
                           video_dislikes_count=metadata['statistics'].get('dislikeCount', 0),
                           video_topic_ids=_get_topic_ids(metadata),
                           video_topic_categories=_get_topic_categories(metadata)
                           )
        videos.append(next_video)

    return videos


def write_videos(videos, video_file):
    with open(video_file, "a") as csv_file:
        writer = _csv.DictWriter(csv_file, fieldnames=_get_video_header())
        if _is_empty_file(video_file):
            writer.writeheader()

        for video_row in videos:
            writer.writerow(_convert_to_dictionary(video_row))
