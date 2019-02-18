import csv as _csv
from collections import namedtuple as _namedtuple

from googleapiclient.errors import HttpError

from .util import is_empty_file as _is_empty_file
from .util import convert_to_dictionary as _convert_to_dictionary

comment = _namedtuple("comment", ('video_id',
                                  'comment_id',
                                  'author_display_name',
                                  'author_channel_url',
                                  'author_channel_id',
                                  'comment_text',
                                  'comment_like_count',
                                  'comment_dislike_count',
                                  'comment_time',
                                  'reply_count'))


def _get_comment_header():
    return comment._fields


def get_comments(video_id, youtube_client):
    try:
        return youtube_client.commentThreads().list(
            videoId=video_id,
            part='snippet,replies',
            maxResults=100
        ).execute()
    except HttpError:
        return


def get_more_comments(video_id, youtube_client, next_page_token):
    try:
        return youtube_client.commentThreads().list(
            videoId=video_id,
            part='snippet,replies',
            pageToken=next_page_token,
            maxResults=100
        ).execute()
    except HttpError:
        return


def _get_author_channel_id(data):
    if "authorChannelId" in data['snippet']['topLevelComment']['snippet']:
        return data['snippet']['topLevelComment']['snippet']['authorChannelId'].get("value", 'not set')
    else:
        return "not set"


def convert_to_comments(response):
    if response is None:
        return list()

    comments = list()
    for data in response['items']:
        comments.append(comment(comment_id=data['id'],
                                video_id=data['snippet']['videoId'],
                                author_display_name=data['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                                author_channel_url=data['snippet']['topLevelComment']['snippet']['authorChannelUrl'],
                                author_channel_id=_get_author_channel_id(data),
                                comment_text=data['snippet']['topLevelComment']['snippet']['textDisplay'],
                                comment_like_count=data['snippet']['topLevelComment']['snippet']['likeCount'],
                                comment_dislike_count=data['snippet']['topLevelComment']['snippet'].get('disLikeCount', 0),
                                comment_time=data['snippet']['topLevelComment']['snippet']['publishedAt'],
                                reply_count=data['snippet']['totalReplyCount'])
                        )
        if 'replies' in data:
            for reply in data['replies']['comments']:
                #Replies kunnen worden herkend aan de id:
                # De id is opgebouwd uit twee elementen. {parent_comment_id}.{reply_id}
                # TODO[Olaf]: Is het zinnig om een identifier voor replies mee te geven?

                comments.append(comment(comment_id=reply['id'],
                                        video_id=reply['snippet']['videoId'],
                                        author_display_name=reply['snippet']['authorDisplayName'],
                                        author_channel_url=reply['snippet']['authorChannelUrl'],
                                        author_channel_id=reply['snippet']['authorChannelId']['value'],
                                        comment_text=reply['snippet']['textDisplay'],
                                        comment_like_count=reply['snippet']['likeCount'],
                                        comment_dislike_count='',
                                        comment_time=reply['snippet']['publishedAt'],
                                        reply_count=''))

    return comments


def write_comments(comments_file, comments):
    with open(comments_file, 'a') as csv_file:
        writer = _csv.DictWriter(csv_file, fieldnames=_get_comment_header())
        if _is_empty_file(comments_file):
            writer.writeheader()

        for comment_row in comments:
            writer.writerow(_convert_to_dictionary(comment_row))
