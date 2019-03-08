from unittest import TestCase

from utils_for_test import read_json_from_file, create_test_client_with_response
from youtubecollector.video import convert_to_videos, video


class VideoTest(TestCase):

    def test_get_video(self):
        client = create_test_client_with_response("video_metadata.json", "200")

        response = read_json_from_file("video.json")
        actual = convert_to_videos(response, client)

        expected = [
            video(video_id='The id of the video',
                  video_published='2015-01-01T01:01:01.000Z',
                  channel_id='Id of the channel',
                  video_title='The title of the video',
                  video_description='Description of the video',
                  video_channel_title='Title of the channel',
                  video_tags=['tag one', 'tag two'],
                  video_category_id='1',
                  video_default_language='not set',
                  video_duration='PT3M3S',
                  video_view_count='120',
                  video_comment_count='564',
                  video_likes_count='231',
                  video_dislikes_count='342',
                  video_topic_ids=[
                      'Relevant topics ids 1',
                      'Relevant topics ids 2'
                  ],
                  video_topic_categories=['https://en.wikipedia.org/wiki/Television_program',
                                          'https://en.wikipedia.org/wiki/Society'])
        ]

        self.assertEqual(actual, expected)
