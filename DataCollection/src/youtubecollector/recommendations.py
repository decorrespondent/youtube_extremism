import csv as _csv
from collections import namedtuple as _namedtuple

from .util import is_empty_file as _is_empty_file
from .util import convert_to_dictionary as _convert_to_dictionary

recommendation = _namedtuple("recommendation", ('video_id',
                                                'target_video_id',
                                                'published_at',
                                                'channel_id',
                                                'video_title',
                                                'video_description'))


def _get_recommendations_header():
    return recommendation._fields


def get_recommendations(video_id, youtube_client, max_results=50):
    return youtube_client.search().list(
        part='snippet',
        type='video',
        relatedToVideoId=video_id,
        maxResults=max_results
    ).execute()


def convert_to_recommendations(response, video_id):
    recommendations = list()
    for data in response['items']:
        next_recommendation = recommendation(video_id=video_id,
                                             target_video_id=data['id']['videoId'],
                                             published_at=data['snippet']['publishedAt'],
                                             channel_id=data['snippet']['channelId'],
                                             video_title=data['snippet']['title'],
                                             video_description=data['snippet']['description'])

        recommendations.append(next_recommendation)

    return recommendations


def write_recommendations(recommendations_file, recommendations):
    header = _get_recommendations_header()

    with open(recommendations_file, 'a') as csv_file:
        writer = _csv.DictWriter(csv_file, fieldnames=header)

        if _is_empty_file(recommendations_file):
            writer.writeheader()

        for recommendation_row in recommendations:
            writer.writerow(_convert_to_dictionary(recommendation_row))
